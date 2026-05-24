"""Local trained-model inference for FabriSense."""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

from PIL import Image

from training.models import build_model


DEFAULT_CHECKPOINT_CANDIDATES = [
    "artifacts/model_e_efficientnet_b0_v1/best_model.pt",
    "artifacts/model_d_resnet34_v1/best_model.pt",
    "artifacts/model_b_resnet18_v2/best_model.pt",
    "artifacts/model_c_mobilenet_v3_small_v2/best_model.pt",
    "artifacts/model_g_alexnet_v1/best_model.pt",
    "artifacts/model_f_vgg16_v1/best_model.pt",
    "artifacts/model_a_scratch_v2/best_model.pt",
    "models/fabric_family_phase1/best_model.pt",
    "artifacts/model_b_resnet18_phase1/best_model.pt",
    "artifacts/model_b_resnet18_tuned/best_model.pt",
    "artifacts/model_b_resnet18/best_model.pt",
    "artifacts/model_a_scratch_tuned/best_model.pt",
    "artifacts/model_a_scratch/best_model.pt",
]


class LocalFabricModel:
    """Load a trained checkpoint and run local inference."""

    def __init__(self, checkpoint_path: str | Path | None = None):
        self.checkpoint_path = self._resolve_checkpoint_path(checkpoint_path)
        self._runtime: dict[str, Any] | None = None

    @property
    def is_available(self) -> bool:
        return self.checkpoint_path is not None and self.checkpoint_path.exists()

    @property
    def model_name(self) -> str:
        if not self.is_available:
            return "local-trained-model-unavailable"
        return self.checkpoint_path.parent.name

    def describe(self) -> Dict[str, Any]:
        if not self.is_available:
            return {
                "available": False,
                "checkpoint_path": None,
                "model_name": "Unavailable",
                "architecture": "Unknown",
                "class_count": 0,
                "labels": [],
            }

        try:
            checkpoint = self._load_checkpoint()
            labels = self._labels_from_checkpoint(checkpoint)
        except Exception as exc:
            return {
                "available": False,
                "checkpoint_path": str(self.checkpoint_path.resolve()),
                "model_name": self.model_name,
                "architecture": "Unavailable",
                "class_count": 0,
                "labels": [],
                "error": str(exc),
            }

        metadata = _read_json_if_exists(self.checkpoint_path.parent / "config.json")
        metrics = _read_json_if_exists(self.checkpoint_path.parent / "metrics.json")
        return {
            "available": True,
            "checkpoint_path": str(self.checkpoint_path.resolve()),
            "model_name": self.model_name,
            "architecture": checkpoint.get("architecture", metadata.get("architecture", "unknown")),
            "class_count": len(labels),
            "labels": labels,
            "pretrained": bool(checkpoint.get("pretrained", metadata.get("pretrained", False))),
            "metrics": metrics,
        }

    def predict(self, image: Image.Image) -> Dict[str, Any]:
        if not self.is_available:
            raise RuntimeError(
                "No trained local model checkpoint was found. Place a checkpoint in models/ or artifacts/ first."
            )

        runtime = self._load_runtime()
        torch = runtime["torch"]
        transform = runtime["transform"]
        model = runtime["model"]
        labels = runtime["labels"]
        device = runtime["device"]

        tensor = transform(image.convert("RGB")).unsqueeze(0).to(device)
        model.eval()
        with torch.no_grad():
            logits = model(tensor)
            probabilities = torch.softmax(logits, dim=1)[0]
            top_values, top_indices = torch.topk(probabilities, k=min(3, len(labels)))

        top_predictions = [
            {
                "label": labels[index],
                "confidence": round(float(value), 4),
            }
            for value, index in zip(top_values.cpu().tolist(), top_indices.cpu().tolist())
        ]
        primary = top_predictions[0]
        return {
            "label": primary["label"],
            "confidence": primary["confidence"],
            "top_predictions": top_predictions,
            "checkpoint_path": str(self.checkpoint_path.resolve()),
            "architecture": runtime["architecture"],
            "model_name": self.model_name,
        }

    def _load_runtime(self) -> dict[str, Any]:
        if self._runtime is not None:
            return self._runtime

        torch, transforms = _require_torch_and_transforms()
        checkpoint = self._load_checkpoint()
        labels = self._labels_from_checkpoint(checkpoint)
        architecture = checkpoint["architecture"]
        pretrained = bool(checkpoint.get("pretrained", False))
        image_size = int(checkpoint.get("image_size", 224))
        model, _ = build_model(architecture=architecture, num_classes=len(labels), pretrained=pretrained)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.load_state_dict(checkpoint["model_state_dict"])
        model = model.to(device)

        transform = transforms.Compose(
            [
                transforms.Resize((image_size, image_size)),
                transforms.ToTensor(),
                transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
            ]
        )
        self._runtime = {
            "torch": torch,
            "transform": transform,
            "model": model,
            "labels": labels,
            "device": device,
            "architecture": architecture,
        }
        return self._runtime

    def _load_checkpoint(self) -> Dict[str, Any]:
        torch, _ = _require_torch_and_transforms()
        return torch.load(self.checkpoint_path, map_location="cpu")

    def _resolve_checkpoint_path(self, checkpoint_path: str | Path | None) -> Path | None:
        candidates: list[Path] = []
        env_path = os.getenv("FABRISENSE_LOCAL_MODEL_PATH")
        if env_path:
            candidates.append(Path(env_path))
        if checkpoint_path is not None:
            candidates.append(Path(checkpoint_path))
        candidates.extend(Path(candidate) for candidate in DEFAULT_CHECKPOINT_CANDIDATES)

        for candidate in candidates:
            if candidate.exists():
                return candidate
        return None

    def _labels_from_checkpoint(self, checkpoint: Dict[str, Any]) -> list[str]:
        label_to_index = checkpoint.get("label_to_index", {})
        return [label for label, _ in sorted(label_to_index.items(), key=lambda item: item[1])]


@lru_cache(maxsize=1)
def get_local_model_client() -> LocalFabricModel:
    return LocalFabricModel()


def list_available_local_models() -> list[Dict[str, Any]]:
    seen: set[Path] = set()
    candidates = [Path(candidate) for candidate in DEFAULT_CHECKPOINT_CANDIDATES]
    artifacts_dir = Path("artifacts")
    if artifacts_dir.exists():
        candidates.extend(sorted(artifacts_dir.glob("*/best_model.pt")))
    models_dir = Path("models")
    if models_dir.exists():
        candidates.extend(sorted(models_dir.glob("**/best_model.pt")))

    entries: list[Dict[str, Any]] = []
    for checkpoint_path in candidates:
        resolved = checkpoint_path.resolve()
        if resolved in seen or not checkpoint_path.exists():
            continue
        seen.add(resolved)

        config = _read_json_if_exists(checkpoint_path.parent / "config.json")
        metrics = _read_json_if_exists(checkpoint_path.parent / "metrics.json")
        label_map = config.get("label_to_index", {}) if config else {}
        labels = [label for label, _ in sorted(label_map.items(), key=lambda item: item[1])]
        architecture = config.get("architecture", "unknown") if config else "unknown"
        pretrained = bool(config.get("pretrained", False)) if config else False
        macro_f1 = metrics.get("macro_f1") if metrics else None
        accuracy = metrics.get("accuracy") if metrics else None
        display_name = checkpoint_path.parent.name
        if architecture != "unknown":
            display_name = f"{display_name} | {architecture}"
        if macro_f1 is not None:
            display_name = f"{display_name} | macro F1 {macro_f1:.3f}"

        entries.append(
            {
                "display_name": display_name,
                "checkpoint_path": str(checkpoint_path.resolve()),
                "model_name": checkpoint_path.parent.name,
                "architecture": architecture,
                "pretrained": pretrained,
                "metrics": metrics,
                "class_count": len(labels),
                "labels": labels,
            }
        )

    entries.sort(key=lambda item: item.get("metrics", {}).get("macro_f1", -1), reverse=True)
    return entries


def _read_json_if_exists(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _require_torch_and_transforms():
    try:
        import torch
        from torchvision import transforms
    except ImportError as exc:  # pragma: no cover - runtime dependency
        raise ImportError(
            "PyTorch and torchvision are required for local trained-model inference. Install requirements-ml.txt."
        ) from exc
    return torch, transforms
