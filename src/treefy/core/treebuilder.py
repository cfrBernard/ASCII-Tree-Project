from collections.abc import Callable
from pathlib import Path


def build_tree(root: Path, should_ignore: Callable[[Path], bool], max_depth: int = -1):
    tree = []

    def recurse(path: Path, depth: int):
        if max_depth != -1 and depth > max_depth:
            return
        if should_ignore(path):
            return  # Ignore du dossier/fichier
        tree.append((path, depth))
        if path.is_dir():
            for child in sorted(path.iterdir()):
                recurse(child, depth + 1)

    recurse(root, 0)
    return tree
