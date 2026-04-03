import json
import shutil
import unittest
import uuid
import zipfile
from pathlib import Path

from src.model_benchmark import create_uploaded_benchmark_manifest, list_manifest_directories


class ModelBenchmarkTests(unittest.TestCase):
    def make_manifest_dir(self) -> Path:
        path = Path("data") / f"test_benchmark_{uuid.uuid4().hex}" / "manifests"
        path.mkdir(parents=True, exist_ok=False)
        self.addCleanup(lambda: shutil.rmtree(path.parent, ignore_errors=True))
        return path

    def make_zip_path(self) -> Path:
        root = Path("data") / f"test_benchmark_zip_{uuid.uuid4().hex}"
        root.mkdir(parents=True, exist_ok=False)
        self.addCleanup(lambda: shutil.rmtree(root, ignore_errors=True))
        return root / "dataset.zip"

    def test_list_manifest_directories_discovers_valid_manifest_bundle(self):
        manifest_dir = self.make_manifest_dir()
        metadata = {
            "dataset_root": "data/fabrics/raw",
            "labels": ["cotton", "silk"],
            "counts": {"train": 10, "val": 4, "test": 4},
        }
        (manifest_dir / "labels.json").write_text(json.dumps(metadata), encoding="utf-8")
        for split in ("train", "val", "test"):
            (manifest_dir / f"{split}.csv").write_text("filepath,label\n", encoding="utf-8")

        manifests = list_manifest_directories("data")

        matching = [item for item in manifests if item["manifest_dir"] == str(manifest_dir.resolve())]
        self.assertEqual(len(matching), 1)
        self.assertEqual(matching[0]["label_count"], 2)

    def test_create_uploaded_benchmark_manifest_extracts_nested_zip(self):
        zip_path = self.make_zip_path()

        with zipfile.ZipFile(zip_path, "w") as archive:
            archive.writestr("benchmark/Cotton/example_1.jpg", b"fake")
            archive.writestr("benchmark/Denim/example_2.png", b"fake")

        bundle = create_uploaded_benchmark_manifest(zip_path, output_root=zip_path.parent / "prepared")

        manifest_dir = Path(bundle["manifest_dir"])
        self.addCleanup(lambda: shutil.rmtree(manifest_dir.parent, ignore_errors=True))

        self.assertTrue((manifest_dir / "labels.json").exists())
        self.assertTrue((manifest_dir / "test.csv").exists())
        self.assertEqual(bundle["label_count"], 2)
        self.assertEqual(bundle["image_count"], 2)


if __name__ == "__main__":
    unittest.main()
