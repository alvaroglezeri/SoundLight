""" This script extracts test method names from Python files in a given format and writes them to a text file. """
import re
import os

raw_input = """
./test\\core\\test_sl_configuration.py:
  - test_patch_no_path
  - test_patch_invalid_path
  - test_patch_invalid_file
 ... etc.
"""

def normalize_path(path):
    path = path.replace('./', '').replace('\\', '/').replace('/', '.')
    if path.endswith('.py'):
        path = path[:-3]
    return path

def extract_import_paths(raw_text):
    lines = raw_text.strip().splitlines()
    current_module = ''
    import_paths = []

    for line in lines:
        if line.endswith('.py:'):
            current_module = normalize_path(line.strip().rstrip(':'))
            import_paths.append(f'\nFile: {current_module}')
        elif line.strip().startswith('-'):
            method = line.strip().lstrip('- ').strip()
            full_path = f"{current_module}.{method}"
            import_paths.append(full_path)

    return import_paths

if __name__ == '__main__':
    import_paths = extract_import_paths(raw_input)

    with open('test_methods.txt', 'w') as f:
        for path in import_paths:
            f.write(f"{path}\n")
