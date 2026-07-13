"""
FabriSense: Fabric Classification for iBUG Fabrics Dataset
Kaggle Solution - handles garment-level folders with multiple illuminations

Dataset: ~2000 samples, 20 fabric classes, 4 illumination conditions per garment
Reference: https://www.kaggle.com/datasets/orchit/the-fabrics-dataset-by-ibug
"""

import random
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from torchvision import models
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, classification_report
from PIL import Image
import colorsys
import json

# Output directory configuration
OUTPUT_DIR = Path("./models")


class Config:
    """Training configuration for iBUG dataset."""
    IMG_SIZE = 224
    BATCH_SIZE = 32
    EPOCHS = 25
    LEARNING_RATE = 1e-4
    ARCHITECTURE = "efficientnet_b0"
    ILLUMINATION_COUNT = 4  # Each garment has 4 illumination images

    # 20 fabric classes from iBUG dataset
    FABRIC_CLASSES = [
        "Acrylic", "Chenille", "Corduroy", "Cotton", "Crepe",
        "Denim", "Felt", "Fleece", "Leather", "Linen",
        "Lut", "Nylon", "Polyester", "Satin", "Silk",
        "Suede", "Terrycloth", "Velvet", "Viscose", "Wool"
    ]

    # Class weights for imbalanced dataset (approximate inverse frequency)
    CLASS_WEIGHTS = {
        "Acrylic": 83, "Chenille": 77, "Corduroy": 42, "Cotton": 1,
        "Crepe": 50, "Denim": 7, "Felt": 250, "Fleece": 30,
        "Leather": 53, "Linen": 53, "Lut": 250, "Nylon": 17,
        "Polyester": 4, "Satin": 42, "Silk": 28, "Suede": 100,
        "Terrycloth": 33, "Velvet": 45, "Viscose": 27, "Wool": 5)


def set_seed(seed=42):
    """Set random seeds for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


class IBuGFabricDataset(Dataset):
    """Dataset handler for iBUG structure: garment folders with multiple illuminations."""

    def __init__(self, garment_dict, transform=None, aggregate_illum=True):
        """
        Args:
            garment_dict: {garment_id: {"images": [image_paths], "label": idx}}
            transform: Image transforms
            aggregate_illum: If True, treat all illuminations as one sample; if False, separate
        """
        self.data = []
        self.transform = transform

        for garment_id, info in garment_dict.items():
            if aggregate_illum:
                # Aggregate all illuminations into one sample
                self.data.append({
                    "images": info["images"],
                    "label": info["label"],
                    "garment_id": garment_id
                })
            else:
                # Separate each illumination
                for img_path in info["images"]:
                    self.data.append({
                        "images": [img_path],
                        "label": info["label"],
                        "garment_id": garment_id
                    })

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        entry = self.data[idx]
        images = []

        for img_path in entry["images"]:
            img = Image.open(img_path).convert('RGB')
            if self.transform:
                img = self.transform(img)
            images.append(img)

        # Stack illuminations or take first (for inference)
        if len(images) > 1:
            # Average across illuminations for training
            stacked = torch.stack(images)
            images = stacked.mean(dim=0)  # Simple averaging of all illuminations

        return images, entry["label"]


def load_ibug_dataset(data_dir, aggregate_illum=True):
    """
    Load iBUG dataset with correct folder structure handling.

    Structure:
    data_dir/
        train/
            garment_id_1/
                image_0000.jpg
                image_0001.jpg
                ...
            garment_id_2/
                ...
    """
    train_dir = Path(data_dir) / "train"
    garment_data = {}

    for garment_folder in train_dir.iterdir():
        if not garment_folder.is_dir():
            continue

        # Find all JPG images in this garment folder
        images = list(garment_folder.glob("*.jpg"))
        if not images:
            continue

        # Extract fabric type from folder name or CSV if provided
        # iBUG uses folder naming like A03031-1600080-1, we need label mapping
        garment_data[garment_folder.name] = {
            "images": images[:Config.ILLUMINATION_COUNT],  # Limit to 4 illuminations
            "label": None  # Will be set by caller
        }

    return garment_data


def build_model(architecture, num_classes, pretrained=True):
    """Build PyTorch model for fabric classification."""
    if architecture == "efficientnet_b0":
        model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)
        model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
        return model

    elif architecture == "resnet34":
        model = models.resnet34(weights=models.ResNet34_Weights.DEFAULT)
        model.fc = nn.Linear(model.fc.in_features, num_classes)
        return model

    elif architecture == "resnet18":
        model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        model.fc = nn.Linear(model.fc.in_features, num_classes)
        return model

    elif architecture == "mobilenet_v3_small":
        model = models.mobilenet_v3_small(weights=models.MobileNet_V3_Small_Weights.DEFAULT)
        model.classifier[3] = nn.Linear(model.classifier[3].in_features, num_classes)
        return model


def train_model(train_loader, val_loader, num_classes, class_weights=None):
    """Training loop with weighted loss for imbalanced data."""
    model = build_model(Config.ARCHITECTURE, num_classes)
    model = model.to(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))

    weights = None
    if class_weights:
        weights = torch.tensor([class_weights.get(cls, 1.0) for cls in Config.FABRIC_CLASSES])
        weights = weights.to(model.classifier[1].weight.device if hasattr(model, 'classifier') else 'cpu')

    criterion = nn.CrossEntropyLoss(weight=weights)
    optimizer = optim.AdamW(model.parameters(), lr=Config.LEARNING_RATE, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=Config.EPOCHS)

    best_f1 = 0.0
    history = {"train_loss": [], "val_f1": [], "val_acc": []}

    for epoch in range(Config.EPOCHS):
        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer)
        val_f1, val_acc = validate(model, val_loader)

        history["train_loss"].append(train_loss)
        history["val_f1"].append(val_f1)
        history["val_acc"].append(val_acc)

        print(f"Epoch {epoch+1}/{Config.EPOCHS}: Train Loss={train_loss:.4f}, "
              f"Val F1={val_f1:.4f}, Val Acc={val_acc:.4f}")

        if val_f1 > best_f1:
            best_f1 = val_f1
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            torch.save(model.state_dict(), OUTPUT_DIR / f"best_{Config.ARCHITECTURE}.pth")

        scheduler.step()

    return model, history


def compute_fabric_metrics(image):
    """Extract FabriSense CV features from fabric image."""
    sample = image.copy().resize((256, 256))
    rgb = np.array(sample).astype(np.float32)
    gray = np.array(sample.convert("L")).astype(np.float32)

    # Texture strength
    gx = np.abs(np.diff(gray, axis=1))
    gy = np.abs(np.diff(gray, axis=0))
    texture_strength = ((gx.mean() + gy.mean()) / 2) / 255 * 100

    # Stripe detection via row/column profile variance
    row_strength = np.std(gray.mean(axis=1)) / 255 * 100
    col_strength = np.std(gray.mean(axis=0)) / 255 * 100

    # Sheen detection (high value, low saturation = glossy)
    sheen_scores = []
    for r, g, b in (rgb / 255).reshape(-1, 3)[::64]:
        _, s, v = colorsys.rgb_to_hsv(float(r), float(g), float(b))
        sheen_scores.append(v * (1 - s / 2))
    sheen_score = np.mean(sheen_scores) * 100

    # Edge density for surface detail
    edge_density = ((gx > 18).mean() + (gy > 18).mean()) / 2 * 100

    return {
        "texture": texture_strength,
        "row_strength": row_strength,
        "col_strength": col_strength,
        "sheen": sheen_score,
        "edges": edge_density
    }


def infer_pattern_from_metrics(metrics):
    """Rule-based pattern inference from visual metrics."""
    r, c = metrics["row_strength"], metrics["col_strength"]

    if max(r, c) < 5:
        return "Solid"
    elif c > r * 1.35 and c > 6:
        return "Vertical Stripes"
    elif r > c * 1.35 and r > 6:
        return "Horizontal Stripes"
    elif min(r, c) > 6 and abs(r - c) < 4:
        return "Plaid"
    else:
        return "Textured/Solid"


# ============================================================================
# Utility functions (train_epoch, validate, etc.)
# ============================================================================

def train_epoch(model, loader, criterion, optimizer):
    """Train for one epoch."""
    model.train()
    total_loss, correct, total = 0.0, 0, 0
    device = next(model.parameters()).device

    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        correct += outputs.argmax(1).eq(labels).sum().item()
        total += labels.size(0)

    return total_loss / len(loader), correct / total


def validate(model, loader):
    """Validate and return macro F1 and accuracy."""
    model.eval()
    all_preds, all_labels = [], []
    device = next(model.parameters()).device

    with torch.no_grad():
        for images, labels in loader:
            outputs = model(images.to(device))
            all_preds.extend(outputs.argmax(1).cpu().numpy())
            all_labels.extend(labels.numpy())

    macro_f1 = f1_score(all_labels, all_preds, average='macro')
    accuracy = np.mean(np.array(all_preds) == np.array(all_labels))

    return macro_f1, accuracy


if __name__ == "__main__":
    set_seed(42)
    print("FabriSense - iBUG Fabrics Dataset Solution")
    print(f"Classes: {len(Config.FABRIC_CLASSES)} fabric types")
    print(f"Architecture: {Config.ARCHITECTURE}")