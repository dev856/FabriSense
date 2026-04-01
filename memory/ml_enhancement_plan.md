# ML Model Enhancement Plan for FabriSense

## Current State Analysis
- Existing models: Scratch CNN and ResNet18 variants stored in `artifacts/`
- Current pipeline: Image preprocessing → Color extraction → (Potential) ML classification
- Dependencies: scikit-learn, PyTorch (implied by .pt files), OpenCV, Pillow

## Enhancement Goals
1. Improve fabric classification accuracy beyond basic color/texture features
2. Enable multi-label classification (fabric type, pattern, weave, etc.)
3. Reduce model inference time for real-time applications
4. Add uncertainty quantification for predictions
5. Implement continual learning for new fabric types

## Specific Enhancements

### 1. Architecture Improvements
- Replace scratch CNN with EfficientNet-B0 or MobileNetV3 for better accuracy/size tradeoff
- Implement attention mechanisms (CBAM or SE blocks) to focus on fabric-relevant regions
- Add multi-scale feature extraction for capturing both fine textures and overall patterns
- Consider vision transformers (ViT-Tiny) for long-range dependency modeling

### 2. Data Enhancement
- Implement advanced augmentation:
  * Fabric-specific distortions (weave simulation, thread-level noise)
  * Lighting condition simulation (directional, diffuse, mixed illuminants)
  * Realistic wrinkling and draping simulation
- Generate synthetic fabric datasets using GANs or diffusion models
- Implement active learning to prioritize labeling of ambiguous samples

### 3. Training Strategy
- Use hierarchical classification:
  * Level 1: Fabric family (cotton, silk, synthetic, wool)
  * Level 2: Specific type (jersey, denim, chiffon, etc.)
  * Level 3: Pattern/weave characteristics
- Implement contrastive learning for better feature separation
- Use mixed precision training and gradient accumulation for larger effective batch sizes
- Add label smoothing and focal loss to handle class imbalance

### 4. Model Optimization
- Quantize models to INT8 for 4x speedup with minimal accuracy loss
- Implement model distillation to create smaller student models
- Use tensorRT or ONNX runtime for optimized inference
- Add early exiting mechanisms for easy-to-classify samples

### 5. Uncertainty & Reliability
- Implement Monte Carlo Dropout for uncertainty estimation
- Add out-of-distribution detection using Mahalanobis distance in feature space
- Calibrate prediction probabilities using temperature scaling
- Implement rejection option for low-confidence predictions

### 6. Evaluation & Monitoring
- Create comprehensive test set with diverse lighting, backgrounds, and fabric conditions
- Measure accuracy per fabric type and failure mode analysis
- Track concept drift in production with statistical process control
- Implement A/B testing framework for model updates

### 7. Integration Points
- Modify `src/image_preprocessor.py` to output features compatible with new models
- Update color extraction to work alongside deep features (early/late fusion)
- Create model serving interface in `ui/pages.py` for batch and real-time modes
- Add model metadata tracking (version, training data, metrics) to session state

## Implementation Priority
1. Baseline: EfficientNet-B0 with fabric-specific augmentation
2. Intermediate: Add attention and hierarchical classification
3. Advanced: Uncertainty quantification and model optimization
4. Research: Continual learning and synthetic data generation

## Required Dependencies Additions
- torch>=2.0.0, torchvision>=0.15.0
- timm>=0.9.0 (for EfficientNet/Vision Transformer)
- albumentations>=1.3.0 (for advanced augmentation)
- scikit-learn>=1.5.0 (already present)
- onnxruntime>=1.15.0 (for optimization)