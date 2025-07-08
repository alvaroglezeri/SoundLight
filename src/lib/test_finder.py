""" List all test methods in Python files starting with 'test_' in a directory. """
import os
import ast

def find_test_methods_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read(), filename=file_path)
        except SyntaxError as e:
            print(f"Syntax error in {file_path}: {e}")
            return []

    test_methods = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
            test_methods.append(node.name)
    return test_methods

def walk_directory_and_list_tests(directory):
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.startswith('test_') and file_name.endswith('.py'):
                path = os.path.join(root, file_name)
                tests = find_test_methods_in_file(path)
                if tests:
                    print(f"{path}:")
                    for test in tests:
                        print(f"  - {test}")

# Use current directory or change it if needed
if __name__ == '__main__':
    walk_directory_and_list_tests('./test')
