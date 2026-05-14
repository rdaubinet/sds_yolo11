"""
Export trained YOLO11 models to various engine formats
Exports both 10-epoch and 29-epoch models for deployment
"""

import argparse
from pathlib import Path
from ultralytics import YOLO
import torch

def export_model(
    weights_path: str,
    format: str = 'onnx',
    imgsz: int = 640,
    device: str = '0',
    simplify: bool = True,
    dynamic: bool = False,
    half: bool = False
):
    """
    Export a trained YOLO model to specified format
    
    Args:
        weights_path: Path to trained model weights (.pt file)
        format: Export format (onnx, torchscript, engine, openvino, coreml)
        imgsz: Input image size
        device: Device to use for export
        simplify: Simplify ONNX model
        dynamic: Dynamic input shapes (ONNX)
        half: FP16 half-precision export
    """
    
    weights_path = Path(weights_path)
    if not weights_path.exists():
        raise FileNotFoundError(f"Weights file not found: {weights_path}")
    
    print("=" * 70)
    print(f"Exporting Model: {weights_path.name}")
    print("=" * 70)
    print(f"Format:     {format.upper()}")
    print(f"Image Size: {imgsz}")
    print(f"Device:     {device}")
    print(f"Simplify:   {simplify}")
    print(f"Dynamic:    {dynamic}")
    print(f"Half (FP16): {half}")
    print("=" * 70 + "\n")
    
    # Load the trained model
    model = YOLO(str(weights_path))
    
    # Export the model
    try:
        export_path = model.export(
            format=format,
            imgsz=imgsz,
            device=device,
            simplify=simplify,
            dynamic=dynamic,
            half=half
        )
        
        print("\n" + "=" * 70)
        print("✅ Export completed successfully!")
        print("=" * 70)
        print(f"Exported model: {export_path}")
        print("=" * 70 + "\n")
        
        return export_path
        
    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ Export failed!")
        print("=" * 70)
        print(f"Error: {str(e)}")
        print("=" * 70 + "\n")
        raise

def export_both_models(
    format: str = 'onnx',
    imgsz: int = 640,
    device: str = '0',
    simplify: bool = True,
    dynamic: bool = False,
    half: bool = False
):
    """
    Export both 10-epoch and 29-epoch models
    """
    
    # Define model paths
    models = {
        "10-epoch": "runs/detect/runs/train/exp/weights/best.pt",
        "29-epoch": "runs/detect/runs/train/exp-2/weights/best.pt"
    }
    
    print("\n" + "🚀" * 35)
    print("YOLO11 Model Export - Batch Export")
    print("🚀" * 35 + "\n")
    
    exported_files = {}
    
    for name, weights_path in models.items():
        try:
            print(f"\n📦 Exporting {name} model...")
            export_path = export_model(
                weights_path=weights_path,
                format=format,
                imgsz=imgsz,
                device=device,
                simplify=simplify,
                dynamic=dynamic,
                half=half
            )
            exported_files[name] = export_path
            
        except Exception as e:
            print(f"⚠️  Failed to export {name} model: {str(e)}")
            exported_files[name] = None
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 EXPORT SUMMARY")
    print("=" * 70)
    for name, path in exported_files.items():
        status = "✅ Success" if path else "❌ Failed"
        print(f"{name:15} {status}")
        if path:
            print(f"                → {path}")
    print("=" * 70 + "\n")

def main():
    parser = argparse.ArgumentParser(
        description='Export trained YOLO11 models to deployment formats',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        '--format',
        type=str,
        default='onnx',
        choices=['onnx', 'torchscript', 'engine', 'openvino', 'coreml'],
        help='Export format'
    )
    
    parser.add_argument(
        '--imgsz',
        type=int,
        default=640,
        help='Input image size'
    )
    
    parser.add_argument(
        '--device',
        type=str,
        default='0',
        help='Device to use (cuda device or cpu)'
    )
    
    parser.add_argument(
        '--simplify',
        action='store_true',
        default=True,
        help='Simplify ONNX model'
    )
    
    parser.add_argument(
        '--no-simplify',
        action='store_false',
        dest='simplify',
        help='Do not simplify ONNX model'
    )
    
    parser.add_argument(
        '--dynamic',
        action='store_true',
        help='Dynamic input shapes (ONNX only)'
    )
    
    parser.add_argument(
        '--half',
        action='store_true',
        help='FP16 half-precision export'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        choices=['both', '10', '29'],
        default='both',
        help='Which model(s) to export'
    )
    
    parser.add_argument(
        '--weights',
        type=str,
        help='Custom path to weights file (overrides --model)'
    )
    
    args = parser.parse_args()
    
    # Check CUDA availability
    if args.device != 'cpu':
        if not torch.cuda.is_available():
            print("⚠️  CUDA not available, falling back to CPU")
            args.device = 'cpu'
        else:
            print(f"✅ CUDA available: {torch.cuda.get_device_name(0)}\n")
    
    # Export based on selection
    if args.weights:
        # Export custom weights file
        export_model(
            weights_path=args.weights,
            format=args.format,
            imgsz=args.imgsz,
            device=args.device,
            simplify=args.simplify,
            dynamic=args.dynamic,
            half=args.half
        )
    elif args.model == 'both':
        # Export both models
        export_both_models(
            format=args.format,
            imgsz=args.imgsz,
            device=args.device,
            simplify=args.simplify,
            dynamic=args.dynamic,
            half=args.half
        )
    elif args.model == '10':
        # Export 10-epoch model only
        export_model(
            weights_path="runs/detect/runs/train/exp/weights/best.pt",
            format=args.format,
            imgsz=args.imgsz,
            device=args.device,
            simplify=args.simplify,
            dynamic=args.dynamic,
            half=args.half
        )
    elif args.model == '29':
        # Export 29-epoch model only
        export_model(
            weights_path="runs/detect/runs/train/exp-2/weights/best.pt",
            format=args.format,
            imgsz=args.imgsz,
            device=args.device,
            simplify=args.simplify,
            dynamic=args.dynamic,
            half=args.half
        )

if __name__ == "__main__":
    main()
