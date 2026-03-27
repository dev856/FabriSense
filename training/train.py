"""Train Model A or Model B for the FabriSense textile research workflow."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any

import numpy as np

from training.datasets import build_dataloaders, compute_class_weights
from training.metrics import classification_metrics
from training.models import build_model


def _require_torch() -> Any:
    try:
        import torch
    except ImportError as exc:  # pragma: no cover - runtime dependency
        raise ImportError(
            "PyTorch is required for training. Install requirements from requirements-ml.txt."
        ) from exc
    return torch


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a FabriSense textile classifier.")
    parser.add_argument("--manifest-dir", default="data/fabrics/manifests", help="Directory containing train/val/test CSVs.")
    parser.add_argument("--experiment-dir", required=True, help="Directory to save checkpoints and metrics.")
    parser.add_argument(
        "--architecture",
        default="scratch_cnn",
        choices=["scratch_cnn", "resnet18", "efficientnet_b0", "mobilenet_v3_small"],
        help="Model architecture to train.",
    )
    parser.add_argument("--epochs", type=int, default=12, help="Number of epochs.")
    parser.add_argument("--batch-size", type=int, default=16, help="Mini-batch size.")
    parser.add_argument("--learning-rate", type=float, default=1e-3, help="Optimizer learning rate.")
    parser.add_argument("--weight-decay", type=float, default=1e-4, help="AdamW weight decay.")
    parser.add_argument("--num-workers", type=int, default=0, help="PyTorch dataloader workers.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument("--pretrained", action="store_true", help="Use pretrained weights when supported.")
    parser.add_argument("--weighted-sampler", action="store_true", help="Oversample minority classes during training.")
    parser.add_argument(
        "--loss-weighting",
        default="class_weights",
        choices=["none", "class_weights"],
        help="Loss weighting strategy for imbalanced classes.",
    )
    parser.add_argument("--label-smoothing", type=float, default=0.0, help="Cross-entropy label smoothing.")
    parser.add_argument(
        "--scheduler",
        default="plateau",
        choices=["none", "plateau"],
        help="Learning-rate scheduler.",
    )
    parser.add_argument("--scheduler-patience", type=int, default=2, help="Epochs to wait before reducing LR.")
    parser.add_argument("--scheduler-factor", type=float, default=0.5, help="LR decay factor for plateau scheduler.")
    parser.add_argument("--min-learning-rate", type=float, default=1e-6, help="Lower LR bound for schedulers.")
    parser.add_argument("--gradient-clip-norm", type=float, default=0.0, help="Clip gradient norm when above zero.")
    parser.add_argument(
        "--early-stopping-patience",
        type=int,
        default=0,
        help="Stop after this many non-improving epochs. Zero disables early stopping.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    torch = _require_torch()

    set_seed(args.seed, torch)
    experiment_dir = Path(args.experiment_dir)
    experiment_dir.mkdir(parents=True, exist_ok=True)

    _, image_size = build_model(args.architecture, num_classes=1, pretrained=args.pretrained)
    loaders, label_to_index, class_counts = build_dataloaders(
        manifest_dir=args.manifest_dir,
        image_size=image_size,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        weighted_sampler=args.weighted_sampler,
    )
    labels = [label for label, _ in sorted(label_to_index.items(), key=lambda item: item[1])]
    model, _ = build_model(args.architecture, num_classes=len(labels), pretrained=args.pretrained)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    criterion_kwargs: dict[str, Any] = {"label_smoothing": args.label_smoothing}
    if args.loss_weighting == "class_weights":
        criterion_kwargs["weight"] = compute_class_weights(label_to_index, class_counts).to(device)
    criterion = torch.nn.CrossEntropyLoss(**criterion_kwargs)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay)
    scheduler = _build_scheduler(args, optimizer, torch)

    history: list[dict[str, float]] = []
    best_macro_f1 = -1.0
    epochs_without_improvement = 0
    best_path = experiment_dir / "best_model.pt"

    for epoch in range(1, args.epochs + 1):
        train_loss, train_accuracy = train_one_epoch(
            model,
            loaders["train"],
            optimizer,
            criterion,
            device,
            torch,
            gradient_clip_norm=args.gradient_clip_norm,
        )
        val_loss, y_true, y_pred = evaluate(model, loaders["val"], criterion, device, torch)
        val_metrics = classification_metrics(y_true, y_pred, labels)
        current_lr = float(optimizer.param_groups[0]["lr"])
        history.append(
            {
                "epoch": epoch,
                "train_loss": train_loss,
                "train_accuracy": train_accuracy,
                "val_loss": val_loss,
                "val_accuracy": val_metrics["accuracy"],
                "val_macro_f1": val_metrics["macro_f1"],
                "val_weighted_f1": val_metrics["weighted_f1"],
                "learning_rate": current_lr,
            }
        )
        print(
            f"epoch={epoch} train_loss={train_loss:.4f} train_accuracy={train_accuracy:.4f} "
            f"val_loss={val_loss:.4f} val_accuracy={val_metrics['accuracy']:.4f} "
            f"val_macro_f1={val_metrics['macro_f1']:.4f} lr={current_lr:.6f}"
        )

        if scheduler is not None:
            scheduler.step(val_metrics["macro_f1"])

        if val_metrics["macro_f1"] > best_macro_f1:
            best_macro_f1 = val_metrics["macro_f1"]
            epochs_without_improvement = 0
            torch.save(
                {
                    "architecture": args.architecture,
                    "pretrained": args.pretrained,
                    "image_size": image_size,
                    "label_to_index": label_to_index,
                    "model_state_dict": model.state_dict(),
                },
                best_path,
            )
        else:
            epochs_without_improvement += 1

        if args.early_stopping_patience > 0 and epochs_without_improvement >= args.early_stopping_patience:
            print(f"early_stopping_triggered_at_epoch={epoch}")
            break

    checkpoint = torch.load(best_path, map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])
    test_loss, y_true, y_pred = evaluate(model, loaders["test"], criterion, device, torch)
    test_metrics = classification_metrics(y_true, y_pred, labels)
    test_metrics["loss"] = test_loss

    metadata = {
        "architecture": args.architecture,
        "pretrained": args.pretrained,
        "epochs": args.epochs,
        "batch_size": args.batch_size,
        "learning_rate": args.learning_rate,
        "weight_decay": args.weight_decay,
        "seed": args.seed,
        "manifest_dir": str(Path(args.manifest_dir).resolve()),
        "label_to_index": label_to_index,
        "weighted_sampler": args.weighted_sampler,
        "loss_weighting": args.loss_weighting,
        "label_smoothing": args.label_smoothing,
        "scheduler": args.scheduler,
        "scheduler_patience": args.scheduler_patience,
        "scheduler_factor": args.scheduler_factor,
        "min_learning_rate": args.min_learning_rate,
        "gradient_clip_norm": args.gradient_clip_norm,
        "early_stopping_patience": args.early_stopping_patience,
    }
    _write_json(experiment_dir / "config.json", metadata)
    _write_json(experiment_dir / "history.json", history)
    _write_json(experiment_dir / "metrics.json", test_metrics)

    summary = {
        "architecture": args.architecture,
        "pretrained": args.pretrained,
        "best_val_macro_f1": best_macro_f1,
        "test_accuracy": test_metrics["accuracy"],
        "test_macro_f1": test_metrics["macro_f1"],
        "test_weighted_f1": test_metrics["weighted_f1"],
        "checkpoint": str(best_path.resolve()),
    }
    print(json.dumps(summary, indent=2))


def set_seed(seed: int, torch: Any) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def train_one_epoch(model, loader, optimizer, criterion, device, torch: Any, gradient_clip_norm: float = 0.0) -> tuple[float, float]:
    model.train()
    running_loss = 0.0
    total_examples = 0
    correct_predictions = 0

    for images, labels in loader:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        logits = model(images)
        loss = criterion(logits, labels)
        loss.backward()
        if gradient_clip_norm > 0:
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=gradient_clip_norm)
        optimizer.step()

        predictions = torch.argmax(logits, dim=1)
        batch_size = images.size(0)
        running_loss += loss.item() * batch_size
        total_examples += batch_size
        correct_predictions += int((predictions == labels).sum().item())

    return running_loss / max(total_examples, 1), correct_predictions / max(total_examples, 1)


def evaluate(model, loader, criterion, device, torch: Any) -> tuple[float, list[int], list[int]]:
    model.eval()
    running_loss = 0.0
    total_examples = 0
    y_true: list[int] = []
    y_pred: list[int] = []

    with torch.no_grad():
        for images, labels in loader:
            images = images.to(device)
            labels = labels.to(device)
            logits = model(images)
            loss = criterion(logits, labels)

            predictions = torch.argmax(logits, dim=1)
            batch_size = images.size(0)
            running_loss += loss.item() * batch_size
            total_examples += batch_size
            y_true.extend(labels.cpu().tolist())
            y_pred.extend(predictions.cpu().tolist())

    return running_loss / max(total_examples, 1), y_true, y_pred


def _build_scheduler(args: argparse.Namespace, optimizer, torch: Any):
    if args.scheduler == "none":
        return None
    if args.scheduler == "plateau":
        return torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer,
            mode="max",
            factor=args.scheduler_factor,
            patience=args.scheduler_patience,
            min_lr=args.min_learning_rate,
        )
    raise ValueError(f"Unsupported scheduler: {args.scheduler}")


def _write_json(path: Path, payload: Any) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


if __name__ == "__main__":
    main()
