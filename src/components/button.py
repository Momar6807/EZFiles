"""
Boton de tk con configuraciones faciles, tomando en cuenta los estilos ya definidos
"""
import tkinter as tk


class Button(tk.Button):
    def __init__(self, master=None, variant="primary", **kwargs):
        super().__init__(master, **kwargs)
        self.config(**kwargs)
        match variant:
            case "primary":
                self.config(bg="#007bff", fg="#fff")
                self.apply_hover_effect("#007bff", "#0069d9")
            case "secondary":
                self.config(bg="#6c757d", fg="#fff")
                self.apply_hover_effect("#6c757d", "#5a6268")
            case "danger":
                self.config(bg="#dc3545", fg="#fff")
                self.apply_hover_effect("#dc3545", "#c82333")
            case "success":
                self.config(bg="#28a745", fg="#fff")
                self.apply_hover_effect("#28a745", "#1e7e34")
            case "warning":
                self.config(bg="#fcc213", fg="#fff")
                self.apply_hover_effect("#fcc213", "#e0a800")
            case "info":
                self.config(bg="#17a2b8", fg="#fff")
                self.apply_hover_effect("#17a2b8", "#138496")
        self.config(relief="flat",
                    font=("Segoe UI Emoji", 10, "bold"), padx=10, pady=5)

    def apply_hover_effect(self, bg_normal, bg_hover):
        self.bind("<Enter>", lambda e: self.config(bg=bg_hover))
        self.bind("<Leave>", lambda e: self.config(bg=bg_normal))
