# src/treefy/gui/statspanel.py

import customtkinter as ctk


class StatsPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")
        self._create_widgets()

    def _create_widgets(self):
        self.labels = {}  # stock each stat line
        for key in ["Files", "Folders", "Excluded", "Depth"]:
            label = ctk.CTkLabel(self, text=f"{key} : ...", anchor="center")
            label.pack(padx=10, pady=2, fill="x")
            self.labels[key] = label

    def update_stats(self, stats: dict):
        self.labels["Files"].configure(text=f"Files : {stats.get('nb_files', '?')}")
        self.labels["Folders"].configure(text=f"Folders : {stats.get('nb_dirs', '?')}")
        self.labels["Excluded"].configure(text=f"Excluded : {stats.get('nb_greyed', '?')}")
        self.labels["Depth"].configure(text=f"Depth : {stats.get('max_depth', '?')}")
