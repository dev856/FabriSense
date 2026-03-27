import csv
import json
import shutil
import unittest
import uuid
from pathlib import Path

from training.manifest import create_split_manifests, discover_class_images, stratified_split


class TrainingManifestTests(unittest.TestCase):
    def make_workspace_dir(self) -> Path:
        path = Path("data") / f"test_manifest_{uuid.uuid4().hex}"
        path.mkdir(parents=True, exist_ok=False)
        self.addCleanup(lambda: shutil.rmtree(path, ignore_errors=True))
        return path

    def test_discover_class_images_reads_class_folder_structure(self):
        root = self.make_workspace_dir()
        (root / "cotton").mkdir()
        (root / "silk").mkdir()
        for index in range(2):
            (root / "cotton" / f"cotton_{index}.jpg").write_bytes(b"fake")
        (root / "silk" / "silk_0.png").write_bytes(b"fake")

        labels, records = discover_class_images(root)

        self.assertEqual(labels, ["cotton", "silk"])
        self.assertEqual(len(records), 3)
        self.assertEqual(records[0]["label"], "cotton")

    def test_stratified_split_keeps_all_records(self):
        records = [
            {"filepath": f"/tmp/cotton_{index}.jpg", "label": "cotton"} for index in range(6)
        ] + [
            {"filepath": f"/tmp/silk_{index}.jpg", "label": "silk"} for index in range(6)
        ]

        splits = stratified_split(records, seed=7)

        total = sum(len(items) for items in splits.values())
        self.assertEqual(total, len(records))
        self.assertTrue(splits["train"])
        self.assertTrue(splits["val"])
        self.assertTrue(splits["test"])

    def test_create_split_manifests_writes_csv_and_metadata(self):
        workspace = self.make_workspace_dir()
        root = workspace / "raw"
        output = workspace / "manifests"
        for label in ("cotton", "denim"):
            class_dir = root / label
            class_dir.mkdir(parents=True)
            for index in range(4):
                (class_dir / f"{label}_{index}.jpg").write_bytes(b"fake")

        counts = create_split_manifests(root, output, seed=13)

        self.assertEqual(sum(counts.values()), 8)
        self.assertTrue((output / "train.csv").exists())
        self.assertTrue((output / "val.csv").exists())
        self.assertTrue((output / "test.csv").exists())

        with (output / "labels.json").open("r", encoding="utf-8") as handle:
            metadata = json.load(handle)
        self.assertEqual(metadata["labels"], ["cotton", "denim"])

        with (output / "train.csv").open("r", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertTrue(all("filepath" in row and "label" in row for row in rows))


if __name__ == "__main__":
    unittest.main()
