# src/treefy/gui/treeview.py

from pathlib import Path

import customtkinter as ctk

from treefy.core.config import load_config, save_config
from treefy.core.ignore import build_ignore_matcher
from treefy.core.selection import Node, SelectionManager
from treefy.core.treebuilder import build_node_tree


class TreeView(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.loaded_path: Path | None = None
        self.depth = -1
        self.node_root: Node | None = None
        self.selection_manager: SelectionManager | None = None
        self.label_refs = {}
        self.status_label = ctk.CTkLabel(
            self, text="No folder imported.", font=ctk.CTkFont(size=16)
        )
        self.status_label.pack(pady=20)

    def set_depth(self, value: int):
        self.depth = value
        if self.node_root:
            self._render_tree()

    def load_path(self, path: Path, use_gitignore: bool = False):
        self.loaded_path = path
        self.status_label.configure(text=f"Imported: {path.name}")

        self.should_ignore = build_ignore_matcher(path, use_gitignore)
        self.node_root = build_node_tree(path, self.should_ignore, self.depth)
        self.selection_manager = SelectionManager(self.node_root) if self.node_root else None

        # Load config and apply excluded nodes
        config = load_config(path)
        excluded_relpaths = config.get("excluded", [])
        if self.selection_manager and self.node_root:
            for relpath in excluded_relpaths:
                abs_path = path / relpath
                node = self._find_node_by_path(self.node_root, abs_path)
                if node:
                    self.selection_manager.exclude(node)

        self._render_tree()

    def _render_tree(self):
        for widget in self.winfo_children():
            if widget != self.status_label:
                widget.destroy()
        self.label_refs.clear()

        def walk(node: Node, depth: int):
            ascii_line = self._format_ascii_line(node.path.name, depth)
            label = ctk.CTkLabel(
                self,
                text=ascii_line,
                anchor="w",
                font=ctk.CTkFont(family="Courier New", size=16),
                height=1,
                corner_radius=0,
            )
            label.pack(fill="x", padx=10, pady=0, ipady=0)
            label.bind("<Button-1>", lambda e, n=node, lbl=label: self._toggle_selection(n, lbl))
            self.label_refs[node] = label

            for child in node.children:
                walk(child, depth + 1)

        if self.node_root:
            walk(self.node_root, 0)

        self._update_labels_color()

    def _format_ascii_line(self, name: str, depth: int) -> str:
        indent = "│   " * (depth - 1) + ("├── " if depth > 0 else "")
        return indent + name

    def _toggle_selection(self, node: Node, label: ctk.CTkLabel):
        if not self.selection_manager:
            return
        self.selection_manager.toggle(node)
        self._update_labels_color()

    def _update_labels_color(self):
        if not self.selection_manager:
            return
        for node, label in self.label_refs.items():
            if self.selection_manager.is_included(node):
                label.configure(text_color="white")
            else:
                label.configure(text_color="gray")

    def _find_node_by_path(self, node: Node, target_path: Path) -> Node | None:
        if node.path == target_path:
            return node
        for child in node.children:
            found = self._find_node_by_path(child, target_path)
            if found:
                return found
        return None

    def export_ascii(self):
        if not self.node_root or not self.loaded_path or not self.selection_manager:
            return

        excluded_paths = [
            str(node.path.relative_to(self.loaded_path)) for node in self.selection_manager.excluded
        ]
        save_config(
            self.loaded_path,
            {
                "depth": self.depth,
                "excluded": excluded_paths,
            },
        )
        print(f"[EXPORT] {len(excluded_paths)} excluded lines saved.")
