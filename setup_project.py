"""
Setup script for Enhanced YOLO11 Maritime Search and Rescue project
This script helps integrate custom modules into the Ultralytics YOLO11 framework
"""

import os
import shutil
import sys
from pathlib import Path

def find_ultralytics_path():
    """Find the ultralytics installation path"""
    try:
        import ultralytics
        ultralytics_path = Path(ultralytics.__file__).parent
        return ultralytics_path
    except ImportError:
        print("❌ Ultralytics package not found. Please install it first:")
        print("   pip install ultralytics")
        return None

def backup_file(file_path):
    """Create a backup of the original file"""
    if file_path.exists():
        backup_path = file_path.with_suffix(file_path.suffix + '.backup')
        if not backup_path.exists():
            shutil.copy2(file_path, backup_path)
            print(f"✅ Backed up {file_path.name} to {backup_path.name}")
        return True
    return False

def integrate_space_to_depth(ultralytics_path):
    """Integrate Space-to-Depth module"""
    print("\n📦 Integrating Space-to-Depth module...")
    
    # Copy module file
    src_file = Path("code/space_to_depth.py")
    dest_dir = ultralytics_path / "nn" / "modules"
    dest_file = dest_dir / "space_to_depth.py"
    
    if not src_file.exists():
        print(f"❌ Source file not found: {src_file}")
        return False
    
    shutil.copy2(src_file, dest_file)
    print(f"✅ Copied {src_file} to {dest_file}")
    
    # Update tasks.py
    tasks_file = ultralytics_path / "nn" / "tasks.py"
    if not tasks_file.exists():
        print(f"❌ tasks.py not found at {tasks_file}")
        return False
    
    backup_file(tasks_file)
    
    with open(tasks_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already integrated
    if "from ultralytics.nn.modules.space_to_depth import space_to_depth" in content:
        print("✅ Space-to-Depth already integrated in tasks.py")
        return True
    
    # Add import
    import_line = "from ultralytics.nn.modules.space_to_depth import space_to_depth"
    
    # Find the imports section and add our import
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('from ultralytics.nn.modules'):
            # Add after the last ultralytics.nn.modules import
            if i + 1 < len(lines) and not lines[i + 1].startswith('from ultralytics.nn.modules'):
                lines.insert(i + 1, import_line)
                break
    
    content = '\n'.join(lines)
    
    # Add to parse_model function
    parse_model_addition = """elif m is space_to_depth:
        c2 = 4 * ch[f]"""
    
    if parse_model_addition not in content:
        # Find a good place to add it (after other elif statements in parse_model)
        print("⚠️  Manual integration needed for parse_model function")
        print("   Add the following code to the parse_model function in tasks.py:")
        print(f"   {parse_model_addition}")
    
    with open(tasks_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Updated tasks.py with Space-to-Depth import")
    return True

def integrate_carafe(ultralytics_path):
    """Integrate CARAFE upsampling module"""
    print("\n📦 Integrating CARAFE module...")
    
    # Copy module file
    src_file = Path("code/carafe.py")
    dest_dir = ultralytics_path / "nn" / "modules"
    dest_file = dest_dir / "carafe.py"
    
    if not src_file.exists():
        print(f"❌ Source file not found: {src_file}")
        return False
    
    shutil.copy2(src_file, dest_file)
    print(f"✅ Copied {src_file} to {dest_file}")
    
    # Update tasks.py
    tasks_file = ultralytics_path / "nn" / "tasks.py"
    
    with open(tasks_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already integrated
    if "from ultralytics.nn.modules.carafe import CARAFE" in content:
        print("✅ CARAFE already integrated in tasks.py")
        return True
    
    # Add import
    import_line = "from ultralytics.nn.modules.carafe import CARAFE"
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('from ultralytics.nn.modules'):
            if i + 1 < len(lines) and not lines[i + 1].startswith('from ultralytics.nn.modules'):
                lines.insert(i + 1, import_line)
                break
    
    content = '\n'.join(lines)
    
    with open(tasks_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Updated tasks.py with CARAFE import")
    return True

def update_init_file(ultralytics_path):
    """Update __init__.py to export new modules"""
    print("\n📦 Updating module exports...")
    
    init_file = ultralytics_path / "nn" / "modules" / "__init__.py"
    
    if not init_file.exists():
        print(f"❌ __init__.py not found at {init_file}")
        return False
    
    backup_file(init_file)
    
    with open(init_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    additions = []
    if "space_to_depth" not in content:
        additions.append("from .space_to_depth import space_to_depth")
    if "CARAFE" not in content:
        additions.append("from .carafe import CARAFE")
    
    if additions:
        # Add to imports
        content += "\n" + "\n".join(additions) + "\n"
        
        # Update __all__ if it exists
        if "__all__" in content:
            all_line_idx = content.rfind("__all__")
            # This is a simplified approach - manual verification recommended
            print("⚠️  Please manually add 'space_to_depth' and 'CARAFE' to __all__ list in __init__.py")
        
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Updated __init__.py")
    else:
        print("✅ __init__.py already up to date")
    
    return True

def main():
    """Main setup function"""
    print("=" * 60)
    print("Enhanced YOLO11 Maritime Search & Rescue - Setup Script")
    print("=" * 60)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Find ultralytics installation
    ultralytics_path = find_ultralytics_path()
    if not ultralytics_path:
        print("\n❌ Setup failed: Ultralytics not installed")
        return False
    
    print(f"\n✅ Found Ultralytics at: {ultralytics_path}")
    
    # Integrate modules
    success = True
    success = integrate_space_to_depth(ultralytics_path) and success
    success = integrate_carafe(ultralytics_path) and success
    success = update_init_file(ultralytics_path) and success
    
    if success:
        print("\n" + "=" * 60)
        print("✅ Setup completed successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Review the configuration files in cfgs/ folder")
        print("2. Download the SeaDronesSee dataset from:")
        print("   https://cloud.cs.uni-tuebingen.de/index.php/s/aJQPHLGnke68M52")
        print("3. Train your model using the provided YAML configs")
        print("\nExample training command:")
        print("   yolo detect train data=path/to/data.yaml model=cfgs/SOTA\\ Comparison/ours.yaml")
    else:
        print("\n⚠️  Setup completed with warnings")
        print("Please review the messages above and complete manual steps if needed")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
