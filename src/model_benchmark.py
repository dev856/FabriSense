"""Checkpoint benchmarking helpers for comparing trained FabriSense models."""

from __future__ import annotations

import csv
import json
import shutil
import uuid
import zipfile
from pathlib import Path
from typing import Any

from training.manifest import SUPPORTED_EXTENSIONS, discover_class_images
from training.datasets import build_dataloaders
from training.metrics import classification_metrics
from training.models import build_model


def _require_torch() -> Any:
    try:
        import torch
    except ImportError as exc:  # pragma: no cover - runtime dependency
        raise ImportError(
            "PyTorch is required for checkpoint benchmarking. Install requirements from requirements-ml.txt."
        ) from exc
    return torch


def list_manifest_directories(root: str | Path = "data") -> list[dict[str, Any]]:
    root_path = Path(root)
    if not root_path.exists():
        return []

    manifests = []
    for labels_path in sorted(root_path.glob("**/labels.json")):
        manifest_dir = labels_path.parent
        split_paths = {split: manifest_dir / f"{split}.csv" for split in ("train", "val", "test")}
        if not all(path.exists() for path in split_paths.values()):
            continue

        metadata = _read_json_if_exists(labels_path)
        manifests.append(
            {
                "display_name": str(manifest_dir),
                "manifest_dir": str(manifest_dir.resolve()),
                "dataset_root": metadata.get("dataset_root", ""),
                "label_count": len(metadata.get("labels", [])),
                "counts": metadata.get("counts", {}),
                "class_counts": metadata.get("class_counts", {}),
                "benchmark_mode": metadata.get("benchmark_mode", "standard"),
                "recommended_split": metadata.get("recommended_split", "test"),
            }
        )

    return manifests


def create_uploaded_benchmark_manifest(
    zip_path: str | Path,
    output_root: str | Path = "data/benchmark_uploads",
) -> dict[str, Any]:
    zip_file = Path(zip_path)
    if not zip_file.exists():
        raise FileNotFoundError(f"Benchmark ZIP does not exist: {zip_file}")

    benchmark_id = f"{zip_file.stem}-{uuid.uuid4().hex[:8]}"
    benchmark_root = Path(output_root) / benchmark_id
    extracted_dir = benchmark_root / "dataset"
    manifest_dir = benchmark_root / "manifests"
    extracted_dir.mkdir(parents=True, exist_ok=False)
    manifest_dir.mkdir(parents=True, exist_ok=False)

    try:
        with zipfile.ZipFile(zip_file, "r") as archive:
            archive.extractall(extracted_dir)

        dataset_root = _resolve_dataset_root(extracted_dir)
        labels, records = discover_class_images(dataset_root)

        _write_manifest(manifest_dir / "train.csv", records)
        _write_manifest(manifest_dir / "val.csv", records)
        _write_manifest(manifest_dir / "test.csv", records)

        metadata = {
            "dataset_root": str(dataset_root.resolve()),
            "labels": sorted(labels),
            "label_to_index": {label: index for index, label in enumerate(sorted(labels))},
            "counts": {split: len(records) for split in ("train", "val", "test")},
            "class_counts": _class_counts(records),
            "source_zip": str(zip_file.resolve()),
            "benchmark_mode": "uploaded_test_set",
            "recommended_split": "test",
        }
        (manifest_dir / "labels.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

        return {
            "benchmark_id": benchmark_id,
            "manifest_dir": str(manifest_dir.resolve()),
            "dataset_root": str(dataset_root.resolve()),
            "label_count": len(labels),
            "image_count": len(records),
            "counts": metadata["counts"],
            "class_counts": metadata["class_counts"],
            "source_zip": str(zip_file.resolve()),
        }
    except Exception:
        shutil.rmtree(benchmark_root, ignore_errors=True)
        raise


def evaluate_checkpoint_on_manifest(
    checkpoint_path: str | Path,
    manifest_dir: str | Path,
    split: str = "test",
    batch_size: int = 16,
    num_workers: int = 0,
    max_examples: int | None = None,
) -> dict[str, Any]:
    if split not in {"train", "val", "test"}:
        raise ValueError("split must be one of: train, val, test")

    torch = _require_torch()
    checkpoint = torch.load(checkpoint_path, map_location="cpu")
    label_to_index = checkpoint["label_to_index"]

    model, image_size = build_model(
        architecture=checkpoint["architecture"],
        num_classes=len(label_to_index),
        pretrained=False,
    )
    model.load_state_dict(checkpoint["model_state_dict"])

    loaders, manifest_label_to_index, _ = build_dataloaders(
        manifest_dir=manifest_dir,
        image_size=image_size,
        batch_size=batch_size,
        num_workers=num_workers,
    )
    labels = [label for label, _ in sorted(manifest_label_to_index.items(), key=lambda item: item[1])]

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    criterion = torch.nn.CrossEntropyLoss()

    loss, y_true, y_pred = _evaluate(
        model=model,
        loader=loaders[split],
        criterion=criterion,
        device=device,
        torch=torch,
        max_examples=max_examples,
    )
    metrics = classification_metrics(y_true, y_pred, labels)
    metrics["loss"] = loss
    metrics["evaluated_examples"] = len(y_true)
    metrics["manifest_dir"] = str(Path(manifest_dir).resolve())
    metrics["split"] = split
    metrics["checkpoint_path"] = str(Path(checkpoint_path).resolve())
    metrics["model_name"] = Path(checkpoint_path).resolve().parent.name
    metrics["architecture"] = checkpoint.get("architecture", "unknown")
    return metrics


def compare_checkpoints_on_manifest(
    checkpoint_paths: list[str | Path],
    manifest_dir: str | Path,
    split: str = "test",
    batch_size: int = 16,
    num_workers: int = 0,
    max_examples: int | None = None,
) -> list[dict[str, Any]]:
    results = [
        evaluate_checkpoint_on_manifest(
            checkpoint_path=checkpoint_path,
            manifest_dir=manifest_dir,
            split=split,
            batch_size=batch_size,
            num_workers=num_workers,
            max_examples=max_examples,
        )
        for checkpoint_path in checkpoint_paths
    ]
    results.sort(key=lambda item: item.get("macro_f1", 0), reverse=True)
    return results


def _evaluate(
    model,
    loader,
    criterion,
    device,
    torch: Any,
    max_examples: int | None = None,
) -> tuple[float, list[int], list[int]]:
    model.eval()
    running_loss = 0.0
    total_examples = 0
    y_true: list[int] = []
    y_pred: list[int] = []

    with torch.no_grad():
        for images, labels in loader:
            if max_examples is not None and total_examples >= max_examples:
                break

            images = images.to(device)
            labels = labels.to(device)
            logits = model(images)
            loss = criterion(logits, labels)
            predictions = torch.argmax(logits, dim=1)

            if max_examples is not None:
                remaining = max_examples - total_examples
                if remaining < images.size(0):
                    labels = labels[:remaining]
                    predictions = predictions[:remaining]
                    loss = criterion(logits[:remaining], labels)
                    batch_size = remaining
                else:
                    batch_size = images.size(0)
            else:
                batch_size = images.size(0)

            running_loss += loss.item() * batch_size
            total_examples += batch_size
            y_true.extend(labels.cpu().tolist())
            y_pred.extend(predictions.cpu().tolist())

    return running_loss / max(total_examples, 1), y_true, y_pred


def _read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _resolve_dataset_root(extracted_dir: Path) -> Path:
    current_root = extracted_dir
    while True:
        child_dirs = [path for path in current_root.iterdir() if path.is_dir()]
        image_files = [
            path
            for path in current_root.iterdir()
            if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
        ]
        if image_files:
            return current_root
        if len(child_dirs) != 1:
            return current_root
        current_root = child_dirs[0]


def _write_manifest(path: Path, records: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["filepath", "label"])
        writer.writeheader()
        writer.writerows({"filepath": record["filepath"], "label": record["label"]} for record in records)


def _class_counts(records: list[dict[str, str]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        label = record["label"]
        counts[label] = counts.get(label, 0) + 1
    return dict(sorted(counts.items()))
