# src/treefy/core/treebuilder.py

from collections.abc import Callable
from pathlib import Path

from treefy.core.selection import Node


def build_node_tree(
    root_path: Path,
    should_ignore: Callable[[Path], bool] | None = None,
    max_depth: int = -1,
    _parent: Node | None = None,
    _current_depth: int = 0,
) -> Node | None:
    """
    Crée récursivement un arbre de Node à partir d'un chemin root.
    ignore les fichiers/dossiers si should_ignore(path) == True
    """
    if should_ignore and should_ignore(root_path):
        return None
    if max_depth != -1 and _current_depth > max_depth:
        return None

    node = Node(root_path, _parent)
    if node.is_dir:
        try:
            children_paths = sorted(root_path.iterdir())
        except PermissionError:
            children_paths = []
        for child_path in children_paths:
            child_node = build_node_tree(
                child_path, should_ignore, max_depth, node, _current_depth + 1
            )
            if child_node:
                node.add_child(child_node)
    return node
