"""Counts the number of lines in the files of a directory.
"""
import os
import json
from typing import List, Dict, Any


def count_lines(dir: str, ext: List[str], sort_by: str = "path") -> Dict[str, Any]:
    archivos: Dict[str, int] = {}
    total = 0

    for root, _, files in os.walk(dir):
        for file in files:
            if any(file.endswith(ext) for ext in ext):
                ruta = os.path.join(root, file)
                try:
                    with open(ruta, 'r', encoding='utf-8', errors='ignore') as f:
                        lineas = sum(1 for _ in f)
                        archivos[ruta] = lineas
                        total += lineas
                except Exception as e:
                    print(f"Error leyendo {ruta}: {e}")

    if sort_by == "lines":
        archivos_ordenados = dict(
            sorted(archivos.items(), key=lambda item: item[1], reverse=True))
    else:
        archivos_ordenados = dict(sorted(archivos.items()))

    return {
        "total_lines": total,
        "files": archivos_ordenados
    }


if __name__ == "__main__":
    dir = "./src"
    ext = [".py", ".ipynb", ".md"]
    sort = "lines"  # or "path"
    result = count_lines(dir, ext, sort)
    print(json.dumps(result, indent=4))
