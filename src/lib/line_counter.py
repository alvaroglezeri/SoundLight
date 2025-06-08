import os
import json
from typing import List, Dict, Any


def contar_lineas(directorio: str, extensiones: List[str], ordenar_por: str = "ruta") -> Dict[str, Any]:
    archivos: Dict[str, int] = {}
    total = 0

    for root, _, files in os.walk(directorio):
        for file in files:
            if any(file.endswith(ext) for ext in extensiones):
                ruta = os.path.join(root, file)
                try:
                    with open(ruta, 'r', encoding='utf-8', errors='ignore') as f:
                        lineas = sum(1 for _ in f)
                        archivos[ruta] = lineas
                        total += lineas
                except Exception as e:
                    print(f"Error leyendo {ruta}: {e}")

    if ordenar_por == "lineas":
        archivos_ordenados = dict(
            sorted(archivos.items(), key=lambda item: item[1], reverse=True))
    else:
        archivos_ordenados = dict(sorted(archivos.items()))

    return {
        "total_lines": total,
        "files": archivos_ordenados
    }


# Ejemplo de uso
if __name__ == "__main__":
    directorio = "./src"
    extensiones = [".py", ".ipynb", ".md"]
    ordenar_por = "lineas"  # o "ruta"
    resultado = contar_lineas(directorio, extensiones, ordenar_por)
    print(json.dumps(resultado, indent=4))
