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

        self.use_gitignore = False

    def handle_command(self, command: str, value=None):
        # Centralise les actions venant de la sidebar
        match command:
            case "import":
                self.current_path = value
                if hasattr(self, "use_gitignore"):
                    self.treeview.load_path(self.current_path, use_gitignore=self.use_gitignore)

            case "depth":
                self.treeview.set_depth(value)

            case "export":
                self.treeview.export_ascii()

            case "gitignore":
                self.use_gitignore = value
                if hasattr(self, "current_path"):
                    self.treeview.load_path(self.current_path, use_gitignore=value)

            case _:
                print(f"Unknown command: {command}")

        print(f"[APP] Command received: {command}, value: {value}")
