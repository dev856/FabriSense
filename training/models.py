"""PyTorch model builders for FabriSense experiments."""

from __future__ import annotations

from typing import Any


def _require_torch() -> tuple[Any, Any]:
    try:
        import torch.nn as nn
        from torchvision import models
    except ImportError as exc:  # pragma: no cover - runtime dependency
        raise ImportError(
            "PyTorch and torchvision are required for training. Install requirements from requirements-ml.txt."
        ) from exc
    return nn, models


class _ScratchCNNProxy:
    """Factory wrapper so the module stays importable without torch installed."""

    @staticmethod
    def build(num_classes: int):
        nn, _ = _require_torch()

        class FabricScratchCNN(nn.Module):
            def __init__(self, num_classes: int):
                super().__init__()
                self.features = nn.Sequential(
                    nn.Conv2d(3, 32, kernel_size=3, padding=1),
                    nn.BatchNorm2d(32),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(2),
                    nn.Conv2d(32, 64, kernel_size=3, padding=1),
                    nn.BatchNorm2d(64),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(2),
                    nn.Conv2d(64, 128, kernel_size=3, padding=1),
                    nn.BatchNorm2d(128),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(2),
                    nn.Conv2d(128, 256, kernel_size=3, padding=1),
                    nn.BatchNorm2d(256),
                    nn.ReLU(inplace=True),
                    nn.AdaptiveAvgPool2d((1, 1)),
                )
                self.classifier = nn.Sequential(
                    nn.Flatten(),
                    nn.Dropout(p=0.3),
                    nn.Linear(256, 128),
                    nn.ReLU(inplace=True),
                    nn.Dropout(p=0.2),
                    nn.Linear(128, num_classes),
                )

            def forward(self, x):
                x = self.features(x)
                return self.classifier(x)

        return FabricScratchCNN(num_classes)


def build_model(architecture: str, num_classes: int, pretrained: bool = False):
    """Return a classification model and its preferred image size."""

    nn, models = _require_torch()
    architecture = architecture.lower()

    if architecture == "scratch_cnn":
        return _ScratchCNNProxy.build(num_classes), 224

    if architecture == "resnet18":
        weights = models.ResNet18_Weights.DEFAULT if pretrained else None
        model = models.resnet18(weights=weights)
        model.fc = nn.Linear(model.fc.in_features, num_classes)
        return model, 224

    if architecture == "efficientnet_b0":
        weights = models.EfficientNet_B0_Weights.DEFAULT if pretrained else None
        model = models.efficientnet_b0(weights=weights)
        classifier_input = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(classifier_input, num_classes)
        return model, 224

    if architecture == "mobilenet_v3_small":
        weights = models.MobileNet_V3_Small_Weights.DEFAULT if pretrained else None
        model = models.mobilenet_v3_small(weights=weights)
        classifier_input = model.classifier[3].in_features
        model.classifier[3] = nn.Linear(classifier_input, num_classes)
        return model, 224

    raise ValueError(
        f"Unsupported architecture '{architecture}'. Choose from scratch_cnn, resnet18, efficientnet_b0, mobilenet_v3_small."
    )
