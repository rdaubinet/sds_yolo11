# Using Roboflow Datasets with Enhanced YOLO11

This guide explains how to use datasets from Roboflow with the Enhanced YOLO11 Maritime Search & Rescue project.

## 🎯 Why Roboflow?

- ✅ Exports directly in YOLO format
- ✅ Built-in data augmentation and preprocessing
- ✅ Easy dataset versioning
- ✅ Automatic train/val/test splits
- ✅ Free tier available for small projects
- ✅ Provides data.yaml file automatically

## 📥 Method 1: Automated Download (Recommended)

### Step 1: Run the Download Script

```powershell
# Activate your virtual environment first
.\venv_cuda\Scripts\Activate.ps1

# Run the download script
python download_roboflow.py
```

### Step 2: Follow the Prompts

The script will ask for:
- **API Key**: From your Roboflow account settings
- **Workspace name**: Your Roboflow workspace
- **Project name**: Your project name
- **Version number**: Dataset version (usually 1)
- **Download location**: Where to save (default: ./datasets)

### Step 3: The script will automatically:
- Install the Roboflow package if needed
- Download your dataset in YOLO format
- Show you the exact training command to use

## 📥 Method 2: Manual Download

### Step 1: Export from Roboflow Website

1. Go to your Roboflow project
2. Click **"Export Dataset"**
3. Select **"YOLO v8"** or **"YOLO v11"** format
4. Choose **"show download code"** or **"download zip"**

### Step 2: Option A - Using Roboflow Python API

```python
from roboflow import Roboflow

# Install roboflow first: pip install roboflow

rf = Roboflow(api_key="YOUR_API_KEY")
project = rf.workspace("workspace-name").project("project-name")
version = project.version(1)
dataset = version.download("yolov8", location="./datasets")
```

### Step 2: Option B - Download ZIP

1. Download the ZIP file from Roboflow
2. Extract to `./datasets/your_dataset_name/`
3. The structure will be:
   ```
   datasets/your_dataset_name/
   ├── data.yaml          # Roboflow provides this
   ├── train/
   │   ├── images/
   │   └── labels/
   ├── valid/
   │   ├── images/
   │   └── labels/
   └── test/              # Optional
       ├── images/
       └── labels/
   ```

## 🔧 Configuration

### Option 1: Use Roboflow's data.yaml (Easiest)

Roboflow automatically generates a `data.yaml` file. Just point to it:

```powershell
python train.py --config "cfgs/SOTA Comparison/ours.yaml" --data "./datasets/your_dataset/data.yaml" --epochs 100
```

### Option 2: Create Custom Configuration

Use the provided `roboflow_data.yaml` template:

1. Open `roboflow_data.yaml`
2. Update:
   - `path`: Path to your dataset folder
   - `nc`: Number of classes in your dataset
   - `names`: List of class names
3. Save and use in training

Example for a 3-class dataset:

```yaml
path: ./datasets/my_roboflow_dataset
train: train/images  
val: valid/images
nc: 3
names:
  0: person
  1: vehicle
  2: boat
```

## 🚀 Training with Roboflow Dataset

### Using the Training Script

```powershell
# Activate environment
.\venv_cuda\Scripts\Activate.ps1

# Train with Roboflow dataset
python train.py \
    --config "cfgs/SOTA Comparison/ours.yaml" \
    --data "./datasets/your_dataset/data.yaml" \
    --epochs 100 \
    --batch 8 \
    --device 0
```

### Using YOLO CLI

```powershell
yolo detect train \
    data="./datasets/your_dataset/data.yaml" \
    model="cfgs/SOTA Comparison/ours.yaml" \
    epochs=100 \
    batch=8 \
    device=0
```

### Quick Test (10 epochs)

```powershell
python train.py \
    --config "cfgs/SOTA Comparison/ours.yaml" \
    --data "./datasets/your_dataset/data.yaml" \
    --epochs 10 \
    --batch 4 \
    --device 0
```

## 🔍 Verifying Your Dataset

### Check Dataset Structure

```powershell
# List dataset contents
Get-ChildItem -Recurse "./datasets/your_dataset" -Directory

# Count images in train set
(Get-ChildItem "./datasets/your_dataset/train/images/*.jpg").Count

# Check data.yaml content
Get-Content "./datasets/your_dataset/data.yaml"
```

### Verify with Python

```python
import yaml
from pathlib import Path

# Load data.yaml
with open('./datasets/your_dataset/data.yaml', 'r') as f:
    data = yaml.safe_load(f)

print(f"Classes: {data['nc']}")
print(f"Names: {data['names']}")
print(f"Train path: {data['train']}")
print(f"Val path: {data['val']}")
```

## 💡 Tips for Roboflow Datasets

### 1. Dataset Size Considerations
- **RTX 3050 Ti (4GB VRAM)**: Use batch size 4-8
- **Small datasets (<1000 images)**: Use more augmentation
- **Large datasets (>10,000 images)**: Can reduce augmentation

### 2. Data Augmentation
Roboflow applies augmentation during export. You can add more in training:

```powershell
python train.py \
    --config "cfgs/SOTA Comparison/ours.yaml" \
    --data "./datasets/your_dataset/data.yaml" \
    --epochs 100 \
    --hsv_h 0.015 \
    --hsv_s 0.7 \
    --hsv_v 0.4 \
    --degrees 10 \
    --translate 0.1 \
    --scale 0.5 \
    --fliplr 0.5
```

### 3. Maritime-Specific Datasets
If your Roboflow dataset is maritime-related:
- The SPD and CARAFE modules should work well
- Consider using the "ours.yaml" configuration (optimized for maritime)
- Test with different image sizes (640, 1280)

### 4. Class Imbalance
If some classes have very few examples:
- Use more augmentation for those classes in Roboflow
- Consider class weights in training
- Generate more synthetic examples

## 🎓 Example Workflow

```powershell
# 1. Activate environment
.\venv_cuda\Scripts\Activate.ps1

# 2. Download dataset using the helper script
python download_roboflow.py

# 3. Verify download
Get-Content "./datasets/your_dataset/data.yaml"

# 4. Quick test (10 epochs)
python train.py --config "cfgs/SOTA Comparison/ours.yaml" --data "./datasets/your_dataset/data.yaml" --epochs 10 --batch 4

# 5. Full training (if test successful)
python train.py --config "cfgs/SOTA Comparison/ours.yaml" --data "./datasets/your_dataset/data.yaml" --epochs 100 --batch 8

# 6. Evaluate results
yolo detect val model=runs/train/exp/weights/best.pt data="./datasets/your_dataset/data.yaml"

# 7. Run inference
yolo detect predict model=runs/train/exp/weights/best.pt source=path/to/test/images/
```

## 🆘 Troubleshooting

### Issue: "FileNotFoundError: data.yaml not found"
**Solution**: Check the path to your data.yaml file. Use absolute path if needed:
```powershell
$dataPath = Resolve-Path "./datasets/your_dataset/data.yaml"
python train.py --config "cfgs/SOTA Comparison/ours.yaml" --data $dataPath
```

### Issue: "No images found in train/images"
**Solution**: Verify dataset structure. Roboflow exports should have this structure automatically.

### Issue: "CUDA out of memory"
**Solution**: Reduce batch size:
```powershell
python train.py --config "cfgs/SOTA Comparison/ours.yaml" --data "./datasets/your_dataset/data.yaml" --batch 2
```

### Issue: "API Key Invalid"
**Solution**: Get your API key from Roboflow settings: https://app.roboflow.com/settings/api

## 📚 Additional Resources

- **Roboflow Documentation**: https://docs.roboflow.com/
- **Roboflow YOLO Format**: https://roboflow.com/formats/yolov8-pytorch-txt
- **YOLO11 Documentation**: https://docs.ultralytics.com/

## ✅ Summary

1. ✅ You can use ANY Roboflow dataset with this project
2. ✅ Use `download_roboflow.py` for easy setup
3. ✅ Roboflow provides the data.yaml file automatically
4. ✅ All custom modules (SPD, CARAFE) work with any YOLO dataset
5. ✅ Just change the `--data` parameter to your dataset's data.yaml path
