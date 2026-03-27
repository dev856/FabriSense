"""Evaluate a saved FabriSense textile checkpoint on a chosen split."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from training.datasets import build_dataloaders
from training.metrics import classification_metrics
from training.models import build_model


def _require_torch() -> Any:
    try:
        import torch
    except ImportError as exc:  # pragma: no cover - runtime dependency
        raise ImportError(
            "PyTorch is required for evaluation. Install requirements from requirements-ml.txt."
        ) from exc
    return torch


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate a FabriSense textile checkpoint.")
    parser.add_argument("--checkpoint", required=True, help="Path to best_model.pt.")
    parser.add_argument("--manifest-dir", default="data/fabrics/manifests", help="Directory containing split CSVs.")
    parser.add_argument("--split", default="test", choices=["train", "val", "test"], help="Dataset split to evaluate.")
    parser.add_argument("--batch-size", type=int, default=16, help="Mini-batch size.")
    parser.add_argument("--num-workers", type=int, default=0, help="PyTorch dataloader workers.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    torch = _require_torch()
    checkpoint = torch.load(args.checkpoint, map_location="cpu")

    model, image_size = build_model(
        architecture=checkpoint["architecture"],
        num_classes=len(checkpoint["label_to_index"]),
        pretrained=False,
    )
    model.load_state_dict(checkpoint["model_state_dict"])

    loaders, label_to_index, _ = build_dataloaders(
        manifest_dir=args.manifest_dir,
        image_size=image_size,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
    )
    labels = [label for label, _ in sorted(label_to_index.items(), key=lambda item: item[1])]

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    criterion = torch.nn.CrossEntropyLoss()

    loss, y_true, y_pred = _evaluate(model, loaders[args.split], criterion, device, torch)
    metrics = classification_metrics(y_true, y_pred, labels)
    metrics["loss"] = loss

    output_path = Path(args.checkpoint).resolve().parent / f"evaluation_{args.split}.json"
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(metrics, handle, indent=2)

    print(json.dumps({"split": args.split, "loss": loss, "macro_f1": metrics["macro_f1"]}, indent=2))


def _evaluate(model, loader, criterion, device, torch: Any) -> tuple[float, list[int], list[int]]:
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


if __name__ == "__main__":
    main()
