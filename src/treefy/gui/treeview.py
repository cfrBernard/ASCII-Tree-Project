from pathlib import Path

import customtkinter as ctk


class TreeView(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.loaded_path: Path | None = None
        self.depth = -1

        self.status_label = ctk.CTkLabel(
            self, text="No folder imported.", font=ctk.CTkFont(size=16)
        )
        self.status_label.pack(pady=20)

    def load_path(self, path: Path, use_gitignore: bool = False):
        print(f"[TreeView] gitignore={use_gitignore}")
        self.loaded_path = path
        self.status_label.configure(text=f"Imported: {path.name}")

    def set_depth(self, value: int):
        self.depth = value
        print(f"Depth set to {value}")

    def export_ascii(self):
        print("Export called")
