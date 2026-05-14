"""
Train Standard YOLO11 with Milestone Exports
Trains for 100 epochs with automatic exports at epochs 10, 29, and 100
"""

import argparse
from pathlib import Path
from ultralytics import YOLO
import torch
from datetime import datetime
import shutil

class MilestoneExporter:
    """Handles exports at specific epoch milestones"""
    
    def __init__(self, milestones=[10, 29, 100], export_format='engine'):
        self.milestones = milestones
        self.export_format = export_format
        self.exported_epochs = set()
    
    def on_train_epoch_end(self, trainer):
        """Called after each training epoch"""
        epoch = trainer.epoch + 1  # Ultralytics uses 0-based indexing
        
        if epoch in self.milestones and epoch not in self.exported_epochs:
            print("\n" + "=" * 70)
            print(f"🎯 MILESTONE REACHED: Epoch {epoch}")
            print("=" * 70)
            
            # Copy best.pt to milestone-specific name
            best_path = Path(trainer.save_dir) / 'weights' / 'best.pt'
            milestone_path = Path(trainer.save_dir) / 'weights' / f'best_epoch_{epoch}.pt'
            
            if best_path.exists():
                shutil.copy2(best_path, milestone_path)
                print(f"📦 Saved checkpoint: {milestone_path}")
                
                # Export to TensorRT
                try:
                    print(f"\n🔄 Exporting epoch {epoch} model to {self.export_format.upper()}...")
                    model = YOLO(str(milestone_path))
                    export_path = model.export(
                        format=self.export_format,
                        imgsz=640,
                        device='0',
                        half=False
                    )
                    print(f"✅ Export successful: {export_path}")
                    
                except Exception as e:
                    print(f"⚠️  Export failed: {e}")
            
            self.exported_epochs.add(epoch)
            print("=" * 70 + "\n")

def train_with_milestones(
    config_path='cfgs/Ablation Study/yolo11.yaml',
    data_path='surf_swimming_data.yaml',
    epochs=100,
    batch_size=4,
    imgsz=640,
    device='0',
    project='runs/train',
    name='yolo11-baseline-100ep',
    milestones=[10, 29, 100],
    resume=False
):
    """
    Train YOLO11 with automatic exports at milestone epochs
    
    Args:
        resume: If True, resume from last checkpoint in the specified run directory
    """
    
    print("=" * 70)
    print("Standard YOLO11 Training with Milestone Exports")
    print("=" * 70)
    print(f"\nConfiguration:")
    print(f"  Model:      {config_path}")
    print(f"  Data:       {data_path}")
    print(f"  Epochs:     {epochs}")
    print(f"  Batch Size: {batch_size}")
    print(f"  Image Size: {imgsz}")
    print(f"  Device:     {device}")
    print(f"  Milestones: {milestones}")
    print(f"  Resume:     {resume}")
    print(f"  Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70 + "\n")
    
    # Check CUDA
    if not torch.cuda.is_available():
        print("⚠️  Warning: CUDA not available!")
        device = 'cpu'
    else:
        print(f"✅ Using GPU: {torch.cuda.get_device_name(0)}\n")
    
    # Load model - check for existing checkpoint if resuming
    if resume:
        # Look for last.pt in the expected run directory
        last_checkpoint = Path(project) / name / 'weights' / 'last.pt'
        if last_checkpoint.exists():
            print(f"🔄 Resuming from checkpoint: {last_checkpoint}")
            model = YOLO(str(last_checkpoint))
        else:
            print(f"⚠️  No checkpoint found at {last_checkpoint}")
            print(f"   Starting fresh training from: {config_path}")
            model = YOLO(config_path)
    else:
        print(f"Loading model from: {config_path}")
        model = YOLO(config_path)
    
    # Create milestone callback
    exporter = MilestoneExporter(milestones=milestones, export_format='engine')
    
    # Add callback
    model.add_callback("on_train_epoch_end", exporter.on_train_epoch_end)
    
    # Start training
    print("\n🚀 Starting training...\n")
    
    results = model.train(
        data=data_path,
        epochs=epochs,
        batch=batch_size,
        imgsz=imgsz,
        device=device,
        project=project,
        name=name,
        patience=50,
        save=True,
        plots=True,
        val=True,
        cache=False,
        workers=8,
        deterministic=True
    )
    
    print("\n" + "=" * 70)
    print("✅ TRAINING COMPLETED!")
    print("=" * 70)
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Results saved to: {results.save_dir}")
    print("\nGenerated Models:")
    
    weights_dir = Path(results.save_dir) / 'weights'
    for epoch in milestones:
        pt_file = weights_dir / f'best_epoch_{epoch}.pt'
        engine_file = weights_dir / f'best_epoch_{epoch}.engine'
        
        print(f"\nEpoch {epoch}:")
        if pt_file.exists():
            print(f"  ✅ PyTorch:  {pt_file}")
        if engine_file.exists():
            print(f"  ✅ TensorRT: {engine_file}")
    
    print("\n" + "=" * 70)
    
    return results

def main():
    parser = argparse.ArgumentParser(description='Train YOLO11 with milestone exports')
    
    parser.add_argument('--config', type=str, default='cfgs/Ablation Study/yolo11.yaml',
                        help='Model configuration file')
    parser.add_argument('--data', type=str, default='surf_swimming_data.yaml',
                        help='Dataset configuration file')
    parser.add_argument('--epochs', type=int, default=100,
                        help='Number of training epochs')
    parser.add_argument('--batch', type=int, default=4,
                        help='Batch size')
    parser.add_argument('--imgsz', type=int, default=640,
                        help='Image size')
    parser.add_argument('--device', type=str, default='0',
                        help='Device (cuda device or cpu)')
    parser.add_argument('--project', type=str, default='runs/train',
                        help='Project directory')
    parser.add_argument('--name', type=str, default='yolo11-baseline-100ep',
                        help='Experiment name')
    parser.add_argument('--milestones', type=int, nargs='+', default=[10, 29, 100],
                        help='Epochs to export models at')
    parser.add_argument('--resume', action='store_true',
                        help='Resume training from last checkpoint')
    
    args = parser.parse_args()
    
    train_with_milestones(
        config_path=args.config,
        data_path=args.data,
        epochs=args.epochs,
        batch_size=args.batch,
        imgsz=args.imgsz,
        device=args.device,
        project=args.project,
        name=args.name,
        milestones=args.milestones,
        resume=args.resume
    )

if __name__ == "__main__":
    main()
