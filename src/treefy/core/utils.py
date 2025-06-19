from pathlib import Path

from treefy.core.selection import Node


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
