import os


def print_dir_tree(root_dir, prefix=""):
    # Listar solo directorios
    dirs = [d for d in os.listdir(root_dir) if os.path.isdir(
        os.path.join(root_dir, d))]
    dirs.sort()

    for i, directory in enumerate(dirs):
        is_last = i == len(dirs) - 1
        connector = "└── " if is_last else "├── "
        print(prefix + connector + directory + "/")

        next_prefix = prefix + ("    " if is_last else "│   ")
        print_dir_tree(os.path.join(root_dir, directory), next_prefix)


if __name__ == "__main__":
    # Cambia este path a lo que necesites
    root_path = "."  # "." es el directorio actual
    print(".")
    print_dir_tree(root_path)
