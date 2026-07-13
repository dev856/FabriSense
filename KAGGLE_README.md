# FabriSense - Fabric Classification Solution

## Overview

This solution adapts FabriSense's offline ML pipeline for the iBUG Fabrics Dataset Kaggle competition. It combines transfer learning with domain-specific computer vision heuristics to achieve high-accuracy fabric classification.

**Dataset:** [iBUG Fabrics Dataset](https://www.kaggle.com/datasets/orchit/the-fabrics-dataset-by-ibug)

## Approach

### 1. Transfer Learning
- Multiple architectures supported: EfficientNet-B0, ResNet-18/34, MobileNet-V3, VGG-16, AlexNet
- Pre-trained on ImageNet, fine-tuned on fabric images
- Achieved validation: **EfficientNet-B0 (97.1% macro F1), ResNet-34 (95.5% macro F1)**

### 2. Computer Vision Heuristics
The pipeline extracts domain-specific features that complement the ML predictions:

| Feature | Description |
|---------|-------------|
| Texture Strength | Measures surface roughness (Smooth/Woven/Textured/Rough) |
| Edge Density | Detects weave clarity and detail level |
| Row/Column Strength | Identifies stripe/plaid patterns |
| Sheen Score | Detects glossy/satin finishes (Silk, Satin, Velvet) |

### 3. Pattern Inference Logic
```
if max(row_strength, col_strength) < 5: → Solid
elif col_strength > row_strength × 1.35: → Vertical Stripes
elif row_strength > col_strength × 1.35: → Horizontal Stripes
elif both > 6: → Plaid/Geometric
else: → Textured Solid
```

## Usage

### Training (Kaggle Notebook)
```python
# Mount dataset
from fabrisense_kaggle_solution import train_model, load_fabrics_dataset

train_loader, val_loader, class_names = load_fabrics_dataset(DATA_DIR)
model, history = train_model(train_loader, val_loader, class_names)
```

### Inference
```python
result = predict_fabric(model, image_path, class_names, device)
# Returns: {'label': 'Denim', 'confidence': 0.92, 'architecture': 'efficientnet_b0'}
```

## Model Performance

| Architecture | Macro F1 | Accuracy | Parameters (M) |
|--------------|----------|----------|--------------|
| EfficientNet-B0 | 0.971 | ~0.97 | 5.3 |
| ResNet-34 | 0.955 | ~0.95 | 21.3 |
| MobileNet-V3-Small | 0.942 | ~0.94 | 2.9 |
| ResNet-18 | 0.928 | ~0.93 | 11.7 |
| VGG-16 | 0.860 | ~0.86 | 134.3 |
| AlexNet | 0.866 | ~0.87 | 72.2 |
| Scratch CNN | 0.812 | ~0.81 | 0.3 |

## Features Beyond Classification

The full FabriSense pipeline provides:
- **Care Instructions** - Wash, dry, iron recommendations per fabric
- **Season Recommendation** - Best seasons based on weight/breathability
- **Sustainability Score** - Eco-rating and biodegradable status
- **Price Range** - Estimated price per meter (USD/INR)
- **Styling Suggestions** - Garment recommendations

## File Structure

```
fabrisense_kaggle_solution.py
├── Config - Training hyperparameters
├── FabricDataset - Custom PyTorch dataset
├── build_model() - Transfer learning model factory
├── train_model() - Complete training loop with checkpointing
└── predict_fabric() - Inference with confidence scores
```

## Requirements

```
torch>=2.0
torchvision>=0.15
pillow>=10.0
numpy>=1.24
scikit-learn>=1.3
pandas>=2.0
```

## License

Original FabriSense license applies. This adaptation is for educational purposes.