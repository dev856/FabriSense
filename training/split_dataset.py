"""CLI for creating reproducible train/val/test manifests."""

from __future__ import annotations

import argparse
import json

from training.manifest import create_split_manifests


def _parse_classes(raw_value: str) -> list[str]:
    return [item.strip() for item in raw_value.split(",") if item.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Create manifest CSV files for FabriSense textile experiments.")
    parser.add_argument("--dataset-root", required=True, help="Directory containing one subfolder per class.")
    parser.add_argument("--output-dir", default="data/fabrics/manifests", help="Directory to write manifests.")
    parser.add_argument("--train-ratio", type=float, default=0.7, help="Training split ratio.")
    parser.add_argument("--val-ratio", type=float, default=0.15, help="Validation split ratio.")
    parser.add_argument("--test-ratio", type=float, default=0.15, help="Test split ratio.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed used for splitting.")
    parser.add_argument(
        "--include-classes",
        type=_parse_classes,
        default=None,
        help="Comma-separated class names to keep, for example Cotton,Denim,Silk.",
    )
    parser.add_argument(
        "--exclude-classes",
        type=_parse_classes,
        default=None,
        help="Comma-separated class names to drop, for example Blended,Unclassified.",
    )
    args = parser.parse_args()

    counts = create_split_manifests(
        dataset_root=args.dataset_root,
        output_dir=args.output_dir,
        train_ratio=args.train_ratio,
        val_ratio=args.val_ratio,
        test_ratio=args.test_ratio,
        seed=args.seed,
        include_classes=args.include_classes,
        exclude_classes=args.exclude_classes,
    )
    print(json.dumps(counts, indent=2))


if __name__ == "__main__":
    main()
