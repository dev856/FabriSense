"""Dataset manifest helpers for reproducible textile experiments."""

from __future__ import annotations

import csv
import json
import random
from collections import defaultdict
from pathlib import Path
from typing import Iterable

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def discover_class_images(
    dataset_root: str | Path,
    include_classes: Iterable[str] | None = None,
    exclude_classes: Iterable[str] | None = None,
) -> tuple[list[str], list[dict[str, str]]]:
    """Scan a class-folder dataset and return sorted labels plus records."""

    root = Path(dataset_root)
    if not root.exists():
        raise FileNotFoundError(f"Dataset root does not exist: {root}")

    include_lookup = _normalized_class_set(include_classes)
    exclude_lookup = _normalized_class_set(exclude_classes)

    class_dirs = sorted(path for path in root.iterdir() if path.is_dir())
    if not class_dirs:
        raise ValueError(f"No class directories found in dataset root: {root}")

    labels: list[str] = []
    records: list[dict[str, str]] = []

    for class_dir in class_dirs:
        normalized_name = class_dir.name.casefold()
        if include_lookup and normalized_name not in include_lookup:
            continue
        if normalized_name in exclude_lookup:
            continue

        image_paths = sorted(
            path
            for path in class_dir.rglob("*")
            if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
        )
        if not image_paths:
            continue

        labels.append(class_dir.name)
        for image_path in image_paths:
            records.append({"filepath": str(image_path.resolve()), "label": class_dir.name})

    if not records:
        raise ValueError(f"No supported image files found under dataset root: {root}")

    return labels, records


def stratified_split(
    records: Iterable[dict[str, str]],
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    seed: int = 42,
) -> dict[str, list[dict[str, str]]]:
    """Create stable train/val/test splits while preserving label balance."""

    if round(train_ratio + val_ratio + test_ratio, 5) != 1.0:
        raise ValueError("train_ratio, val_ratio, and test_ratio must sum to 1.0")

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for record in records:
        grouped[record["label"]].append(record)

    rng = random.Random(seed)
    splits = {"train": [], "val": [], "test": []}

    for label, label_records in grouped.items():
        shuffled = list(label_records)
        rng.shuffle(shuffled)
        count = len(shuffled)

        train_count, val_count, test_count = _split_counts(count, train_ratio, val_ratio, test_ratio)

        splits["train"].extend(shuffled[:train_count])
        splits["val"].extend(shuffled[train_count : train_count + val_count])
        splits["test"].extend(shuffled[train_count + val_count : train_count + val_count + test_count])

    for split_name in splits:
        rng.shuffle(splits[split_name])

    return splits


def create_split_manifests(
    dataset_root: str | Path,
    output_dir: str | Path,
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    seed: int = 42,
    include_classes: Iterable[str] | None = None,
    exclude_classes: Iterable[str] | None = None,
) -> dict[str, int]:
    """Scan a dataset, split it, and write CSV manifests plus labels metadata."""

    labels, records = discover_class_images(
        dataset_root,
        include_classes=include_classes,
        exclude_classes=exclude_classes,
    )
    splits = stratified_split(
        records,
        train_ratio=train_ratio,
        val_ratio=val_ratio,
        test_ratio=test_ratio,
        seed=seed,
    )

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for split_name, split_records in splits.items():
        _write_manifest(output_path / f"{split_name}.csv", split_records)

    label_to_index = {label: index for index, label in enumerate(sorted(labels))}
    metadata = {
        "dataset_root": str(Path(dataset_root).resolve()),
        "labels": sorted(labels),
        "label_to_index": label_to_index,
        "seed": seed,
        "ratios": {"train": train_ratio, "val": val_ratio, "test": test_ratio},
        "counts": {split_name: len(split_records) for split_name, split_records in splits.items()},
        "class_counts": _class_counts(records),
        "included_classes": sorted(include_classes) if include_classes else [],
        "excluded_classes": sorted(exclude_classes) if exclude_classes else [],
    }
    with (output_path / "labels.json").open("w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2)

    return metadata["counts"]


def _write_manifest(path: Path, records: Iterable[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["filepath", "label"])
        writer.writeheader()
        for record in records:
            writer.writerow(record)


def _class_counts(records: Iterable[dict[str, str]]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for record in records:
        counts[record["label"]] += 1
    return dict(sorted(counts.items()))


def _normalized_class_set(values: Iterable[str] | None) -> set[str]:
    if values is None:
        return set()
    return {value.strip().casefold() for value in values if value.strip()}


def _split_counts(count: int, train_ratio: float, val_ratio: float, test_ratio: float) -> tuple[int, int, int]:
    if count == 1:
        return 1, 0, 0
    if count == 2:
        return 1, 1, 0

    train_count = max(1, int(round(count * train_ratio)))
    val_count = max(1, int(round(count * val_ratio)))
    test_count = count - train_count - val_count

    if test_count < 1:
        test_count = 1
        if train_count >= val_count and train_count > 1:
            train_count -= 1
        else:
            val_count = max(1, val_count - 1)

    total = train_count + val_count + test_count
    if total < count:
        train_count += count - total
    elif total > count:
        overflow = total - count
        while overflow > 0 and train_count > 1:
            train_count -= 1
            overflow -= 1
        while overflow > 0 and val_count > 1:
            val_count -= 1
            overflow -= 1
        while overflow > 0 and test_count > 1:
            test_count -= 1
            overflow -= 1

    return train_count, val_count, test_count
