import customtkinter as ctk

from treefy.gui.app import TreefyApp


def main():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    app = TreefyApp()
    app.mainloop()


if __name__ == "__main__":
    main()
