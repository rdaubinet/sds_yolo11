"""
CUDA Diagnostic Script
Check PyTorch and CUDA configuration
"""

import sys
import torch

print("=" * 70)
print("CUDA DIAGNOSTIC REPORT")
print("=" * 70)

# Python version
print(f"\nPython version: {sys.version}")

# PyTorch version
print(f"\nPyTorch version: {torch.__version__}")

# CUDA availability
cuda_available = torch.cuda.is_available()
print(f"\nCUDA available: {cuda_available}")

if cuda_available:
    print(f"CUDA version: {torch.version.cuda}")
    print(f"cuDNN version: {torch.backends.cudnn.version()}")
    print(f"Number of GPUs: {torch.cuda.device_count()}")
    
    for i in range(torch.cuda.device_count()):
        print(f"\nGPU {i}:")
        print(f"  Name: {torch.cuda.get_device_name(i)}")
        print(f"  Capability: {torch.cuda.get_device_capability(i)}")
        
        props = torch.cuda.get_device_properties(i)
        print(f"  Total memory: {props.total_memory / 1024**3:.2f} GB")
        print(f"  Multi-processor count: {props.multi_processor_count}")
    
    # Test tensor creation on GPU
    try:
        test_tensor = torch.randn(3, 3).cuda()
        print(f"\n✅ Test tensor successfully created on GPU")
        print(f"   Device: {test_tensor.device}")
        del test_tensor
    except Exception as e:
        print(f"\n❌ Failed to create tensor on GPU: {e}")
        
else:
    print("\n⚠️  CUDA is NOT available")
    print("\nPossible reasons:")
    print("  1. PyTorch CPU-only version installed")
    print("  2. NVIDIA GPU drivers not installed")
    print("  3. CUDA toolkit not installed")
    print("  4. GPU not detected by system")
    
    # Check if this is a CPU-only build
    if '+cpu' in torch.__version__:
        print("\n❌ PyTorch CPU-only version detected!")
        print("   You need to install PyTorch with CUDA support")
    
print("\n" + "=" * 70)
print("ENVIRONMENT CHECK")
print("=" * 70)

# Check for CUDA environment variables
import os
cuda_vars = {k: v for k, v in os.environ.items() if 'CUDA' in k}
if cuda_vars:
    print("\nCUDA Environment Variables:")
    for k, v in cuda_vars.items():
        print(f"  {k}: {v}")
else:
    print("\nNo CUDA environment variables found")

print("\n" + "=" * 70)
