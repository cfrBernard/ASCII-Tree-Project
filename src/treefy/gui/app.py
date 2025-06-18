# src/treefy/gui/app.py

import customtkinter as ctk

from treefy.core.config import load_config
from treefy.gui.sidebar import Sidebar
from treefy.gui.treeview import TreeView


class TreefyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Treefy - ASCII Project Tree Viewer")
        self.geometry("1000x700")
        self.minsize(800, 500)

        self.sidebar = Sidebar(self, command_handler=self.handle_command)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        self.treeview = TreeView(self)
        self.treeview.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.current_path = None

    def handle_command(self, command: str, value=None):
        match command:
            case "import":
                self.current_path = value
                self.use_gitignore = (self.current_path / ".gitignore").exists()
                self.treeview.load_path(self.current_path, use_gitignore=self.use_gitignore)

                # Load config
                config = load_config(self.current_path)
                depth = config.get("depth", 5)
                self.treeview.set_depth(depth)
                self.sidebar.set_depth_slider(depth)

            case "depth":
                self.treeview.set_depth(value)

            case "export":
                self.treeview.export_ascii()

            case _:
                print(f"Unknown command: {command}")

        print(f"[APP] Command received: {command}, value: {value}")
