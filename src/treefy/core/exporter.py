from pathlib import Path

from treefy.core.config import save_config
from treefy.core.selection import Node, SelectionManager


def export_ascii_config(
    node_root: Node, selection_manager: SelectionManager, depth: int, base_path: Path
):
    excluded_paths = [str(node.path.relative_to(base_path)) for node in selection_manager.excluded]
    save_config(
        base_path,
        {
            "depth": depth,
            "excluded": excluded_paths,
        },
    )
    print(f"[EXPORT] {len(excluded_paths)} excluded lines saved.")
    return excluded_paths
