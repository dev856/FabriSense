"""Compare multiple FabriSense experiment outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare FabriSense experiment directories.")
    parser.add_argument("experiment_dirs", nargs="+", help="One or more experiment directories containing metrics.json.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = []

    for experiment_dir in args.experiment_dirs:
        experiment_path = Path(experiment_dir)
        with (experiment_path / "config.json").open("r", encoding="utf-8") as handle:
            config = json.load(handle)
        with (experiment_path / "metrics.json").open("r", encoding="utf-8") as handle:
            metrics = json.load(handle)

        rows.append(
            {
                "experiment_dir": str(experiment_path.resolve()),
                "architecture": config["architecture"],
                "pretrained": config["pretrained"],
                "accuracy": metrics["accuracy"],
                "macro_f1": metrics["macro_f1"],
                "weighted_f1": metrics["weighted_f1"],
                "loss": metrics["loss"],
            }
        )

    rows.sort(key=lambda row: row["macro_f1"], reverse=True)
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
