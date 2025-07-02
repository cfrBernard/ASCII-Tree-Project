# src/treefy/gui/sidebar.py

from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk

from treefy.gui.statspanel import StatsPanel


class ToggleSection(ctk.CTkFrame):
    def __init__(self, master, title, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.visible = ctk.BooleanVar(value=True)
        self.title = title

        self.toggle_btn = ctk.CTkButton(
            self,
            text=f"▼ {title}",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.toggle,
            fg_color="transparent",
            hover=True,
        )
        self.toggle_btn.pack(fill="x")

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(fill="x", pady=(5, 10))

    def toggle(self):
        if self.visible.get():
            self.content_frame.pack_forget()
            self.visible.set(False)
            self.toggle_btn.configure(text=f"► {self.title}")
        else:
            self.content_frame.pack(fill="x", pady=(5, 10))
            self.visible.set(True)
            self.toggle_btn.configure(text=f"▼ {self.title}")


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, command_handler):
        super().__init__(master, width=200)
        self.pack_propagate(False)
        self.command_handler = command_handler

        self.slider_max = 11  # 0..10 + 1 = All
        self.real_max_depth = 20  # Hard cap
        self._last_depth = None

        self.init_ui()

    def init_ui(self):
        self._create_action_buttons()
        self._create_depth_section()
        self._create_stats_section()

    def _create_action_buttons(self):
        # Container for buttons on top
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10, padx=10)

        import_btn = ctk.CTkButton(btn_frame, text="Import Folder", command=self.import_folder)
        import_btn.pack(fill="x", pady=(0, 5))

        export_btn = ctk.CTkButton(
            btn_frame, text="Export", command=lambda: self.command_handler("export")
        )
        export_btn.pack(fill="x", pady=(10, 5))
        export_btn.configure(state="disabled")

        export_as_btn = ctk.CTkButton(
            btn_frame, text="Export As...", command=lambda: self.command_handler("export_as")
        )
        export_as_btn.pack(fill="x")

    def _create_depth_section(self):
        self.depth_section = ToggleSection(self, "Depth")
        self.depth_section.pack(fill="x", padx=10, pady=(10, 0))

        self.depth_var = ctk.IntVar(value=5)

        self.depth_slider = ctk.CTkSlider(
            self.depth_section.content_frame,
            from_=0,
            to=self.slider_max,
            number_of_steps=self.slider_max,
            variable=self.depth_var,
            command=self._on_depth_change,
        )
        self.depth_slider.pack(fill="x", padx=5, pady=(10, 5))

        self.depth_label = ctk.CTkLabel(
            self.depth_section.content_frame, text="Depth: 5", font=ctk.CTkFont(size=12)
        )
        self.depth_label.pack()

    def _create_stats_section(self):
        self.stats_section = ToggleSection(self, "Stats & Ignore")
        self.stats_section.pack(fill="x", padx=10, pady=(10, 10))

        self.stats_panel = StatsPanel(self.stats_section.content_frame)
        self.stats_panel.pack(fill="x", pady=(0, 5))

        self.ignore_footer = ctk.CTkLabel(
            self.stats_section.content_frame, text="Ignore: (none)", font=ctk.CTkFont(size=10)
        )
        self.ignore_footer.pack(fill="x")

    def set_depth_slider(self, value: int):
        if value >= self.slider_max:
            self.depth_slider.set(self.slider_max)
            self.depth_label.configure(text="All")
        else:
            self.depth_slider.set(value)
            self.depth_label.configure(text=f"Depth: {value}")

    def _on_depth_change(self, val):
        val = int(float(val))

        if val == self._last_depth:
            return  # avoid unnecessary refresh

        self._last_depth = val

        if val == self.slider_max:
            label = "All"
            internal_depth = self.real_max_depth
        else:
            label = f"Depth: {val}"
            internal_depth = val

        self.depth_label.configure(text=label)
        self.command_handler("depth", internal_depth)

    def import_folder(self):
        path_str = filedialog.askdirectory()
        if path_str:
            path = Path(path_str)
            self.gitignore_used = (path / ".gitignore").exists()
            self.command_handler("import", path)

            ignores = []
            if self.gitignore_used:
                ignores.append(".gitignore")
            if (path / ".treefy" / ".treefyignore").exists():
                ignores.append(".treefyignore")

            self.ignore_footer.configure(
                text=f"Ignore: {', '.join(ignores) if ignores else '(none)'}"
            )
