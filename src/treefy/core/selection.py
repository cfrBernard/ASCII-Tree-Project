# src/treefy/core/selection.py

from pathlib import Path
from typing import Optional


class Node:
    def __init__(self, path: Path, parent: Optional["Node"] = None):
        self.path = path
        self.parent = parent
        self.children: list[Node] = []
        self.is_dir = path.is_dir()

    def add_child(self, child: "Node"):
        self.children.append(child)

    def iter_ancestors(self):
        current = self.parent
        while current:
            yield current
            current = current.parent

    def iter_descendants(self):
        for child in self.children:
            yield child
            if child.is_dir:
                yield from child.iter_descendants()

    def __hash__(self):
        return hash(self.path)

    def __eq__(self, other):
        return isinstance(other, Node) and self.path == other.path

    def __repr__(self):
        return f"Node({self.path.name})"


class SelectionManager:
    def __init__(self, root: Node):
        self.root = root
        self.excluded: set[Node] = set()  # default = included

    def include(self, node: Node):
        self.excluded.discard(node)
        if node.is_dir:
            for desc in node.iter_descendants():
                self.excluded.discard(desc)
        for ancestor in node.iter_ancestors():
            self.excluded.discard(ancestor)

    def exclude(self, node: Node):
        self.excluded.add(node)
        if node.is_dir:
            for desc in node.iter_descendants():
                self.excluded.add(desc)

        # if all children are excluded
        parent = node.parent
        while parent:
            if any(child not in self.excluded for child in parent.children):
                break
            self.excluded.add(parent)
            parent = parent.parent

    def toggle(self, node: Node):
        if node in self.excluded:
            self.include(node)
        else:
            self.exclude(node)

    def is_included(self, node: Node) -> bool:
        return node not in self.excluded

    def get_excluded(self) -> list[Node]:
        return list(self.excluded)
