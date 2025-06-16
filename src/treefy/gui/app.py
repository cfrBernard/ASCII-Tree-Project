import customtkinter as ctk

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

    def handle_command(self, command: str, value=None):
        # Centralise les actions venant de la sidebar
        match command:
            case "import":
                path = value
                self.treeview.load_path(path)

            case "depth":
                self.treeview.set_depth(value)

            case "export":
                self.treeview.export_ascii()

            case _:
                print(f"Unknown command: {command}")
