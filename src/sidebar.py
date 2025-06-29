"""
Lado izquierdo de la aplicación, con las paginas disponibles
"""


import tkinter as tk
from tkinter import ttk
from components.roundedbutton import RoundedButton as Button


class Sidebar:
    def __init__(self, frame: tk.Frame, options: list[dict]):
        self.frame = frame
        self.frame.config(bg="#1e2e38")
        self.options = options

    def render(self):
        ttk.Label(master=self.frame,
                  text="Menú",
                  font=("Segoe UI Emoji", 14, "bold"),
                  background="#1e2e38",
                  padding=(10, 10, 10, 10),
                  foreground="white").pack()
        for option in self.options:
            Button(master=self.frame,
                   variant="info", text=option["label"],
                   command=lambda: option["command"](option["page"])).pack(pady=5, padx=5)
