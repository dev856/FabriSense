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

    def test_discover_class_images_can_filter_classes(self):
        root = self.make_workspace_dir()
        for label in ("cotton", "silk", "wool"):
            class_dir = root / label
            class_dir.mkdir()
            (class_dir / f"{label}.jpg").write_bytes(b"fake")

        labels, records = discover_class_images(root, include_classes=["cotton", "wool"], exclude_classes=["wool"])

        self.assertEqual(labels, ["cotton"])
        self.assertEqual({record["label"] for record in records}, {"cotton"})

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

    def test_stratified_split_keeps_grouped_samples_together(self):
        records = []
        for label in ("cotton", "silk"):
            for sample_id in ("sample_a", "sample_b", "sample_c"):
                for index in range(4):
                    records.append(
                        {
                            "filepath": f"/tmp/{label}/{sample_id}/im_{index}.jpg",
                            "label": label,
                            "group_id": sample_id,
                        }
                    )

        splits = stratified_split(records, seed=11)

        assignments = {}
        for split_name, split_records in splits.items():
            for record in split_records:
                key = (record["label"], record["group_id"])
                if key in assignments:
                    self.assertEqual(assignments[key], split_name)
                else:
                    assignments[key] = split_name

        self.assertEqual(len(assignments), 6)

    def test_discover_class_images_assigns_group_ids_from_sample_folders(self):
        root = self.make_workspace_dir()
        sample_dir = root / "cotton" / "sample_1"
        sample_dir.mkdir(parents=True)
        for index in range(2):
            (sample_dir / f"im_{index}.jpg").write_bytes(b"fake")

        _, records = discover_class_images(root)

        self.assertEqual({record["group_id"] for record in records}, {"sample_1"})

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

    def test_create_split_manifests_persists_include_and_exclude_lists(self):
        workspace = self.make_workspace_dir()
        root = workspace / "raw"
        output = workspace / "manifests"
        for label in ("cotton", "denim", "silk"):
            class_dir = root / label
            class_dir.mkdir(parents=True)
            for index in range(3):
                (class_dir / f"{label}_{index}.jpg").write_bytes(b"fake")

        create_split_manifests(root, output, include_classes=["cotton", "silk"], exclude_classes=["silk"], seed=9)

        with (output / "labels.json").open("r", encoding="utf-8") as handle:
            metadata = json.load(handle)
        self.assertEqual(metadata["labels"], ["cotton"])
        self.assertEqual(metadata["included_classes"], ["cotton", "silk"])
        self.assertEqual(metadata["excluded_classes"], ["silk"])


if __name__ == "__main__":
    unittest.main()
