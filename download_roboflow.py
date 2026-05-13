"""
Helper script to download and configure a Roboflow dataset for YOLO11 training
"""

import os
import sys
from pathlib import Path

def download_roboflow_dataset():
    """
    Interactive script to download a Roboflow dataset
    """
    
    print("=" * 70)
    print("Roboflow Dataset Downloader for YOLO11")
    print("=" * 70)
    print()
    
    # Check if roboflow is installed
    try:
        from roboflow import Roboflow
    except ImportError:
        print("❌ Roboflow package not found. Installing...")
        os.system("pip install roboflow")
        try:
            from roboflow import Roboflow
            print("✅ Roboflow installed successfully!")
        except ImportError:
            print("❌ Failed to install roboflow. Please run: pip install roboflow")
            return
    
    print("\n📋 You'll need the following information from your Roboflow project:")
    print("   1. API Key (from Roboflow account settings)")
    print("   2. Workspace name")
    print("   3. Project name")
    print("   4. Version number")
    print()
    print("💡 You can find these in the Roboflow export code snippet")
    print()
    
    # Get user input
    api_key = input("Enter your Roboflow API Key: ").strip()
    workspace = input("Enter your workspace name: ").strip()
    project = input("Enter your project name: ").strip()
    version = input("Enter version number (default: 1): ").strip() or "1"
    
    # Dataset download location
    download_path = input("Enter download location (default: ./datasets): ").strip() or "./datasets"
    
    print("\n" + "=" * 70)
    print("Downloading dataset...")
    print("=" * 70 + "\n")
    
    try:
        # Initialize Roboflow
        rf = Roboflow(api_key=api_key)
        
        # Get project
        project_obj = rf.workspace(workspace).project(project)
        
        # Get version
        version_obj = project_obj.version(int(version))
        
        # Download dataset in YOLOv8 format
        dataset = version_obj.download("yolov8", location=download_path)
        
        print("\n" + "=" * 70)
        print("✅ Dataset downloaded successfully!")
        print("=" * 70)
        print(f"\n📁 Dataset location: {dataset.location}")
        print(f"📄 Data YAML file: {dataset.location}/data.yaml")
        print(f"📊 Classes: {dataset.classes}")
        print(f"🔢 Number of classes: {len(dataset.classes)}")
        
        # Display training command
        print("\n" + "=" * 70)
        print("🚀 Next Steps - Training Command:")
        print("=" * 70)
        print("\nUse this command to train with your Roboflow dataset:\n")
        
        data_yaml_path = Path(dataset.location) / "data.yaml"
        print(f'python train.py --config "cfgs/SOTA Comparison/ours.yaml" --data "{data_yaml_path}" --epochs 100 --batch 8 --device 0')
        
        print("\nOr with YOLO CLI:\n")
        print(f'yolo detect train data="{data_yaml_path}" model="cfgs/SOTA Comparison/ours.yaml" epochs=100 batch=8 device=0')
        
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error downloading dataset: {e}")
        print("\nPlease check:")
        print("  - API key is correct")
        print("  - Workspace and project names are correct")
        print("  - Version number exists")
        print("  - You have internet connection")

def main():
    print("\n")
    download_roboflow_dataset()
    print("\n")

if __name__ == "__main__":
    main()
