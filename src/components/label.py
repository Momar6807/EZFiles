import tkinter as tk


class Label(tk.Label):
    def __init__(self, master, text, font=("Segoe UI Emoji", 12), justify="center", bg="#FBFEF9", fg="#212529", **kwargs):
        super().__init__(master, text=text, fg=fg,
                         justify=justify, font=font, bg=bg,
                         **kwargs)
