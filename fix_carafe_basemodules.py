"""
Script to properly integrate CARAFE into parse_model function
1. Add CARAFE to base_modules frozenset
2. Remove the manual elif handling
"""

import sys
from pathlib import Path

# Path to tasks.py
tasks_path = Path("venv_cuda/Lib/site-packages/ultralytics/nn/tasks.py")

if not tasks_path.exists():
    print(f"❌ Error: {tasks_path} not found!")
    sys.exit(1)

# Read the file
print(f"📖 Reading {tasks_path}")
with open(tasks_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Step 1: Add CARAFE to base_modules
print("✏️  Step 1: Adding CARAFE to base_modules frozenset")
old_base_modules = """    base_modules = frozenset(
        {
            Classify,
            Conv,
            ConvTranspose,
            GhostConv,
            Bottleneck,
            GhostBottleneck,
            SPP,
            SPPF,
            C2fPSA,
            C2PSA,
            DWConv,
            Focus,
            BottleneckCSP,
            C1,
            C2,
            C2f,
            C3k2,
            RepNCSPELAN4,
            ELAN1,
            ADown,
            AConv,
            SPPELAN,
            C2fAttn,
            C3,
            C3TR,
            C3Ghost,
            torch.nn.ConvTranspose2d,
            DWConvTranspose2d,
            C3x,
            RepC3,
            PSA,
            SCDown,
            C2fCIB,
            A2C2f,
        }
    )"""

new_base_modules = """    base_modules = frozenset(
        {
            Classify,
            Conv,
            ConvTranspose,
            GhostConv,
            Bottleneck,
            GhostBottleneck,
            SPP,
            SPPF,
            C2fPSA,
            C2PSA,
            DWConv,
            Focus,
            BottleneckCSP,
            C1,
            C2,
            C2f,
            C3k2,
            RepNCSPELAN4,
            ELAN1,
            ADown,
            AConv,
            SPPELAN,
            C2fAttn,
            C3,
            C3TR,
            C3Ghost,
            torch.nn.ConvTranspose2d,
            DWConvTranspose2d,
            C3x,
            RepC3,
            PSA,
            SCDown,
            C2fCIB,
            A2C2f,
            CARAFE,
        }
    )"""

if old_base_modules in content:
    content = content.replace(old_base_modules, new_base_modules)
    print("   ✅ Added CARAFE to base_modules")
else:
    print("   ⚠️  base_modules not found in expected format")

# Step 2: Remove manual CARAFE handling
print("✏️  Step 2: Removing manual CARAFE handling")
old_manual_handling = """        elif m is space_to_depth:
            c2 = 4 * ch[f]
        elif m is CARAFE:
            c1 = ch[f]  # input channels from previous layer
            c2 = args[0] if args else ch[f]  # output channels from config
            args = [c1, c2] + args[1:]  # [c1, c2, kernel_size, up_factor]
        elif m in frozenset("""

new_manual_handling = """        elif m is space_to_depth:
            c2 = 4 * ch[f]
        elif m in frozenset("""

if old_manual_handling in content:
    content = content.replace(old_manual_handling, new_manual_handling)
    print("   ✅ Removed manual CARAFE handling")
else:
    print("   ⚠️  Manual handling not found or already removed")

# Write back
print(f"💾 Writing updated file")
with open(tasks_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Successfully integrated CARAFE into parse_model function!")
print("   CARAFE is now in base_modules and will be handled automatically")
