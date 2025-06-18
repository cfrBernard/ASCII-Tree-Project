# src/treefy/gui/treeview.py

from pathlib import Path

import customtkinter as ctk

from treefy.core.config import save_config
from treefy.core.ignore import build_ignore_matcher
from treefy.core.treebuilder import build_tree


class TreeView(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.loaded_path: Path | None = None
        self.depth = -1
        self.selected_paths = set()
        self.label_refs = {}

        self.status_label = ctk.CTkLabel(
            self, text="No folder imported.", font=ctk.CTkFont(size=16)
        )
        self.status_label.pack(pady=20)

    def set_depth(self, value: int):
        self.depth = value
        if self.loaded_path:
            self._render_tree()

    def load_path(self, path: Path, use_gitignore: bool = False):
        self.loaded_path = path
        self.status_label.configure(text=f"Imported: {path.name}")
        self.should_ignore = build_ignore_matcher(path, use_gitignore)
        self.selected_paths.clear()
        self._render_tree()

    def _render_tree(self):
        for widget in self.winfo_children():
            if widget != self.status_label:
                widget.destroy()
        self.label_refs.clear()

        tree = build_tree(self.loaded_path, self.should_ignore, self.depth)

        for _idx, (path, depth) in enumerate(tree):
            ascii_line = self._format_ascii_line(
                path.name, depth, is_last=False
            )  # simplify for now
            label = ctk.CTkLabel(
                self,
                text=ascii_line,
                anchor="w",
                font=ctk.CTkFont(family="Courier New", size=16),
                height=1,
                corner_radius=0,
            )
            label.pack(fill="x", padx=10, pady=0, ipady=0)

            label.bind("<Button-1>", lambda e, p=path, lbl=label: self._toggle_selection(p, lbl))
            self.label_refs[path] = label

    def _format_ascii_line(self, name: str, depth: int, is_last: bool = False) -> str:
        indent = "│   " * (depth - 1) + ("├── " if depth > 0 else "")
        return indent + name

    def _toggle_selection(self, path: Path, label: ctk.CTkLabel):
        if path in self.selected_paths:
            self.selected_paths.remove(path)
            label.configure(text_color="default")
        else:
            self.selected_paths.add(path)
            label.configure(text_color="gray")

    def export_ascii(self):
        # placeholder – export pas encore implémenté
        if self.loaded_path:
            save_config(
                self.loaded_path,
                {
                    "depth": self.depth,
                    "deselected": [
                        str(p.relative_to(self.loaded_path)) for p in self.selected_paths
                    ],
                },
            )
            print(f"[EXPORT] {len(self.selected_paths)} deselected lines saved.")
