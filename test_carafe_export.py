"""
Test CARAFE ONNX/TensorRT Export Compatibility
Quick validation script to test if the fixed CARAFE module exports correctly
"""

import torch
from ultralytics import YOLO
import sys

def test_onnx_export(weights_path="runs/detect/runs/train/exp-2/weights/best.pt"):
    """
    Test ONNX export with the fixed CARAFE module
    """
    print("=" * 70)
    print("Testing CARAFE ONNX Export Compatibility")
    print("=" * 70)
    
    try:
        # Load model
        print(f"\n📦 Loading model: {weights_path}")
        model = YOLO(weights_path)
        print("✅ Model loaded successfully")
        
        # Test ONNX export
        print("\n🔄 Attempting ONNX export...")
        onnx_path = model.export(
            format='onnx',
            imgsz=640,
            device='0',
            simplify=True,
            dynamic=False,
            half=False
        )
        
        print("\n" + "=" * 70)
        print("✅ ONNX EXPORT SUCCESSFUL!")
        print("=" * 70)
        print(f"ONNX model saved to: {onnx_path}")
        print("\nThe CARAFE fix works! You can now export to ONNX.")
        print("=" * 70)
        
        return True, onnx_path
        
    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ ONNX EXPORT FAILED")
        print("=" * 70)
        print(f"Error: {str(e)}")
        print("\nThe CARAFE module still has export issues.")
        print("=" * 70)
        
        return False, None

def test_tensorrt_export(weights_path="runs/detect/runs/train/exp-2/weights/best.pt"):
    """
    Test TensorRT export with the fixed CARAFE module
    """
    print("\n" + "=" * 70)
    print("Testing CARAFE TensorRT Export Compatibility")
    print("=" * 70)
    
    try:
        # Load model
        print(f"\n📦 Loading model: {weights_path}")
        model = YOLO(weights_path)
        print("✅ Model loaded successfully")
        
        # Test TensorRT export
        print("\n🔄 Attempting TensorRT export...")
        engine_path = model.export(
            format='engine',
            imgsz=640,
            device='0',
            half=False
        )
        
        print("\n" + "=" * 70)
        print("✅ TENSORRT EXPORT SUCCESSFUL!")
        print("=" * 70)
        print(f"TensorRT engine saved to: {engine_path}")
        print("\nReady for high-speed video analysis!")
        print("=" * 70)
        
        return True, engine_path
        
    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ TENSORRT EXPORT FAILED")
        print("=" * 70)
        print(f"Error: {str(e)}")
        print("\nTensorRT export still has issues.")
        print("=" * 70)
        
        return False, None

def main():
    print("\n🚀 CARAFE Export Compatibility Test\n")
    
    # Check CUDA
    if not torch.cuda.is_available():
        print("⚠️  Warning: CUDA not available. Exports may be limited.")
    else:
        print(f"✅ CUDA available: {torch.cuda.get_device_name(0)}\n")
    
    # Test on 29-epoch model
    weights = "runs/detect/runs/train/exp-2/weights/best.pt"
    
    # Test ONNX first
    onnx_success, onnx_path = test_onnx_export(weights)
    
    if onnx_success:
        # If ONNX works, try TensorRT
        tensorrt_success, engine_path = test_tensorrt_export(weights)
        
        if tensorrt_success:
            print("\n" + "🎉" * 35)
            print("COMPLETE SUCCESS!")
            print("🎉" * 35)
            print("\nBoth ONNX and TensorRT exports work!")
            print(f"ONNX: {onnx_path}")
            print(f"TensorRT: {engine_path}")
            print("\n✅ Ready to proceed with training remaining 71 epochs!")
            return 0
        else:
            print("\n" + "⚠️ " * 20)
            print("PARTIAL SUCCESS")
            print("⚠️ " * 20)
            print("\nONNX export works, but TensorRT has issues.")
            print("You can use ONNX with ONNXRuntime-GPU for fast inference.")
            return 1
    else:
        print("\n" + "❌" * 35)
        print("EXPORT FAILED")
        print("❌" * 35)
        print("\nThe CARAFE fix needs more work.")
        print("Recommend: Train standard YOLO11 for TensorRT compatibility.")
        return 2

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
