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
        if not isinstance(other, Node):
            return False
        return self.path == other.path

    def __repr__(self):
        return f"Node({self.path.name})"


class SelectionManager:
    def __init__(self, root: Node):
        self.root = root
        self.selected: set[Node] = set()

    def select(self, node: Node):
        if node.is_dir:
            self._select_dir(node)
        else:
            self._select_file(node)
        self._select_ancestors(node)

    def deselect(self, node: Node):
        if node.is_dir:
            self._deselect_dir(node)
        else:
            self._deselect_file(node)

    def toggle(self, node: Node):
        if node in self.selected:
            self.deselect(node)
        else:
            self.select(node)

    def _select_file(self, node: Node):
        self.selected.add(node)

    def _select_dir(self, node: Node):
        self.selected.add(node)
        for desc in node.iter_descendants():
            self.selected.add(desc)

    def _select_ancestors(self, node: Node):
        for ancestor in node.iter_ancestors():
            if ancestor not in self.selected:
                self.selected.add(ancestor)

    def _deselect_file(self, node: Node):
        self.selected.discard(node)
        # remonter et désélection si tous frères désélectionnés
        parent = node.parent
        while parent:
            if any(sib in self.selected for sib in parent.children):
                break
            self.selected.discard(parent)
            parent = parent.parent

    def _deselect_dir(self, node: Node):
        self.selected.discard(node)
        for desc in node.iter_descendants():
            self.selected.discard(desc)
