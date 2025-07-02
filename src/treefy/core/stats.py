# src/treefy/core/stats.py

from treefy.core.selection import Node, SelectionManager


def get_tree_stats(
    root_node: Node,
    selection_manager: SelectionManager,
) -> dict:
    """
    Returns tree statistics:
    - total number of files
    - total number of folders
    - number of files/folders excluded
    - maximum depth
    """
    total_files = 0
    total_dirs = 0
    max_depth = 0
    greyed = set(selection_manager.get_excluded())

    def walk(node: Node, depth: int = 0):
        nonlocal total_files, total_dirs, max_depth
        if node.is_dir:
            total_dirs += 1
        else:
            total_files += 1
        max_depth = max(max_depth, depth)
        for child in node.children:
            walk(child, depth + 1)

    walk(root_node)

    return {
        "nb_files": total_files,
        "nb_dirs": total_dirs,
        "nb_greyed": len(greyed),
        "max_depth": max_depth,
    }
