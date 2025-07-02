# src/treefy/gui/treeview.py

import tkinter.filedialog as filedialog
from pathlib import Path

import customtkinter as ctk

from treefy.core.config import load_config
from treefy.core.exporter import export_ascii_config
from treefy.core.ignore import build_ignore_matcher
from treefy.core.selection import Node, SelectionManager
from treefy.core.stats import get_tree_stats
from treefy.core.treebuilder import build_node_tree
from treefy.core.utils import find_node_by_path, format_ascii_line, generate_ascii_tree


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
        self.on_stats_update = None

    def load_path(self, path: Path, use_gitignore: bool = False):
        self.loaded_path = path
        self.status_label.configure(text=f"Imported: {path.name}")
        self.should_ignore = build_ignore_matcher(path, use_gitignore)

        self._rebuild_tree()
        self._render_tree()

    def set_depth(self, value: int):
        self.depth = max(0, value)
        if self.loaded_path:
            self._rebuild_tree()
            self._render_tree()

    def _rebuild_tree(self):
        self.node_root = build_node_tree(self.loaded_path, self.should_ignore, self.depth)
        self.selection_manager = SelectionManager(self.node_root)

        # Load config and apply excluded nodes
        config = load_config(self.loaded_path)
        excluded_relpaths = config.get("excluded", [])
        if self.selection_manager and self.node_root:
            for relpath in excluded_relpaths:
                abs_path = self.loaded_path / relpath
                node = find_node_by_path(self.node_root, abs_path)
                if node:
                    self.selection_manager.exclude(node)

        # callback with stats
        if self.on_stats_update and self.node_root and self.selection_manager:
            stats = get_tree_stats(
                self.node_root,
                self.selection_manager,
            )
            self.on_stats_update(stats)

    def _render_tree(self):
        for widget in self.winfo_children():
            if widget != self.status_label:
                widget.destroy()
        self.label_refs.clear()

        def walk(node: Node, prefix_parts: list[bool]):
            name = node.path.name + "/" if node.is_dir else node.path.name
            ascii_line = format_ascii_line(name, prefix_parts)
            label = ctk.CTkLabel(
                self,
                text=ascii_line,
                anchor="w",
                font=ctk.CTkFont(family="Courier New", size=14),
                height=1,
                corner_radius=0,
            )
            label.pack(fill="x", padx=10, pady=1, ipady=0)

            def on_enter(e):
                label.configure(cursor="hand2", bg_color="#3F3F3F")

            def on_leave(e):
                label.configure(cursor="", bg_color="transparent")

            label.bind("<Enter>", on_enter)
            label.bind("<Leave>", on_leave)
            label.bind("<Button-1>", lambda e, n=node, lbl=label: self._toggle_selection(n, lbl))
            self.label_refs[node] = label

            child_count = len(node.children)
            for idx, child in enumerate(node.children):
                walk(child, prefix_parts + [idx == child_count - 1])

        if self.node_root:
            walk(self.node_root, [])

        self._update_labels_color()

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

    def export_ascii(self):
        if not self.node_root or not self.loaded_path or not self.selection_manager:
            return

        # exports the config and generates the tree/file
        export_ascii_config(self.node_root, self.selection_manager, self.depth, self.loaded_path)
        ascii_output = generate_ascii_tree(self.node_root, self.selection_manager)

        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"{self.loaded_path.name}.txt",
            title="Export ASCII tree",
        )

        if not filepath:
            print("[EXPORT] Export canceled.")
            return

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(ascii_output)
            print(f"[EXPORT] Exported ASCII tree in {filepath}")
        except Exception as e:
            print(f"[EXPORT] Export failed : {e}")
