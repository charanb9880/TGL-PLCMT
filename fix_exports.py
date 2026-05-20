import os
import re
from pathlib import Path

def fix_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Match: export default function Something(...) {
    # We will replace it with:
    # const Something = (...) => {
    # and append export default Something; to the bottom.
    
    pattern = re.compile(r'^export default function\s+([A-Za-z0-9_]+)\s*\((.*?)\)\s*\{', re.MULTILINE)
    
    match = pattern.search(content)
    if not match:
        return
        
    func_name = match.group(1)
    args = match.group(2)
    
    # Replace the declaration
    new_decl = f"const {func_name} = ({args}) => {{"
    new_content = content[:match.start()] + new_decl + content[match.end():]
    
    # Append export default at the end
    if not new_content.strip().endswith(";"):
        new_content += "\n"
    new_content += f"\nexport default {func_name};\n"
    
    with open(file_path, 'w') as f:
        f.write(new_content)
    print(f"Fixed {file_path}")

directories = ['frontend/src/hooks', 'frontend/src/pages']
for d in directories:
    for root, _, files in os.walk(d):
        for file in files:
            if file.endswith('.js') or file.endswith('.jsx'):
                fix_file(os.path.join(root, file))

