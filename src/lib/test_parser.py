import re
import os

raw_input = """
./test\\core\\test_sl_configuration.py:
  - test_patch_no_path
  - test_patch_invalid_path
  - test_patch_invalid_file
  - test_patch_valid_patch
  - test_analysis_no_argument
  - test_analysis_invalid_argument
  - test_analysis_valid_argument
  - test_generation_no_argument
  - test_generation_invalid_argument
  - test_generation_valid_argument
  - test_export_no_argument
  - test_export_invalid_argument
  - test_export_valid_argument
  - test_exportPath_no_argument
  - test_exportPath_invalid_argument
  - test_exportPath_invalid_argument2
  - test_exportPath_valid_argument
./test\\core\\test_sl_config_file.py:
  - test_blank_config_path
  - test_invalid_config_path
  - test_invalid_config_path2
  - test_not_existing_file
  - test_invalid_file
  - test_valid_file
./test\\core\\test_sl_file_handling.py:
  - test_no_path
  - test_invalid_path
  - test_invalid_file
  - test_valid_file
  - test_duplicate_element
  - test_duplicate_element2
  - test_file_conversion
  - test_empty_select
  - test_empty_select2
  - test_invalid_selection
  - test_invalid_selection2
  - test_invalid_index
  - test_valid_index
  - test_close_no_select
  - test_close_no_loaded
  - test_close_selected
  - test_double_close
./test\\core\\test_sl_run.py:
  - test_run_autocreate
  - test_run_checks1
  - test_run_checks2
  - test_run_checks3
  - test_run_checks4
  - test_run_checks5
./test\\core\\analysis\\test_an.py:
  - test_no_song
  - test_invalid_song
  - test_valid_song
  - test_set_no_alg
  - test_set_invalid_alg
  - test_set_valid_alg
  - test_analyze_no_alg
./test\\core\\export\\test_ex.py:
  - test_no_song
  - test_invalid_song
  - test_valid_song
  - test_export_no_song
  - test_set_no_alg
  - test_set_invalid_alg
  - test_set_valid_alg
  - test_export_no_alg
  - test_no_path
  - test_invalid_path
  - test_valid_path
  - test_return_list
  - test_return_bytesIO
  - test_return_none
  - test_return_other
./test\\core\\generation\\test_gen.py:
  - test_no_song
  - test_invalid_song
  - test_valid_song
  - test_set_no_alg
  - test_set_invalid_alg
  - test_set_valid_alg
  - test_gen_no_alg
  - test_patch_no_patch
  - test_patch_invalid_patch
  - test_patch_invalid_patch1
  - test_patch_invalid_patch2
  - test_patch_invalid_patch3
  - test_patch_invalid_patch4
  - test_patch_invalid_patch5
  - test_patch_invalid_patch6
  - test_patch_invalid_patch7
  - test_patch_invalid_patch8
  - test_patch_invalid_patch9
  - test_patch_valid_patch
./test\\core\\model\\test_features.py:
  - test_SimpleFlash_creation1
  - test_SimpleFlash_creation2
  - test_SimpleFlash_creation3
  - test_RGBWFlash_creation1
  - test_RGBWFlash_creation2
  - test_RGBWFlash_creation3
  - test_RotFlash_creation1
  - test_RotFlash_creation2
  - test_RotFlash_creation3
./test\\core\\model\\test_song.py:
  - test_invalid_file
  - test_invalid_file2
  - test_invalid_file3
  - test_valid_file
  - test_eq
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
