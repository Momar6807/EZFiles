import tkinter as tk
from tkinter import font as tkfont


class RoundedButtonOld(tk.Canvas):
    def __init__(self, master=None, text="", variant="primary", radius=15, padding=10, command=None, **kwargs):
        super().__init__(master, highlightthickness=0, bg=master["bg"])

        self.radius = radius
        self.padding = padding
        self.command = command
        self.text = text
        self.kwargs = kwargs

        # Define estilos
        variants = {
            "primary": ("#007bff", "#0069d9"),
            "secondary": ("#6c757d", "#5a6268"),
            "danger": ("#dc3545", "#c82333"),
            "success": ("#28a745", "#1e7e34"),
            "warning": ("#fcc213", "#e0a800"),
            "info": ("#17a2b8", "#138496")
        }

        self.bg_color, self.hover_color = variants.get(
            variant, ("#007bff", "#0069d9"))
        self.fg_color = "#ffffff"
        self.font = tkfont.Font(family="Segoe UI Emoji",
                                size=10, weight="bold")

        self.button_id = None
        self.text_id = None

        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

        # Inicializar tamaño
        self.update_size_and_draw()

    def update_size_and_draw(self):
        text_width = self.font.measure(self.text)
        text_height = self.font.metrics("linespace")

        total_width = text_width + self.padding * 2
        total_height = text_height + self.padding

        self.config(width=total_width, height=total_height)
        self.draw_button(total_width, total_height)

    def draw_button(self, width, height):
        self.delete("all")
        r = self.radius
        self.button_id = self.create_round_rect(
            0, 0, width, height, r, fill=self.bg_color, outline="")
        self.text_id = self.create_text(width // 2, height // 2, text=self.text,
                                        fill=self.fg_color, font=self.font)

    def create_round_rect(self, x1, y1, x2, y2, r=25, **kwargs):
        return self.create_polygon([
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1
        ], smooth=True, **kwargs)

    def on_click(self, event):
        if self.command:
            self.command()

    def on_hover(self, event):
        self.itemconfig(self.button_id, fill=self.hover_color)

    def on_leave(self, event):
        self.itemconfig(self.button_id, fill=self.bg_color)


if __name__ == "__main__":
    def test():
        print("¡Haz hecho clic!")

    root = tk.Tk()
    root.configure(bg="#f8f9fa")

    btn1 = RoundedButton(root, text="Aceptar", variant="success",
                         radius=20, padding=12, command=test)
    btn1.pack(padx=20, pady=10)

    btn2 = RoundedButton(root, text="Cancelar operación",
                         variant="danger", radius=15, padding=15, command=test)
    btn2.pack(padx=20, pady=10)

    root.mainloop()


"""
Botón de CustomTkinter con configuraciones fáciles y estilos predefinidos
"""
import customtkinter as ctk


class RoundedButton(ctk.CTkButton):
    def __init__(self, master=None, variant="primary", width=200, height=40, **kwargs):
        # Configuración de apariencia general de CustomTkinter
        ctk.set_appearance_mode("system")  # Puedes cambiar a "light" o "dark"
        ctk.set_default_color_theme("blue")  # Temas: blue, green, dark-blue

        super().__init__(master, **kwargs)

        # Configuraciones comunes para todos los botones
        common_settings = {
            "font": ("Segoe UI Emoji", 14, "bold"),
            "corner_radius": 8,
            "border_width": 1,
            "text_color": ("#ffffff", "#ffffff"),
            "hover": True,
            "width": width, "height": height,
        }

        # Configuraciones específicas por variante
        match variant:
            case "primary":
                colors = {
                    "fg_color": ("#3a7ebf", "#1f538d"),
                    "hover_color": ("#325882", "#14375e"),
                    "border_color": ("#3a7ebf", "#1f538d")
                }
            case "secondary":
                colors = {
                    "fg_color": ("#6c757d", "#565e64"),
                    "hover_color": ("#5a6268", "#484e53"),
                    "border_color": ("#6c757d", "#565e64")
                }
            case "danger":
                colors = {
                    "fg_color": ("#dc3545", "#a71d2a"),
                    "hover_color": ("#c82333", "#8a1a24"),
                    "border_color": ("#dc3545", "#a71d2a")
                }
            case "success":
                colors = {
                    "fg_color": ("#28a745", "#1e7e34"),
                    "hover_color": ("#218838", "#186429"),
                    "border_color": ("#28a745", "#1e7e34")
                }
            case "warning":
                colors = {
                    "fg_color": ("#ffc107", "#d39e00"),
                    "hover_color": ("#e0a800", "#b38c00"),
                    "border_color": ("#ffc107", "#d39e00"),
                    # Texto negro para mejor contraste
                    "text_color": ("#ffffff", "#ffffff")
                }
            case "info":
                colors = {
                    "fg_color": ("#17a2b8", "#117a8b"),
                    "hover_color": ("#138496", "#0e6674"),
                    "border_color": ("#17a2b8", "#117a8b")
                }
            case _:  # default
                colors = {
                    "fg_color": ("#3a7ebf", "#1f538d"),
                    "hover_color": ("#325882", "#14375e"),
                    "border_color": ("#3a7ebf", "#1f538d")
                }

        # Combinar configuraciones comunes con las específicas
        final_settings = {**common_settings, **colors, **kwargs}

        # Aplicar todas las configuraciones
        self.configure(**final_settings)
