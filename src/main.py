"""Copyright (C) 2025  Omar Martinez @Momar6807

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    """

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import sys
import pystray
from PIL import Image
from movefiles import MoveFiles
from sidebar import Sidebar
from utils.icon import resource_path
# Crear la ventana principal
ventana = tk.Tk()
ventana.title("EZFiles")
ventana.geometry("1000x650")
ventana.configure(bg="#FBFEF9")
ventana.minsize(1000, 650)

# icono
# Para poner el icono a la aplicacion, sin depender del archivo independiente




def minimize_to_tray():
    ventana.withdraw()

def exit_app():
    tray.stop()
    ventana.destroy()
    sys.exit(0)


def show_window():
    ventana.deiconify()


def confirm_exit(self):
    if messagebox.askyesno("Salir", "¿Estás seguro de que quieres salir?"):
        self.exit_app()

ventana.iconbitmap(resource_path('icono.ico'))
# ventana.iconbitmap('icono.ico')
# try:
# except:
# pass


# Configurar el tray
ventana.protocol("WM_DELETE_WINDOW", minimize_to_tray)
tray_icon = Image.open(resource_path('icono.ico'))

menu = pystray.Menu(
    # pystray.MenuItem('Abrir', lambda: minimize_to_tray()),
    pystray.MenuItem('Mostrar', lambda: show_window(), default=True),
    pystray.MenuItem('Salir', lambda: exit_app())
)

tray = pystray.Icon("EZFiles", tray_icon, "EZFiles", menu)

tray_thread = threading.Thread(target=lambda: tray.run(), daemon=True)
tray_thread.start()


# checkbox mover o copiar (False)
style = ttk.Style()
style.map(
    "Bootstrap.TCheckbutton",
    background=[('active', '#007bff'), ('!active', '#FBFEF9')],
    foreground=[('active', 'white'), ('!active', 'black')],
    relief=[('pressed', 'sunken'), ('!pressed', 'raised')]
)

# Configurar el aspecto general
style.configure(
    "Bootstrap.TCheckbutton",
    padding=6,
    relief="raised",
    bordercolor="#007bff",
    background="#FBFEF9",
    foreground="black",
    font=('Helvetica', 10),
    width=15
)


# * Configurar menu
menubar = tk.Menu(ventana)

# Menu Archivo
archivo_menu = tk.Menu(menubar, tearoff=0)
archivo_menu.add_command(label="Salir", command=ventana.quit)

# Menu Preferencias
preferencias_menu = tk.Menu(menubar, tearoff=0)
preferencias_menu.add_command(label="Configuraciones", command=lambda: print(
    "Configuraciones"))  # todo ventana de configuraciones

# Submenu Preferencias > Tema
tema_seleccionado = tk.StringVar()
tema_seleccionado.set("Default")
menu_tema = tk.Menu(menubar, tearoff=0)
menu_tema.add_radiobutton(
    label="Default", variable=tema_seleccionado, value="Default")
menu_tema.add_radiobutton(
    label="Dark (Próximamente)", variable=tema_seleccionado, value="Dark")
preferencias_menu.add_cascade(menu=menu_tema, label="Tema")

# Agregar menus a la barra
menubar.add_cascade(label="Archivo", menu=archivo_menu)
menubar.add_cascade(label="Preferencias", menu=preferencias_menu)
ventana.config(menu=menubar)


# Configurar layout
leftside = tk.Frame(ventana,  width=200)
leftside.pack(side="left", fill="y")

rightside = tk.Frame(ventana, bg="#FBFEF9")
rightside.pack(side="right", fill="both", padx=10, expand=True)


def selectMenuOption(option):
    # limpiar ventana derecha (contenido)
    for widget in rightside.winfo_children():
        widget.destroy()
    match option:
        case "mover":
            # mostrar ventana mover
            page = MoveFiles(rightside)
            page.render()

if __name__ == "__main__":
    # Ejecutar mostrar menu
    menu = Sidebar(
        leftside,
        options=[
            {
                "label": "📁 Organizar Archivos",
                "command": lambda x: selectMenuOption(x),
                "page": "mover"
            },
            # {
            #     "label": "📁 Extraer y aplanar",
            #     "command": lambda x: selectMenuOption(x)
            # },

        ])
    menu.render()
    ventana.mainloop()
