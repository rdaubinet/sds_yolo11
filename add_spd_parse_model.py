"""
Add space_to_depth handling to parse_model function
"""

from pathlib import Path

def add_spd_parse_model():
    """Add space_to_depth handling to parse_model function"""
    
    tasks_file = Path("venv_cuda/Lib/site-packages/ultralytics/nn/tasks.py")
    
    if not tasks_file.exists():
        print(f"❌ File not found: {tasks_file}")
        return False
    
    print(f"📝 Reading {tasks_file}...")
    with open(tasks_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Check if already added
    for line in lines:
        if "elif m is space_to_depth:" in line:
            print("✅ space_to_depth parse_model code already exists")
            return True
    
    # Find the line with "elif m is Concat:"
    insert_index = -1
    for i, line in enumerate(lines):
        if "elif m is Concat:" in line:
            # Find the end of this elif block (next 1-2 lines)
            # The Concat block is typically:
            # elif m is Concat:
            #     c2 = sum(ch[x] for x in f)
            # We want to insert after this
            insert_index = i + 2  # After the c2 = sum(...) line
            break
    
    if insert_index == -1:
        print("❌ Could not find insertion point (Concat block)")
        return False
    
    # Code to insert
    spd_code = [
        "        elif m is space_to_depth:\n",
        "            c2 = 4 * ch[f]\n"
    ]
    
    # Insert the code
    lines[insert_index:insert_index] = spd_code
    
    # Write back
    print(f"💾 Writing updated {tasks_file}...")
    with open(tasks_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("✅ space_to_depth parse_model code added successfully!")
    print(f"   Inserted at line {insert_index + 1}")
    return True

if __name__ == "__main__":
    add_spd_parse_model()
