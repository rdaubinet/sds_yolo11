"""
Quick GPU verification script
"""
import torch

print("=" * 60)
print("GPU Configuration Check")
print("=" * 60)

# CUDA availability
print(f"\n✅ CUDA Available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    # Number of GPUs
    print(f"✅ CUDA Device Count: {torch.cuda.device_count()}")
    
    # List all CUDA devices
    print("\n📱 Available CUDA Devices:")
    for i in range(torch.cuda.device_count()):
        print(f"   Device {i}: {torch.cuda.get_device_name(i)}")
        props = torch.cuda.get_device_properties(i)
        print(f"      - Total Memory: {props.total_memory / 1024**3:.2f} GB")
        print(f"      - Compute Capability: {props.major}.{props.minor}")
    
    # Current device
    print(f"\n🎯 Current CUDA Device: {torch.cuda.current_device()}")
    print(f"   Name: {torch.cuda.get_device_name(torch.cuda.current_device())}")
    
    # Test allocation
    print("\n🧪 Testing GPU allocation...")
    try:
        test_tensor = torch.randn(1000, 1000).cuda()
        print(f"   ✅ Successfully allocated tensor on GPU")
        print(f"   Device of tensor: {test_tensor.device}")
        del test_tensor
        torch.cuda.empty_cache()
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Memory info
    print(f"\n💾 GPU Memory Status:")
    print(f"   Allocated: {torch.cuda.memory_allocated(0) / 1024**3:.2f} GB")
    print(f"   Reserved: {torch.cuda.memory_reserved(0) / 1024**3:.2f} GB")

else:
    print("❌ CUDA is not available!")

print("\n" + "=" * 60)
print("\nWindows Task Manager GPU Numbering:")
print("  - Task Manager shows physical GPU order")
print("  - PyTorch CUDA only sees CUDA-capable GPUs")
print("  - device=0 in PyTorch = first CUDA GPU")
print("  - This is likely your NVIDIA GPU (GPU 1 in Task Manager)")
print("=" * 60)
