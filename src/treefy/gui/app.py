from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from treefy.core.ignore import load_ignore_patterns
from treefy.core.treebuilder import build_tree


class TreefyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Treefy - Project Structure Viewer")
        self.geometry("300x150")

        self.browse_button = ctk.CTkButton(self, text="Choose a folder", command=self.choose_folder)
        self.browse_button.pack(pady=20)

        self.depth_slider = ctk.CTkSlider(
            self, from_=1, to=10, number_of_steps=9, command=self.update_depth
        )
        self.depth_slider.set(5)
        self.depth_slider.pack(pady=10)
        self.depth_value = 5

        self.gitignore_checkbox = ctk.CTkCheckBox(self, text=".gitignore")
        self.gitignore_checkbox.pack()

    def update_depth(self, value):
        self.depth_value = int(value)

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return

        path = Path(folder)
        ignore = load_ignore_patterns(path) if self.gitignore_checkbox.get() else None
        tree = build_tree(path, ignore=ignore, max_depth=self.depth_value)

        out_path = path / "treefy_output.txt"
        out_path.write_text(str(tree))
        messagebox.showinfo("Treefy", f"Exported in :\n{out_path}")
