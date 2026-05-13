"""
Training script for Enhanced YOLO11 Maritime Search & Rescue
This script provides a convenient way to train models with the custom configurations
"""

import argparse
from pathlib import Path
from ultralytics import YOLO

def train_model(
    config_path: str,
    data_path: str,
    epochs: int = 100,
    batch_size: int = 16,
    imgsz: int = 640,
    device: str = '0',
    project: str = 'runs/train',
    name: str = 'exp',
    pretrained: str = 'yolo11n.pt',
    **kwargs
):
    """
    Train a YOLO11 model with custom configuration
    
    Args:
        config_path: Path to model configuration YAML file
        data_path: Path to data configuration YAML file
        epochs: Number of training epochs
        batch_size: Batch size for training
        imgsz: Input image size
        device: Device to use (cuda device, i.e. 0 or 0,1,2,3 or cpu)
        project: Project directory name
        name: Experiment name
        pretrained: Path to pretrained weights or model name
        **kwargs: Additional arguments to pass to model.train()
    """
    
    print("=" * 70)
    print("Enhanced YOLO11 Maritime Search & Rescue - Training")
    print("=" * 70)
    print(f"\n📋 Configuration:")
    print(f"   Model Config: {config_path}")
    print(f"   Data Config:  {data_path}")
    print(f"   Epochs:       {epochs}")
    print(f"   Batch Size:   {batch_size}")
    print(f"   Image Size:   {imgsz}")
    print(f"   Device:       {device}")
    print(f"   Pretrained:   {pretrained}")
    print("\n" + "=" * 70 + "\n")
    
    # Load model
    if Path(pretrained).exists():
        print(f"Loading pretrained model from {pretrained}")
        model = YOLO(pretrained)
    else:
        print(f"Loading pretrained model: {pretrained}")
        model = YOLO(pretrained)
    
    # Start training
    results = model.train(
        data=data_path,
        cfg=config_path,
        epochs=epochs,
        batch=batch_size,
        imgsz=imgsz,
        device=device,
        project=project,
        name=name,
        **kwargs
    )
    
    print("\n" + "=" * 70)
    print("✅ Training completed!")
    print("=" * 70)
    print(f"\nResults saved to: {results.save_dir}")
    print(f"Best model: {results.save_dir / 'weights' / 'best.pt'}")
    print(f"Last model: {results.save_dir / 'weights' / 'last.pt'}")
    
    return results

def main():
    parser = argparse.ArgumentParser(
        description='Train Enhanced YOLO11 for Maritime Search & Rescue',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Required arguments
    parser.add_argument(
        '--config',
        type=str,
        required=True,
        help='Path to model configuration YAML file (e.g., cfgs/SOTA Comparison/ours.yaml)'
    )
    
    parser.add_argument(
        '--data',
        type=str,
        default='seadrones_data.yaml',
        help='Path to data configuration YAML file'
    )
    
    # Training parameters
    parser.add_argument('--epochs', type=int, default=100, help='Number of epochs')
    parser.add_argument('--batch', type=int, default=16, help='Batch size')
    parser.add_argument('--imgsz', type=int, default=640, help='Input image size')
    parser.add_argument('--device', type=str, default='0', help='Device (cuda device or cpu)')
    
    # Pretrained weights
    parser.add_argument(
        '--pretrained',
        type=str,
        default='yolo11n.pt',
        help='Pretrained weights path or model name (yolo11n.pt, yolo11s.pt, etc.)'
    )
    
    # Output directories
    parser.add_argument('--project', type=str, default='runs/train', help='Project directory')
    parser.add_argument('--name', type=str, default='exp', help='Experiment name')
    
    # Additional training arguments
    parser.add_argument('--workers', type=int, default=8, help='Number of worker threads')
    parser.add_argument('--patience', type=int, default=50, help='Early stopping patience')
    parser.add_argument('--save-period', type=int, default=-1, help='Save checkpoint every x epochs')
    parser.add_argument('--resume', action='store_true', help='Resume training from last checkpoint')
    parser.add_argument('--amp', action='store_true', help='Use Automatic Mixed Precision')
    
    # Optimization
    parser.add_argument('--optimizer', type=str, default='auto', help='Optimizer (auto, SGD, Adam, AdamW)')
    parser.add_argument('--lr0', type=float, default=0.01, help='Initial learning rate')
    parser.add_argument('--lrf', type=float, default=0.01, help='Final learning rate factor')
    
    args = parser.parse_args()
    
    # Validate paths
    if not Path(args.config).exists():
        raise FileNotFoundError(f"Config file not found: {args.config}")
    
    if not Path(args.data).exists():
        raise FileNotFoundError(f"Data file not found: {args.data}")
    
    # Additional kwargs
    kwargs = {
        'workers': args.workers,
        'patience': args.patience,
        'save_period': args.save_period,
        'resume': args.resume,
        'amp': args.amp,
        'optimizer': args.optimizer,
        'lr0': args.lr0,
        'lrf': args.lrf,
    }
    
    # Train model
    train_model(
        config_path=args.config,
        data_path=args.data,
        epochs=args.epochs,
        batch_size=args.batch,
        imgsz=args.imgsz,
        device=args.device,
        project=args.project,
        name=args.name,
        pretrained=args.pretrained,
        **kwargs
    )

if __name__ == '__main__':
    main()
