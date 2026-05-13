"""
Fix tasks.py to properly integrate Space-to-Depth and CARAFE modules
"""

import re
from pathlib import Path

def fix_tasks_py():
    """Properly integrate custom modules into tasks.py"""
    
    # Path to tasks.py
    tasks_file = Path("venv_cuda/Lib/site-packages/ultralytics/nn/tasks.py")
    
    if not tasks_file.exists():
        print(f"❌ File not found: {tasks_file}")
        return False
    
    print(f"📝 Reading {tasks_file}...")
    with open(tasks_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already integrated
    if "from ultralytics.nn.modules.space_to_depth import space_to_depth" in content:
        print("✅ space_to_depth import already exists")
    else:
        # Find the line after the main import statement
        # Look for the closing parenthesis of "from ultralytics.nn.modules import ("
        pattern = r'(from ultralytics\.nn\.modules import \([^)]+\))'
        
        # Add the import after the closing parenthesis
        replacement = r'\1\nfrom ultralytics.nn.modules.space_to_depth import space_to_depth'
        content = re.sub(pattern, replacement, content, count=1)
        print("✅ Added space_to_depth import")
    
    if "from ultralytics.nn.modules.carafe import CARAFE" in content:
        print("✅ CARAFE import already exists")
    else:
        # Add CARAFE import after space_to_depth
        if "from ultralytics.nn.modules.space_to_depth import space_to_depth" in content:
            content = content.replace(
                "from ultralytics.nn.modules.space_to_depth import space_to_depth",
                "from ultralytics.nn.modules.space_to_depth import space_to_depth\nfrom ultralytics.nn.modules.carafe import CARAFE"
            )
            print("✅ Added CARAFE import")
    
    # Now add the parse_model code
    # Look for the parse_model function and add the space_to_depth handling
    if "elif m is space_to_depth:" in content:
        print("✅ space_to_depth parse_model code already exists")
    else:
        # Find a good place to add it - after other elif statements in parse_model
        # Look for a pattern like "elif m in (...:" and add after it
        pattern = r'(elif m in \{Classify[^\}]+\}:.*?args = \[ch\[f\], args\[0\]\])'
        
        spd_code = '''
        elif m is space_to_depth:
            c2 = 4 * ch[f]'''
        
        if re.search(pattern, content, re.DOTALL):
            replacement = r'\1' + spd_code
            content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)
            print("✅ Added space_to_depth parse_model code")
        else:
            print("⚠️  Could not automatically add space_to_depth parse_model code")
            print("   You may need to add it manually")
    
    # Write the updated content
    print(f"💾 Writing updated {tasks_file}...")
    with open(tasks_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ tasks.py updated successfully!")
    return True

if __name__ == "__main__":
    fix_tasks_py()
