# Surf Swimming Detection - Training Guide

## 📊 Dataset Overview

**Dataset:** Surf Swimming Detection (Roboflow)
- **Classes:** 1 (person - surf swimmers)
- **Training Images:** 9,774
- **Validation Images:** 827
- **Test Images:** 65
- **Total:** 10,666 images
- **License:** CC BY 4.0
- **Source:** https://universe.roboflow.com/renes-workspace-bchun/surf-swimming-ruayv/dataset/1

## ✅ Dataset Status

✅ Dataset verified and ready
✅ All images have corresponding labels
✅ Proper YOLO format structure
✅ Configuration file created: `surf_swimming_data.yaml`

## 🚀 Training Instructions

### Prerequisites

1. **Activate CUDA Environment:**
   ```powershell
   cd "C:\AUS\0 - Repositories\SurfLink AI\sds_yolo11"
   .\venv_cuda\Scripts\Activate.ps1
   ```

2. **Verify Dataset (Optional):**
   ```powershell
   python verify_dataset.py
   ```

### Recommended Training Workflow

#### **Phase 1: Quick Test (Recommended First)**

Test with 10 epochs to ensure everything works:

```powershell
python train.py `
    --config "cfgs/SOTA Comparison/ours.yaml" `
    --data surf_swimming_data.yaml `
    --epochs 10 `
    --batch 4 `
    --device 0
```

**Expected time:** ~30-60 minutes (depending on GPU)
**Purpose:** Verify training pipeline works end-to-end

#### **Phase 2: Baseline Model**

Train baseline YOLO11 for comparison:

```powershell
python train.py `
    --config "cfgs/Ablation Study/yolo11.yaml" `
    --data surf_swimming_data.yaml `
    --epochs 100 `
    --batch 8 `
    --device 0 `
    --name yolo11_baseline
```

**Expected time:** ~5-8 hours
**Purpose:** Establish baseline performance metrics

#### **Phase 3: Enhanced Model (Main)**

Train the enhanced model with SPD and CARAFE:

```powershell
python train.py `
    --config "cfgs/SOTA Comparison/ours.yaml" `
    --data surf_swimming_data.yaml `
    --epochs 100 `
    --batch 8 `
    --device 0 `
    --name enhanced_model
```

**Expected time:** ~5-8 hours
**Purpose:** Achieve best performance with custom modules

#### **Phase 4: Ablation Studies (Optional)**

Test individual components:

**SPD Only:**
```powershell
python train.py `
    --config "cfgs/Ablation Study/SPD123.yaml" `
    --data surf_swimming_data.yaml `
    --epochs 100 `
    --batch 8 `
    --device 0 `
    --name spd_only
```

**CARAFE Only:**
```powershell
python train.py `
    --config "cfgs/Ablation Study/CARAFE123.yaml" `
    --data surf_swimming_data.yaml `
    --epochs 100 `
    --batch 8 `
    --device 0 `
    --name carafe_only
```

## ⚙️ GPU-Specific Settings (RTX 3050 Ti - 4GB VRAM)

### Batch Size Recommendations

| Configuration | Batch Size | Expected Usage |
|--------------|------------|----------------|
| Quick Test (10 epochs) | 4 | ~3.5 GB VRAM |
| Full Training | 8 | ~3.8 GB VRAM |
| If OOM Error | 2-4 | Reduce if needed |

### Memory Optimization

If you encounter "CUDA out of memory" errors:

```powershell
# Option 1: Reduce batch size
python train.py --config "cfgs/SOTA Comparison/ours.yaml" --data surf_swimming_data.yaml --batch 4

# Option 2: Reduce image size
python train.py --config "cfgs/SOTA Comparison/ours.yaml" --data surf_swimming_data.yaml --imgsz 512 --batch 8

# Option 3: Enable mixed precision (FP16)
python train.py --config "cfgs/SOTA Comparison/ours.yaml" --data surf_swimming_data.yaml --amp
```

## 📈 Monitoring Training

### Using TensorBoard (Optional)

```powershell
# Install tensorboard if not already installed
pip install tensorboard

# View training metrics in real-time
tensorboard --logdir runs/train
```

Then open: http://localhost:6006

### Training Outputs

Results are saved to: `runs/train/exp*/`
- `weights/best.pt` - Best model based on validation mAP
- `weights/last.pt` - Most recent checkpoint
- `results.png` - Training/validation metrics plots
- `confusion_matrix.png` - Confusion matrix
- `F1_curve.png` - F1 score curve
- `PR_curve.png` - Precision-Recall curve
- `P_curve.png` - Precision curve
- `R_curve.png` - Recall curve

## 🔍 Validation & Testing

### Validate on Validation Set

```powershell
yolo detect val model=runs/train/enhanced_model/weights/best.pt data=surf_swimming_data.yaml
```

### Test on Test Set

```powershell
yolo detect val model=runs/train/enhanced_model/weights/best.pt data=surf_swimming_data.yaml split=test
```

### Run Inference on New Images

```powershell
# Single image
yolo detect predict model=runs/train/enhanced_model/weights/best.pt source=path/to/image.jpg

# Folder of images
yolo detect predict model=runs/train/enhanced_model/weights/best.pt source=path/to/images/

# Video
yolo detect predict model=runs/train/enhanced_model/weights/best.pt source=path/to/video.mp4

# Webcam
yolo detect predict model=runs/train/enhanced_model/weights/best.pt source=0
```

## 📊 Expected Performance Metrics

Based on maritime SAR datasets, you can expect:

### Baseline YOLO11:
- **mAP@0.5:** ~75-85%
- **mAP@0.5:0.95:** ~50-60%
- **Inference Time:** ~8-12ms per image

### Enhanced Model (SPD + CARAFE):
- **mAP@0.5:** ~80-90% (+5-10% improvement)
- **mAP@0.5:0.95:** ~55-65% (+5% improvement)
- **Inference Time:** ~10-15ms per image

*Note: Actual results depend on dataset quality and training parameters*

## 💡 Training Tips for Surf Swimming Detection

### 1. Data Augmentation

Your dataset is fairly large (9,774 training images), but additional augmentation can help:

```powershell
python train.py `
    --config "cfgs/SOTA Comparison/ours.yaml" `
    --data surf_swimming_data.yaml `
    --epochs 100 `
    --batch 8 `
    --hsv_h 0.015 `
    --hsv_s 0.7 `
    --hsv_v 0.4 `
    --degrees 10 `
    --translate 0.1 `
    --scale 0.5 `
    --fliplr 0.5 `
    --mosaic 1.0
```

### 2. Learning Rate Scheduling

For fine-tuning or if training plateaus:

```powershell
python train.py `
    --config "cfgs/SOTA Comparison/ours.yaml" `
    --data surf_swimming_data.yaml `
    --epochs 100 `
    --lr0 0.001 `
    --lrf 0.01
```

### 3. Resume Training

If training is interrupted:

```powershell
python train.py --resume runs/train/enhanced_model/weights/last.pt
```

## 🎯 Use Case: Surf Monitoring

This model is optimized for detecting people (swimmers/surfers) in maritime/surf environments:

- **Typical Scenarios:** Beach monitoring, surf safety, swimmer tracking
- **Advantages of Enhanced Model:**
  - **SPD Module:** Better detection of small/distant swimmers
  - **CARAFE Module:** Improved feature resolution for water conditions
  - **Lightweight:** Fast enough for real-time monitoring

### Deployment Considerations

**Real-time Beach Monitoring:**
```powershell
# Export to ONNX for deployment
yolo export model=runs/train/enhanced_model/weights/best.pt format=onnx

# Export to TensorRT (for NVIDIA devices)
yolo export model=runs/train/enhanced_model/weights/best.pt format=engine device=0
```

## 🆘 Troubleshooting

### Issue: Training is very slow
**Solutions:**
1. Check GPU is being used: `nvidia-smi` in terminal
2. Increase batch size if VRAM allows
3. Reduce workers: `--workers 4`
4. Close other GPU-intensive applications

### Issue: Low mAP scores
**Solutions:**
1. Train for more epochs (150-200)
2. Adjust confidence threshold during validation
3. Review data augmentation parameters
4. Check for label quality issues

### Issue: Model overfitting
**Symptoms:** Train metrics much better than validation
**Solutions:**
1. Increase data augmentation
2. Add dropout (modify config YAML)
3. Reduce model complexity
4. Use early stopping

## 📚 Next Steps After Training

1. **Compare Models:** Compare baseline vs enhanced model performance
2. **Error Analysis:** Review false positives/negatives
3. **Optimize for Deployment:** Export to production format (ONNX, TensorRT)
4. **Real-world Testing:** Test on actual surf monitoring footage
5. **Documentation:** Document performance metrics and findings

## 🔗 Useful Commands Reference

```powershell
# Verify dataset
python verify_dataset.py

# Quick test training
python train.py --config "cfgs/SOTA Comparison/ours.yaml" --data surf_swimming_data.yaml --epochs 10 --batch 4 --device 0

# Full training
python train.py --config "cfgs/SOTA Comparison/ours.yaml" --data surf_swimming_data.yaml --epochs 100 --batch 8 --device 0

# Validate model
yolo detect val model=runs/train/exp/weights/best.pt data=surf_swimming_data.yaml

# Run inference
yolo detect predict model=runs/train/exp/weights/best.pt source=path/to/images/

# Export model
yolo export model=runs/train/exp/weights/best.pt format=onnx

# Resume training
python train.py --resume runs/train/exp/weights/last.pt
```

---

**Ready to Start Training?** Run the quick test first:
```powershell
.\venv_cuda\Scripts\Activate.ps1
python train.py --config "cfgs/SOTA Comparison/ours.yaml" --data surf_swimming_data.yaml --epochs 10 --batch 4 --device 0
```
