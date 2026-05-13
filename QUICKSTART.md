# Quick Start Guide - Enhanced YOLO11 Maritime Search & Rescue

This guide will help you set up and run the Enhanced YOLO11 project for maritime search and rescue object detection.

## 🚀 Quick Setup

### 1. Install Dependencies

First, make sure you have Python 3.8+ installed. Then install the required packages:

```bash
pip install -r requirements.txt
```

### 2. Integrate Custom Modules

Run the automated setup script to integrate Space-to-Depth and CARAFE modules into YOLO11:

```bash
python setup_project.py
```

This script will:
- ✅ Copy custom modules to the Ultralytics YOLO11 installation
- ✅ Update the necessary configuration files
- ✅ Create backups of modified files

### 3. Download Dataset (Optional)

If you want to train models on the maritime search and rescue dataset:

1. Download the SeaDronesSee dataset from: [Download Link](https://cloud.cs.uni-tuebingen.de/index.php/s/aJQPHLGnke68M52)
2. Extract the dataset to a directory
3. Prepare the dataset in YOLO format (images + labels)

For more details, visit the official website: [https://macvi.org/](https://macvi.org/)

## 📁 Project Structure

```
sds_yolo11/
├── code/                       # Custom modules
│   ├── space_to_depth.py      # Space-to-Depth (SPD) module
│   └── carafe.py              # CARAFE upsampling module
├── cfgs/                      # Model configurations
│   ├── Ablation Study/        # Ablation study configs
│   │   ├── yolo11.yaml       # Baseline YOLO11
│   │   ├── SPD*.yaml         # SPD variants
│   │   ├── CARAFE*.yaml      # CARAFE variants
│   │   └── SFI.yaml          # Feature integration variant
│   └── SOTA Comparison/       # State-of-the-art comparison
│       └── ours.yaml         # Proposed enhanced model
├── requirements.txt           # Python dependencies
├── setup_project.py          # Automated setup script
├── QUICKSTART.md             # This file
└── README.md                 # Original project README

## 🎯 Usage Examples

### Training a Model

Use any of the configuration files in the `cfgs/` directory:

**Train with the proposed enhanced model:**
```bash
yolo detect train data=path/to/seadrones.yaml model=cfgs/SOTA\ Comparison/ours.yaml epochs=100 imgsz=640
```

**Train with baseline YOLO11:**
```bash
yolo detect train data=path/to/seadrones.yaml model=cfgs/Ablation\ Study/yolo11.yaml epochs=100 imgsz=640
```

**Train with Space-to-Depth variants:**
```bash
yolo detect train data=path/to/seadrones.yaml model=cfgs/Ablation\ Study/SPD123.yaml epochs=100 imgsz=640
```

### Running Inference

**On images:**
```bash
yolo detect predict model=path/to/best.pt source=path/to/images/
```

**On video:**
```bash
yolo detect predict model=path/to/best.pt source=path/to/video.mp4
```

**With confidence threshold:**
```bash
yolo detect predict model=path/to/best.pt source=path/to/images/ conf=0.5
```

### Validation

```bash
yolo detect val model=path/to/best.pt data=path/to/seadrones.yaml
```

## 🔬 Model Configurations Explained

### Ablation Study Configs

These configurations help understand the impact of each module:

- `yolo11.yaml` - Baseline YOLO11 model
- `SPD1.yaml`, `SPD12.yaml`, `SPD123.yaml`, `SPD1234.yaml` - Progressive addition of Space-to-Depth modules
- `CARAFE1.yaml`, `CARAFE12.yaml`, `CARAFE123.yaml`, `CARAFE23.yaml` - CARAFE upsampling variants
- `SFI.yaml` - Spatial Feature Integration variant

### SOTA Comparison

- `ours.yaml` - The complete proposed enhanced YOLO11 model with all optimizations

## 🛠️ Manual Integration (If Setup Script Fails)

If the automatic setup script encounters issues, follow these manual steps:

### Space-to-Depth Module

1. Copy `code/space_to_depth.py` to `<ultralytics_path>/nn/modules/`
2. Edit `<ultralytics_path>/nn/tasks.py`:
   - Add import: `from ultralytics.nn.modules.space_to_depth import space_to_depth`
   - In the `parse_model` function, add:
     ```python
     elif m is space_to_depth:
         c2 = 4 * ch[f]
     ```

### CARAFE Module

1. Copy `code/carafe.py` to `<ultralytics_path>/nn/modules/`
2. Edit `<ultralytics_path>/nn/tasks.py`:
   - Add import: `from ultralytics.nn.modules.carafe import CARAFE`

### Update Module Exports

Edit `<ultralytics_path>/nn/modules/__init__.py`:
- Add: `from .space_to_depth import space_to_depth`
- Add: `from .carafe import CARAFE`
- Add both to the `__all__` list

## 📊 Dataset Preparation

The SeaDronesSee dataset should be structured in YOLO format:

```
dataset/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
└── labels/
    ├── train/
    ├── val/
    └── test/
```

Create a `seadrones.yaml` data configuration file:

```yaml
path: path/to/dataset  # dataset root dir
train: images/train    # train images (relative to 'path')
val: images/val        # val images (relative to 'path')
test: images/test      # test images (optional)

# Classes
names:
  0: swimmer
  1: boat
  2: jetski
  3: life_saving_appliances
  4: buoy
```

## 🎓 Research Context

This project implements enhancements to YOLO11 specifically for:
- ✈️ Drone-based detection
- 🌊 Maritime environments
- 🆘 Search and rescue operations
- ⚡ Lightweight model requirements
- 🎯 Small object detection

The enhancements include:
- **Space-to-Depth (SPD)**: Better handling of small objects and low-resolution images
- **CARAFE**: Content-aware feature upsampling for better feature reconstruction

## 📝 References

- **Space-to-Depth**: Sunkara et al., "No More Strided Convolutions or Pooling: A New CNN Building Block for Low-Resolution Images and Small Objects"
- **CARAFE**: Wang et al., "CARAFE: Content-Aware ReAssembly of FEatures"
- **YOLO11**: Ultralytics YOLO11 framework

## 🐛 Troubleshooting

### Module Import Errors

If you get import errors:
```python
ImportError: cannot import name 'space_to_depth'
```

Solution:
1. Verify the module files are copied to the correct location
2. Check that `__init__.py` is updated
3. Try reinstalling ultralytics: `pip install --upgrade --force-reinstall ultralytics`

### CUDA/GPU Issues

If you encounter GPU-related errors:
```bash
# Check PyTorch CUDA availability
python -c "import torch; print(torch.cuda.is_available())"

# Reinstall PyTorch with CUDA support
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Configuration File Errors

If YAML config files throw errors:
- Make sure custom modules are properly integrated
- Verify the syntax in the YAML file
- Check that all referenced modules exist

## 💡 Tips for Best Results

1. **Start with pretrained weights**: Use YOLO11 pretrained models as a starting point
2. **Adjust hyperparameters**: Tune learning rate, batch size, and augmentation for your specific use case
3. **Monitor training**: Use TensorBoard or Weights & Biases for tracking
4. **Validate regularly**: Check validation metrics to avoid overfitting
5. **Use appropriate image size**: 640x640 is the standard, but you can experiment

## 📞 Support

For issues related to:
- **This project**: Check the original repository issues
- **YOLO11/Ultralytics**: Visit [Ultralytics GitHub](https://github.com/ultralytics/ultralytics)
- **SeaDronesSee dataset**: Visit [MacVi website](https://macvi.org/)

## ⚖️ License

Please refer to the original repository and dataset licenses for usage terms.
