"""Checks which methods of the whole codebase have documentation strings.
Useful to check completion of code.
"""
import os
import ast

from typing import Generator


EXCLUDE_DIRS = {"venv", ".venv", "__pycache__", "env", ".env", "site-packages"}
output_file = "missing_docstrings.txt"


def get_py_files(directory) -> Generator:
    for root, dirs, files in os.walk(directory):
        dirs[:] = [
            d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for file in files:
            if file.endswith(".py"):
                yield os.path.join(root, file)


def analyze_file(file_path, tree_result) -> None:
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()
    try:
        tree = ast.parse(source, filename=file_path)
    except SyntaxError:
        return

    relative_path = os.path.relpath(file_path)
    elements = []

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.ClassDef):
            if not ast.get_docstring(node):
                elements.append(node.name)
            sub_elements = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and not ast.get_docstring(item):
                    sub_elements.append(f"{node.name}.{item.name}")
            elements.extend(sub_elements)
        elif isinstance(node, ast.FunctionDef):
            if not ast.get_docstring(node):
                elements.append(node.name)

    if elements:
        tree_result[relative_path] = elements


def build_tree(data) -> dict:
    tree = {}
    for path, symbols in data.items():
        parts = path.split(os.sep)
        d = tree
        for part in parts[:-1]:
            d = d.setdefault(part, {})
        d[parts[-1]] = symbols
    return tree


def format_tree(tree, prefix="") -> list[str]:
    lines = []
    keys = sorted(tree.keys())
    for i, key in enumerate(keys):
        connector = "└── " if i == len(keys) - 1 else "├── "
        new_prefix = prefix + ("    " if i == len(keys) - 1 else "│   ")
        if isinstance(tree[key], dict):
            lines.append(f"{prefix}{connector}{key} ")
            lines.extend(format_tree(tree[key], new_prefix))
        else:
            lines.append(f"{prefix}{connector}{key}")
            for j, item in enumerate(tree[key]):
                item_connector = "└── " if j == len(tree[key]) - 1 else "├── "
                lines.append(f"{new_prefix}{item_connector}{item} ")
    return lines


if __name__ == "__main__":

    directorio = "."
    tree_data = {}
    for py_file in get_py_files(directorio):
        analyze_file(py_file, tree_data)

    tree = build_tree(tree_data)
    output_lines = ["root"]
    output_lines += format_tree(tree)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    print(
        f"Finished! Results saved in '{output_file}'")
