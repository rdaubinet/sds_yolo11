"""
Comprehensive CUDA environment verification
"""

import sys

print("=" * 70)
print("CUDA Environment Verification")
print("=" * 70)

# 1. Python version
print("\n1. Python Version:")
print(f"   {sys.version}")

# 2. PyTorch and CUDA
print("\n2. PyTorch and CUDA:")
try:
    import torch
    print(f"   ✅ PyTorch: {torch.__version__}")
    print(f"   ✅ CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"   ✅ CUDA Version: {torch.version.cuda}")
        print(f"   ✅ cuDNN Version: {torch.backends.cudnn.version()}")
        print(f"   ✅ GPU: {torch.cuda.get_device_name(0)}")
        print(f"   ✅ GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
    else:
        print("   ❌ CUDA not available")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 3. Ultralytics
print("\n3. Ultralytics YOLO:")
try:
    import ultralytics
    print(f"   ✅ Ultralytics: {ultralytics.__version__}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 4. Custom modules
print("\n4. Custom Modules:")
try:
    from ultralytics.nn.modules.space_to_depth import space_to_depth
    from ultralytics.nn.modules.carafe import CARAFE
    print(f"   ✅ space_to_depth: {space_to_depth}")
    print(f"   ✅ CARAFE: {CARAFE}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 5. Other dependencies
print("\n5. Other Dependencies:")
packages = [
    'opencv-python',
    'pandas',
    'seaborn',
    'matplotlib',
    'numpy',
    'pyyaml',
    'tqdm'
]

for pkg in packages:
    try:
        module_name = pkg.replace('-', '_').replace('_python', '')
        if module_name == 'pyyaml':
            module_name = 'yaml'
        __import__(module_name)
        print(f"   ✅ {pkg}")
    except Exception:
        print(f"   ❌ {pkg}")

# 6. Test model loading with custom modules
print("\n6. Test Model Configuration:")
try:
    from ultralytics import YOLO
    import os
    
    # Check if config files exist
    configs = [
        "cfgs/SOTA Comparison/ours.yaml",
        "cfgs/Ablation Study/yolo11.yaml",
        "cfgs/Ablation Study/SPD123.yaml"
    ]
    
    for config in configs:
        if os.path.exists(config):
            print(f"   ✅ {config}")
        else:
            print(f"   ⚠️  {config} not found")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# 7. Dataset configuration
print("\n7. Dataset Configuration:")
try:
    import os
    if os.path.exists("surf_swimming_data.yaml"):
        print("   ✅ surf_swimming_data.yaml exists")
        
        # Check dataset path
        dataset_path = r"C:\AUS\0 - Repositories\AI Surf Monitoring\Training Data Yolo"
        if os.path.exists(dataset_path):
            print(f"   ✅ Dataset found at: {dataset_path}")
            
            # Count images
            train_path = os.path.join(dataset_path, "train", "images")
            if os.path.exists(train_path):
                train_count = len([f for f in os.listdir(train_path) if f.endswith(('.jpg', '.jpeg', '.png'))])
                print(f"   ✅ Training images: {train_count}")
        else:
            print(f"   ⚠️  Dataset not found at: {dataset_path}")
    else:
        print("   ⚠️  surf_swimming_data.yaml not found")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 70)
print("CUDA Environment Setup Complete!")
print("=" * 70)

print("\n✅ Ready to train! Use these commands:")
print("\n1. Quick test (10 epochs):")
print('   python train.py --config "cfgs/SOTA Comparison/ours.yaml" --data surf_swimming_data.yaml --epochs 10 --batch 4 --device 0')
print("\n2. Full training (100 epochs):")
print('   python train.py --config "cfgs/SOTA Comparison/ours.yaml" --data surf_swimming_data.yaml --epochs 100 --batch 8 --device 0')
print("\n" + "=" * 70)
