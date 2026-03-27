"""Manifest-backed PyTorch datasets for FabriSense experiments."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

from PIL import Image


def _require_training_deps() -> tuple[Any, Any, Any, Any, Any]:
    try:
        import torch
        from torch.utils.data import DataLoader, Dataset, WeightedRandomSampler
        from torchvision import transforms
    except ImportError as exc:  # pragma: no cover - runtime dependency
        raise ImportError(
            "PyTorch and torchvision are required for training. Install requirements from requirements-ml.txt."
        ) from exc
    return torch, DataLoader, Dataset, WeightedRandomSampler, transforms


class _DatasetProxy:
    @staticmethod
    def build():
        _, _, Dataset, _, _ = _require_training_deps()

        class FabricManifestDataset(Dataset):
            def __init__(self, records: list[dict[str, str]], label_to_index: dict[str, int], transform=None):
                self.records = records
                self.label_to_index = label_to_index
                self.transform = transform

            def __len__(self) -> int:
                return len(self.records)

            def __getitem__(self, index: int):
                record = self.records[index]
                image = Image.open(record["filepath"]).convert("RGB")
                if self.transform is not None:
                    image = self.transform(image)
                label = self.label_to_index[record["label"]]
                return image, label

        return FabricManifestDataset


def build_dataloaders(
    manifest_dir: str | Path,
    image_size: int,
    batch_size: int,
    num_workers: int = 0,
    weighted_sampler: bool = False,
) -> tuple[dict[str, Any], dict[str, int], dict[str, int]]:
    """Create train/val/test dataloaders from CSV manifests."""

    _, DataLoader, _, WeightedRandomSampler, transforms = _require_training_deps()
    dataset_cls = _DatasetProxy.build()
    manifest_path = Path(manifest_dir)

    with (manifest_path / "labels.json").open("r", encoding="utf-8") as handle:
        metadata = json.load(handle)
    label_to_index = metadata["label_to_index"]

    train_transform = transforms.Compose(
        [
            transforms.Resize((image_size, image_size)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(degrees=10),
            transforms.ColorJitter(brightness=0.15, contrast=0.15, saturation=0.1),
            transforms.ToTensor(),
            transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
        ]
    )
    eval_transform = transforms.Compose(
        [
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
        ]
    )

    loaders: dict[str, Any] = {}
    class_counts: dict[str, int] = {}
    for split_name in ("train", "val", "test"):
        records = _read_manifest(manifest_path / f"{split_name}.csv")
        dataset = dataset_cls(
            records=records,
            label_to_index=label_to_index,
            transform=train_transform if split_name == "train" else eval_transform,
        )

        loader_kwargs: dict[str, Any] = {
            "batch_size": batch_size,
            "num_workers": num_workers,
        }
        if split_name == "train":
            counter = Counter(record["label"] for record in records)
            class_counts = {label: counter.get(label, 0) for label in metadata["labels"]}
            if weighted_sampler:
                sample_weights = [1.0 / max(counter[record["label"]], 1) for record in records]
                loader_kwargs["sampler"] = WeightedRandomSampler(
                    weights=sample_weights,
                    num_samples=len(sample_weights),
                    replacement=True,
                )
            else:
                loader_kwargs["shuffle"] = True
        else:
            loader_kwargs["shuffle"] = False

        loaders[split_name] = DataLoader(dataset, **loader_kwargs)

    return loaders, label_to_index, class_counts


def compute_class_weights(label_to_index: dict[str, int], class_counts: dict[str, int]):
    """Inverse-frequency class weights for imbalanced datasets."""

    torch, _, _, _, _ = _require_training_deps()
    total = sum(class_counts.values())
    weights = [0.0] * len(label_to_index)

    for label, index in label_to_index.items():
        count = max(class_counts.get(label, 0), 1)
        weights[index] = total / (len(label_to_index) * count)

    return torch.tensor(weights, dtype=torch.float32)


def _read_manifest(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))
