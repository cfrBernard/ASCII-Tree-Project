# src/treefy/core/utils.py

from pathlib import Path

from treefy.core.selection import Node, SelectionManager


def find_node_by_path(node: Node, target_path: Path) -> Node | None:
    if node.path == target_path:
        return node
    for child in node.children:
        found = find_node_by_path(child, target_path)
        if found:
            return found
    return None


def format_ascii_line(name: str, prefix_parts: list[bool]) -> str:
    parts = []
    for is_last_level in prefix_parts[:-1]:
        parts.append("    " if is_last_level else "│   ")
    if prefix_parts:
        is_last = prefix_parts[-1]
        parts.append("└── " if is_last else "├── ")
    return "".join(parts) + name


def generate_ascii_tree(node: Node, selection_manager: SelectionManager, prefix_parts=None) -> str:
    if prefix_parts is None:
        prefix_parts = []

    if not selection_manager.is_included(node):
        return ""

    name = node.path.name + "/" if node.is_dir else node.path.name
    lines = [format_ascii_line(name, prefix_parts)]

    child_count = len([c for c in node.children if selection_manager.is_included(c)])
    for idx, child in enumerate(node.children):
        if not selection_manager.is_included(child):
            continue
        is_last = idx == (child_count - 1)
        lines.append(generate_ascii_tree(child, selection_manager, prefix_parts + [is_last]))

    return "\n".join(filter(None, lines))
