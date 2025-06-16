from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, command_handler):
        super().__init__(master, width=200)
        self.command_handler = command_handler

        self.slider_max = 11  # 0..10 + 1 = All
        self.real_max_depth = 20  # Hard cap
        self.init_ui()

    def init_ui(self):
        import_btn = ctk.CTkButton(self, text="Import Folder", command=self.import_folder)
        import_btn.pack(fill="x", pady=5)

        ctk.CTkLabel(self, text="Depth").pack(pady=(20, 0))

        self.depth_var = ctk.IntVar(value=5)  # Default to 5

        self.depth_slider = ctk.CTkSlider(
            self,
            from_=0,
            to=self.slider_max,
            number_of_steps=self.slider_max + 1,
            variable=self.depth_var,
            command=self._on_depth_change,
        )
        self.depth_slider.pack(fill="x", padx=5, pady=5)

        self.depth_label = ctk.CTkLabel(self, text="Depth: 5")
        self.depth_label.pack()

        self.use_gitignore = ctk.BooleanVar(value=False)
        self.gitignore_checkbox = ctk.CTkCheckBox(
            self,
            text="Use .gitignore",
            variable=self.use_gitignore,
            command=self._on_gitignore_toggle,
        )
        self.gitignore_checkbox.pack(pady=(10, 0))
        self.gitignore_checkbox.configure(state="disabled")

        ctk.CTkButton(self, text="Export", command=lambda: self.command_handler("export")).pack(
            fill="x", pady=(30, 10)
        )

    def _on_depth_change(self, val):
        val = int(float(val))
        if val == self.slider_max:
            label = "All"
            internal_depth = self.real_max_depth
        else:
            label = f"Depth: {val}"
            internal_depth = val

        self.depth_label.configure(text=label)
        self.command_handler("depth", internal_depth)

    def _on_gitignore_toggle(self):
        self.command_handler("gitignore", self.use_gitignore.get())

    def import_folder(self):
        path_str = filedialog.askdirectory()
        if path_str:
            path = Path(path_str)
            self.command_handler("import", path)

            if (path / ".gitignore").exists():
                self.gitignore_checkbox.configure(state="normal")
                self.use_gitignore.set(True)
                self._on_gitignore_toggle()
            else:
                self.gitignore_checkbox.configure(state="disabled")
                self.gitignore_checkbox.deselect()
                self.use_gitignore.set(False)
