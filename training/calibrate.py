"""Fit temperature scaling for a FabriSense checkpoint and report calibration error.

Fits one temperature on the val split (minimising NLL), reports ECE on the test split
before/after, and writes calibration.json next to the checkpoint. The app picks it up
automatically, so softmax confidences become trustworthy probabilities.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from training.datasets import build_dataloaders
from training.evaluate import _require_torch
from training.models import build_model


def softmax(logits: np.ndarray, temperature: float = 1.0) -> np.ndarray:
    scaled = logits / temperature
    scaled = scaled - scaled.max(axis=1, keepdims=True)
    exp = np.exp(scaled)
    return exp / exp.sum(axis=1, keepdims=True)


def expected_calibration_error(probabilities: np.ndarray, labels: np.ndarray, n_bins: int = 15) -> float:
    """Gap between confidence and accuracy, averaged over confidence bins (weighted by bin size)."""
    confidence = probabilities.max(axis=1)
    correct = probabilities.argmax(axis=1) == labels
    bins = np.minimum((confidence * n_bins).astype(int), n_bins - 1)
    ece = 0.0
    for b in range(n_bins):
        mask = bins == b
        if mask.any():
            ece += mask.mean() * abs(correct[mask].mean() - confidence[mask].mean())
    return float(ece)


def reliability_bins(probabilities: np.ndarray, labels: np.ndarray, n_bins: int = 10) -> list[dict]:
    confidence = probabilities.max(axis=1)
    correct = probabilities.argmax(axis=1) == labels
    bins = np.minimum((confidence * n_bins).astype(int), n_bins - 1)
    return [
        {
            "bin": f"{b / n_bins:.1f}-{(b + 1) / n_bins:.1f}",
            "count": int((bins == b).sum()),
            "confidence": float(confidence[bins == b].mean()),
            "accuracy": float(correct[bins == b].mean()),
        }
        for b in range(n_bins)
        if (bins == b).any()
    ]


def fit_temperature(logits: np.ndarray, labels: np.ndarray) -> float:
    # ponytail: 1-D grid search over T; exact enough for a single scalar, swap for LBFGS if you need more digits.
    def nll(temperature: float) -> float:
        probs = softmax(logits, temperature)
        return float(-np.log(probs[np.arange(len(labels)), labels] + 1e-12).mean())

    grid = np.linspace(0.25, 5.0, 476)
    return float(grid[np.argmin([nll(t) for t in grid])])


def collect_logits(model, loader, device, torch) -> tuple[np.ndarray, np.ndarray]:
    model.eval()
    all_logits, all_labels = [], []
    with torch.no_grad():
        for images, labels in loader:
            all_logits.append(model(images.to(device)).cpu().numpy())
            all_labels.append(labels.numpy())
    return np.concatenate(all_logits), np.concatenate(all_labels)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fit temperature scaling for a FabriSense checkpoint.")
    parser.add_argument("--checkpoint", required=True, help="Path to best_model.pt.")
    parser.add_argument("--manifest-dir", default="data/fabrics/manifests", help="Directory containing split CSVs.")
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--num-workers", type=int, default=0)
    args = parser.parse_args()

    torch = _require_torch()
    checkpoint = torch.load(args.checkpoint, map_location="cpu")
    model, image_size = build_model(
        architecture=checkpoint["architecture"],
        num_classes=len(checkpoint["label_to_index"]),
        pretrained=False,
    )
    model.load_state_dict(checkpoint["model_state_dict"])
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    loaders, _, _ = build_dataloaders(
        manifest_dir=args.manifest_dir,
        image_size=image_size,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
    )
    val_logits, val_labels = collect_logits(model, loaders["val"], device, torch)
    test_logits, test_labels = collect_logits(model, loaders["test"], device, torch)

    temperature = fit_temperature(val_logits, val_labels)
    result = {
        "temperature": temperature,
        "fit_split": "val",
        "test_ece_before": expected_calibration_error(softmax(test_logits), test_labels),
        "test_ece_after": expected_calibration_error(softmax(test_logits, temperature), test_labels),
        "reliability_before": reliability_bins(softmax(test_logits), test_labels),
        "reliability_after": reliability_bins(softmax(test_logits, temperature), test_labels),
    }
    output_path = Path(args.checkpoint).resolve().parent / "calibration.json"
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("temperature", "test_ece_before", "test_ece_after")}, indent=2))


if __name__ == "__main__":
    main()
