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
    )
    labels = [label for label, _ in sorted(label_to_index.items(), key=lambda item: item[1])]
    model, _ = build_model(args.architecture, num_classes=len(labels), pretrained=args.pretrained)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    class_weights = compute_class_weights(label_to_index, class_counts).to(device)
    criterion = torch.nn.CrossEntropyLoss(weight=class_weights)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay)

    history: list[dict[str, float]] = []
    best_macro_f1 = -1.0
    best_path = experiment_dir / "best_model.pt"

    for epoch in range(1, args.epochs + 1):
        train_loss = train_one_epoch(model, loaders["train"], optimizer, criterion, device)
        val_loss, y_true, y_pred = evaluate(model, loaders["val"], criterion, device, torch)
        val_metrics = classification_metrics(y_true, y_pred, labels)
        history.append(
            {
                "epoch": epoch,
                "train_loss": train_loss,
                "val_loss": val_loss,
                "val_accuracy": val_metrics["accuracy"],
                "val_macro_f1": val_metrics["macro_f1"],
                "val_weighted_f1": val_metrics["weighted_f1"],
            }
        )
        print(
            f"epoch={epoch} train_loss={train_loss:.4f} val_loss={val_loss:.4f} "
            f"val_accuracy={val_metrics['accuracy']:.4f} val_macro_f1={val_metrics['macro_f1']:.4f}"
        )

        if val_metrics["macro_f1"] > best_macro_f1:
            best_macro_f1 = val_metrics["macro_f1"]
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


def train_one_epoch(model, loader, optimizer, criterion, device) -> float:
    model.train()
    running_loss = 0.0
    total_examples = 0

    for images, labels in loader:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        logits = model(images)
        loss = criterion(logits, labels)
        loss.backward()
        optimizer.step()

        batch_size = images.size(0)
        running_loss += loss.item() * batch_size
        total_examples += batch_size

    return running_loss / max(total_examples, 1)


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


def _write_json(path: Path, payload: Any) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


if __name__ == "__main__":
    main()
