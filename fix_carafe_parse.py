"""
Script to add CARAFE handling in parse_model function
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

# Find the location to insert CARAFE handling (after space_to_depth)
search_text = """        elif m is space_to_depth:
            c2 = 4 * ch[f]
        elif m in frozenset("""

if search_text not in content:
    print("❌ Could not find insertion point!")
    sys.exit(1)

# Add CARAFE handling
replacement_text = """        elif m is space_to_depth:
            c2 = 4 * ch[f]
        elif m is CARAFE:
            c1 = ch[f]  # input channels from previous layer
            c2 = args[0] if args else ch[f]  # output channels from config
            args = [c1, c2] + args[1:]  # [c1, c2, kernel_size, up_factor]
        elif m in frozenset("""

# Replace
content = content.replace(search_text, replacement_text)

# Write back
print(f"✏️  Writing updated file")
with open(tasks_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Successfully added CARAFE handling to parse_model function!")
print("\nAdded code:")
print("    elif m is CARAFE:")
print("        c1 = ch[f]  # input channels from previous layer")
print("        c2 = args[0] if args else ch[f]  # output channels from config")
print("        args = [c1, c2] + args[1:]  # [c1, c2, kernel_size, up_factor]")
