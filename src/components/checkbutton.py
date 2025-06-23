import tkinter as tk
from tkinter import ttk


class Checkbutton(ttk.Checkbutton):
    def __init__(self, master=None, text="", variable=None, command=None, **kwargs):
        self.style_name = "Bootstrap.TCheckbutton"
        style = ttk.Style(master)
        if not self.style_name in style.theme_names():
            style.configure(self.style_name,
                            font=("Segoe UI", 10),
                            background="#f8f9fa",
                            foreground="#212529",
                            focuscolor="#f8f9fa",
                            padding=6)
            style.map(self.style_name,
                      background=[("active", "#e2e6ea")],
                      foreground=[("active", "#212529")],
                      indicatorcolor=[("selected", "#0d6efd"),
                                      ("!selected", "#adb5bd")],
                      indicatorbackground=[("selected", "#0d6efd"), ("!selected", "#f8f9fa")])

        super().__init__(master,
                         text=text,
                         variable=variable,
                         command=command,
                         style=self.style_name,
                         **kwargs)

        self.configure(takefocus=False)
