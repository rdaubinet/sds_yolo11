# GPU Setup Guide - CUDA-Enabled PyTorch Installation

## 🎮 Your GPU Configuration

- **Primary GPU:** NVIDIA GeForce RTX 3050 Ti Laptop GPU (4 GB VRAM)
- **Driver Version:** 596.36
- **CUDA Version:** 13.2
- **Status:** ✅ Ready for GPU training

## ⚠️ Python 3.14 Limitation

**Issue:** Python 3.14 is too new, and PyTorch doesn't have CUDA-enabled builds for it yet.  
**Solution:** Created a Python 3.12 virtual environment with CUDA support.

## 🔄 Installation in Progress

Currently installing **PyTorch 2.5.1 + CUDA 12.1** in the virtual environment:

```
Location: C:\AUS\0 - Repositories\SurfLink AI\sds_yolo11\venv_cuda\
Python Version: 3.12.2
PyTorch Version: 2.5.1+cu121 (CUDA 12.1)
Download Size: 2.4 GB
```

**Status:** Installation is running in the background terminal

## ✅ How to Use the CUDA Environment

### 1. Activate the Virtual Environment

Every time you want to train with GPU, activate the environment first:

```powershell
cd "C:\AUS\0 - Repositories\SurfLink AI\sds_yolo11"
.\venv_cuda\Scripts\Activate.ps1
```

You'll see `(venv_cuda)` appear in your prompt when activated.

### 2. Verify CUDA Installation (After Download Completes)

```powershell
python -c "import torch; print('PyTorch:', torch.__version__); print('CUDA Available:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"
```

Expected output:
```
PyTorch: 2.5.1+cu121
CUDA Available: True
GPU: NVIDIA GeForce RTX 3050 Ti Laptop GPU
```

### 3. Install Additional Dependencies in the Virtual Environment

Once PyTorch finishes installing, you'll need to install other dependencies:

```powershell
# Make sure venv_cuda is activated
pip install ultralytics opencv-python matplotlib seaborn pandas tqdm pyyaml
```

### 4. Re-run Setup Script in Virtual Environment

```powershell
python setup_project.py
```

This will integrate the custom modules (Space-to-Depth and CARAFE) with the Ultralytics installation in the virtual environment.

## 🚀 Training Commands with GPU

### Using the Training Script

```powershell
# Activate environment first
.\venv_cuda\Scripts\Activate.ps1

# Train with GPU
python train.py --config "cfgs/SOTA Comparison/ours.yaml" --data seadrones_data.yaml --epochs 100 --batch 8 --device 0
```

### Using YOLO CLI

```powershell
# Activate environment first
.\venv_cuda\Scripts\Activate.ps1

# Train with GPU (device 0 = first GPU)
yolo detect train data=seadrones_data.yaml model="cfgs/SOTA Comparison/ours.yaml" epochs=100 device=0
```

## 💡 GPU Memory Management Tips

Your RTX 3050 Ti has **4GB VRAM**, which is limited. Here are optimization tips:

### 1. Reduce Batch Size
```powershell
# Use smaller batch size for 4GB VRAM
python train.py --config "cfgs/SOTA Comparison/ours.yaml" --data seadrones_data.yaml --batch 4
```

### 2. Reduce Image Size
```powershell
# Use smaller input images (default is 640)
python train.py --config "cfgs/SOTA Comparison/ours.yaml" --data seadrones_data.yaml --imgsz 416 --batch 8
```

### 3. Use Smaller Model Variant
```powershell
# Try yolo11n (nano) instead of larger variants
python train.py --config "cfgs/Ablation Study/yolo11.yaml" --data seadrones_data.yaml --pretrained yolo11n.pt
```

### 4. Enable Mixed Precision Training
```powershell
# Use Automatic Mixed Precision to save memory
python train.py --config "cfgs/SOTA Comparison/ours.yaml" --data seadrones_data.yaml --amp
```

## 🔍 Troubleshooting

### "CUDA out of memory" Error

If you get out of memory errors during training:

1. **Reduce batch size:**
   ```powershell
   --batch 2  # or even --batch 1 for very memory-constrained training
   ```

2. **Reduce image size:**
   ```powershell
   --imgsz 320  # smaller images use less memory
   ```

3. **Close other GPU-using applications:**
   - Check GPU usage: `nvidia-smi`
   - Close games, browsers with hardware acceleration, etc.

4. **Use gradient accumulation:**
   ```powershell
   # Simulate larger batch size without using more memory
   python train.py --batch 4 --accumulate 4  # Effective batch size: 16
   ```

### Check GPU Usage During Training

Open a new terminal and run:
```powershell
nvidia-smi -l 1  # Update every 1 second
```

This shows:
- GPU memory usage
- GPU utilization %
- Temperature
- Power consumption

### Verify CUDA is Being Used

After starting training, check that CUDA is detected:
```python
import torch
print(f"Training on: {torch.cuda.get_device_name(0)}")
print(f"Memory allocated: {torch.cuda.memory_allocated(0) / 1024**3:.2f} GB")
print(f"Memory reserved: {torch.cuda.memory_reserved(0) / 1024**3:.2f} GB")
```

## 📊 Expected Performance

With your RTX 3050 Ti (4GB):

| Configuration | Batch Size | Speed (Approx) |
|--------------|------------|----------------|
| YOLO11n (nano) + 640px | 8 | ~15-20 img/s |
| YOLO11n + 416px | 12-16 | ~20-25 img/s |
| YOLO11s (small) + 640px | 4-6 | ~10-15 img/s |
| Enhanced model + 640px | 4-8 | ~10-15 img/s |

*Speeds are estimates and may vary*

## 🔄 Switching Between CPU and GPU

### Use GPU Environment (for training)
```powershell
.\venv_cuda\Scripts\Activate.ps1
python train.py --device 0  # GPU
```

### Use CPU Environment (for testing/debugging)
```powershell
deactivate  # Exit venv if active
python train.py --device cpu
```

### Auto-select Best Device
```powershell
# Ultralytics automatically selects GPU if available
python train.py --device 0  # or leave blank to auto-detect
```

## 📝 Complete Setup Checklist

- [x] GPU detected (RTX 3050 Ti)
- [x] NVIDIA drivers installed (v596.36)
- [x] CUDA 13.2 available
- [x] Python 3.12 virtual environment created
- [ ] **PyTorch CUDA installation (downloading...)**
- [ ] Install Ultralytics in virtual environment
- [ ] Run setup_project.py in virtual environment
- [ ] Test GPU with sample inference
- [ ] Configure dataset paths
- [ ] Start training!

## 🎓 Next Steps (After Installation Completes)

### 1. Check Installation Status

Check if the download/installation is complete:
```powershell
# Look for the terminal that shows the PyTorch installation
# It should say "Successfully installed torch-2.5.1+cu121 torchvision..."
```

### 2. Verify GPU Access

```powershell
.\venv_cuda\Scripts\Activate.ps1
python -c "import torch; print('CUDA:', torch.cuda.is_available())"
```

### 3. Install Remaining Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Run Initial Test

```powershell
python -c "from ultralytics import YOLO; model = YOLO('yolo11n.pt'); model.info(); print('Device:', model.device)"
```

### 5. Start Training

```powershell
# Small test run first
python train.py --config "cfgs/Ablation Study/yolo11.yaml" --data seadrones_data.yaml --epochs 3 --batch 4
```

## 💾 Disk Space Note

The CUDA PyTorch installation requires:
- **Download:** 2.4 GB
- **Installed:** ~3.5 GB
- **Total with dependencies:** ~5-6 GB

Make sure you have sufficient disk space in your user directory.

## 🔗 Useful Commands

### Check Environment Info
```powershell
.\venv_cuda\Scripts\Activate.ps1
python -c "import torch; import sys; print(f'Python: {sys.version}'); print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}'); print(f'cuDNN: {torch.backends.cudnn.version() if torch.cuda.is_available() else None}')"
```

### Deactivate Virtual Environment
```powershell
deactivate
```

### Delete and Recreate (if needed)
```powershell
Remove-Item -Recurse -Force venv_cuda
py -3.12 -m venv venv_cuda
```

---

**Virtual Environment Location:** `C:\AUS\0 - Repositories\SurfLink AI\sds_yolo11\venv_cuda`

**Installation Status:** 🔄 In Progress (downloading PyTorch 2.4 GB)

**Your GPU:** NVIDIA GeForce RTX 3050 Ti (4GB) - Perfect for training YOLO models!
