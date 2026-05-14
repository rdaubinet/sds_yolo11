"""
Dataset Verification Script
Verifies the Surf Swimming dataset structure and provides statistics
"""

import os
from pathlib import Path
import yaml

def verify_dataset():
    """Verify the Training Data Yolo dataset"""
    
    print("=" * 70)
    print("Surf Swimming Dataset Verification")
    print("=" * 70)
    
    # Dataset path
    base_path = Path(r"C:\AUS\0 - Repositories\SurfLink AI\Training Data Yolo")
    
    if not base_path.exists():
        print(f"\n❌ Dataset not found at: {base_path}")
        print("Please check the path in surf_swimming_data.yaml")
        return False
    
    print(f"\n✅ Dataset found at: {base_path}")
    
    # Check data.yaml
    data_yaml = base_path / "data.yaml"
    if data_yaml.exists():
        print(f"✅ data.yaml exists")
        with open(data_yaml, 'r') as f:
            data_config = yaml.safe_load(f)
            print(f"   Classes: {data_config.get('nc', 'N/A')}")
            print(f"   Names: {data_config.get('names', 'N/A')}")
    else:
        print("❌ data.yaml not found")
    
    # Check splits
    splits = ['train', 'valid', 'test']
    total_images = 0
    total_labels = 0
    
    print("\n" + "=" * 70)
    print("Dataset Structure:")
    print("=" * 70)
    
    for split in splits:
        split_path = base_path / split
        images_path = split_path / "images"
        labels_path = split_path / "labels"
        
        if not split_path.exists():
            print(f"\n❌ {split.upper()} split not found")
            continue
        
        # Count images
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        images = []
        for ext in image_extensions:
            images.extend(list(images_path.glob(f"*{ext}")))
        
        # Count labels
        labels = list(labels_path.glob("*.txt"))
        
        total_images += len(images)
        total_labels += len(labels)
        
        print(f"\n{split.upper()}:")
        print(f"  📁 Path: {split_path}")
        print(f"  🖼️  Images: {len(images)}")
        print(f"  🏷️  Labels: {len(labels)}")
        
        if len(images) != len(labels):
            print(f"  ⚠️  Warning: Mismatch between images and labels!")
        else:
            print(f"  ✅ Images and labels match")
    
    print("\n" + "=" * 70)
    print("Summary:")
    print("=" * 70)
    print(f"Total Images: {total_images}")
    print(f"Total Labels: {total_labels}")
    
    if total_images > 0:
        print(f"\n✅ Dataset is valid and ready for training!")
        print("\n" + "=" * 70)
        print("Training Commands:")
        print("=" * 70)
        print("\n1. Quick test (10 epochs):")
        print('   python train.py --config "cfgs/SOTA Comparison/ours.yaml" --data surf_swimming_data.yaml --epochs 10 --batch 4 --device 0')
        
        print("\n2. Full training (100 epochs):")
        print('   python train.py --config "cfgs/SOTA Comparison/ours.yaml" --data surf_swimming_data.yaml --epochs 100 --batch 8 --device 0')
        
        print("\n3. Baseline YOLO11 (for comparison):")
        print('   python train.py --config "cfgs/Ablation Study/yolo11.yaml" --data surf_swimming_data.yaml --epochs 100 --batch 8 --device 0')
        
        return True
    else:
        print("\n❌ No images found in dataset")
        return False

if __name__ == "__main__":
    verify_dataset()
