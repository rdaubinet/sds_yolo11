# Model Export Guide

## Quick Start

Export both models to ONNX format (recommended):
```powershell
cd sds_yolo11
python export_models.py --format onnx
```

## Export Options

### Export Formats

1. **ONNX** (Recommended - Universal format)
   ```powershell
   python export_models.py --format onnx
   ```

2. **TensorRT** (NVIDIA GPU optimized - fastest inference)
   ```powershell
   python export_models.py --format engine
   ```

3. **TorchScript** (PyTorch native)
   ```powershell
   python export_models.py --format torchscript
   ```

4. **OpenVINO** (Intel hardware optimized)
   ```powershell
   python export_models.py --format openvino
   ```

### Export Specific Model

Export only 10-epoch model:
```powershell
python export_models.py --model 10 --format onnx
```

Export only 29-epoch model:
```powershell
python export_models.py --model 29 --format onnx
```

Export both (default):
```powershell
python export_models.py --model both --format onnx
```

### Advanced Options

**Half Precision (FP16)** - Faster inference, smaller files:
```powershell
python export_models.py --format onnx --half
```

**Dynamic Input Shapes** - Variable image sizes:
```powershell
python export_models.py --format onnx --dynamic
```

**Custom Image Size**:
```powershell
python export_models.py --format onnx --imgsz 1280
```

**CPU Export** (if GPU has issues):
```powershell
python export_models.py --format onnx --device cpu
```

**Export Custom Weights**:
```powershell
python export_models.py --weights path/to/custom/weights.pt --format onnx
```

## Output Locations

Exported files are saved next to the original `.pt` files:

- **10-epoch ONNX**: `runs/detect/runs/train/exp/weights/best.onnx`
- **29-epoch ONNX**: `runs/detect/runs/train/exp-2/weights/best.onnx`
- **10-epoch Engine**: `runs/detect/runs/train/exp/weights/best.engine`
- **29-epoch Engine**: `runs/detect/runs/train/exp-2/weights/best.engine`

## Recommended Workflow

1. **Development/Testing**: ONNX format
   ```powershell
   python export_models.py --format onnx
   ```

2. **Production (NVIDIA GPU)**: TensorRT for maximum speed
   ```powershell
   python export_models.py --format engine --half
   ```

3. **Production (CPU/Cross-platform)**: ONNX with simplification
   ```powershell
   python export_models.py --format onnx --simplify
   ```

## File Sizes (Approximate)

- **.pt** (PyTorch): ~5-6 MB
- **.onnx**: ~5-6 MB
- **.onnx** (half precision): ~3 MB
- **.engine** (TensorRT): ~4-5 MB
- **.torchscript**: ~5-6 MB

## Notes

- Export does NOT affect training or original `.pt` files
- Export requires GPU if using `--device 0` (CPU fallback available)
- ONNX is the most portable format
- TensorRT (.engine) is fastest but NVIDIA GPU specific
- Half precision (`--half`) reduces size ~50% with minimal accuracy loss
