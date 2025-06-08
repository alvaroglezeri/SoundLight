import os
import ast
import re
from typing import Generator

EXCLUDE_DIRS = {"venv", ".venv", "__pycache__", "env", ".env", "site-packages"}
output_file = "funciones_no_snake_case.txt"
snake_case_pattern = re.compile(r"^_?_?[a-z_][a-z0-9_]*$")


def get_py_files(directory) -> Generator:
    for root, dirs, files in os.walk(directory):
        dirs[:] = [
            d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for file in files:
            if file.endswith(".py"):
                yield os.path.join(root, file)


def analyze_file(file_path, result) -> None:
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()
    try:
        tree = ast.parse(source, filename=file_path)
    except SyntaxError:
        return

    relative_path = os.path.relpath(file_path)
    bad_names = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    if not snake_case_pattern.match(item.name):
                        bad_names.append(f"{node.name}.{item.name}")

    if bad_names:
        result[relative_path] = bad_names


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
            lines.append(f"{prefix}{connector}{key}")
            lines.extend(format_tree(tree[key], new_prefix))
        else:
            lines.append(f"{prefix}{connector}{key}")
            for j, item in enumerate(tree[key]):
                item_connector = "└── " if j == len(tree[key]) - 1 else "├── "
                lines.append(f"{new_prefix}{item_connector}{item}")
    return lines


if __name__ == "__main__":
    directorio = "."
    result_data = {}

    for py_file in get_py_files(directorio):
        analyze_file(py_file, result_data)

    tree = build_tree(result_data)
    output_lines = ["root"]
    output_lines += format_tree(tree)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    print(f"Análisis completado. Resultados guardados en '{output_file}'")
