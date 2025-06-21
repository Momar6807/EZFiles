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
from tkinter import filedialog, messagebox, ttk
import sys
import os
import shutil
import threading

# Variables globales
selected_origin = None
selected_destination = None



# Para poner el icono a la aplicacion, sin depender del archivo independiente
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Cambios de color en hover
def apply_hover_effect(widget, bg_normal, bg_hover):
    widget.bind("<Enter>", lambda e: widget.config(bg=bg_hover))
    widget.bind("<Leave>", lambda e: widget.config(bg=bg_normal))


#Selección de carpetas y asignación de sus variables
def select_dir(dir_type):
    global selected_origin, selected_destination
    selected = filedialog.askdirectory(title="Selecciona una carpeta")
    if not selected:
        messagebox.showinfo("Info", "No se seleccionó ninguna carpeta.")
        return

    if dir_type == "origin":
        selected_origin = selected
        origin_tag.config(text=f"📁 Origen:\n{selected}")
    elif dir_type == "destination":
        selected_destination = selected
        destination_tag.config(text=f"📂 Destino:\n{selected}")
    update_move_button_state()

#función principal, par mover o copiar los archivos según move_check
def move_files():
    if not selected_origin or not selected_destination:
        messagebox.showwarning("Advertencia", "Selecciona ambas carpetas.")
        return

    archivos = [f for f in os.listdir(selected_origin) if os.path.isfile(
        os.path.join(selected_origin, f))]
    total = len(archivos)

    if total == 0:
        messagebox.showinfo("Info", "No hay archivos para mover.")
        return

    progress["maximum"] = total
    progress["value"] = 0

    def groupFilesByFileType():
        filesByType = {}
        for file in archivos:
            extension = os.path.splitext(file)[1].lower()
            if extension in filesByType:
                filesByType[extension].append(file)
            else:
                filesByType[extension] = [file]
        return filesByType

    def mover():
        groupedFiles = groupFilesByFileType()
        # mover archivos según el tipo de archivo

        for key in groupedFiles.keys():
            for file in groupedFiles[key]:
                final_destination = selected_destination + "/" + key.upper().replace(".", "")
                source_path = os.path.join(selected_origin, file)
                # revisar si existe la carpeta de la extension, sino crearla y continuar
                if not os.path.isdir(final_destination):
                    os.mkdir(final_destination)
                destination_path = os.path.join(
                    final_destination, os.path.basename(file))
                if move_check.get():
                    shutil.move(source_path, destination_path)
                else:
                    shutil.copy(source_path, destination_path)
                progress["value"] += 1

        if (move_check.get()):
            messagebox.showinfo("Éxito", f"Se movieron {total} archivos.")
        else:
            messagebox.showinfo(
                "Éxito", f"Se copiaron {total} archivos.\nRevisa las carpetas generadas y elimina lo que no necesites del origen 🤓")

        progress_label.config(text="✔ Movimiento completado")

    threading.Thread(target=mover).start()



# Para habilitar o inhabilitar el botón de inicio de migración (copiar o mover), para evitar el dialogo de "No seleccionado"
def update_move_button_state():
    if selected_origin and selected_destination:
        move_btn.config(state=tk.NORMAL, bg="#ffc107")
        apply_hover_effect(move_btn, "#ffc107", "#e0a800")
    else:
        move_btn.config(state=tk.DISABLED, bg="#ffc107")
        apply_hover_effect(move_btn, "#f8f9fa", "#575750")


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("EZFiles")
ventana.geometry("700x400")
ventana.configure(bg="#f8f9fa")
ventana.minsize(700, 400)

# icono
ventana.iconbitmap(resource_path('icono.ico'))
# try:
# except:
# pass


# checkbox mover o copiar (False)
style = ttk.Style()
style.map(
    "Bootstrap.TCheckbutton",
    background=[('active', '#007bff'), ('!active', '#f8f9fa')],
    foreground=[('active', 'white'), ('!active', 'black')],
    relief=[('pressed', 'sunken'), ('!pressed', 'raised')]
)

# Configurar el aspecto general
style.configure(
    "Bootstrap.TCheckbutton",
    padding=6,
    relief="raised",
    bordercolor="#007bff",
    background="#f8f9fa",
    foreground="black",
    font=('Helvetica', 10),
    width=15
)
move_check = tk.BooleanVar()
checkbox_move = ttk.Checkbutton(
    ventana,
    text="Mover Archivos",
    variable=move_check,
    onvalue=True,
    offvalue=False,
    style="Bootstrap.TCheckbutton",
)

# Heading
heading = tk.Label(ventana, text="EZFiles - Organizar Archivos", font=("Segoe UI", 16, "bold"),
                   bg="#f8f9fa", fg="#343a40")
heading.pack(pady=(20, 10))

# Frame de botones
button_frame = tk.Frame(ventana, bg="#f8f9fa")
button_frame.pack(pady=10)

# Botón origen
origin_btn = tk.Button(button_frame, text="📁 Carpeta de Origen",
                       command=lambda: select_dir("origin"),
                       bg="#0d6efd", fg="white", relief="flat",
                       font=("Segoe UI", 10, "bold"), padx=10, pady=5)
origin_btn.grid(row=0, column=0, padx=10)
apply_hover_effect(origin_btn, "#0d6efd", "#0b5ed7")

# Botón destino
destination_btn = tk.Button(button_frame, text="📂 Carpeta de Destino",
                            command=lambda: select_dir("destination"),
                            bg="#198754", fg="white", relief="flat",
                            font=("Segoe UI", 10, "bold"), padx=10, pady=5)
destination_btn.grid(row=0, column=1, padx=10)
apply_hover_effect(destination_btn, "#198754", "#157347")

# Botón mover
move_btn = tk.Button(button_frame, text="🚀 Migrar Archivos",
                     command=move_files,
                     bg="#f8f9fa", fg="#212529", relief="flat",
                     font=("Segoe UI", 10, "bold"), padx=10, pady=5,
                     state=tk.DISABLED)
move_btn.grid(row=0, column=2, padx=10)
apply_hover_effect(move_btn, "#f8f9fa", "#f8f9fa")

checkbox_move.pack(pady=10)

# Etiquetas de ruta
origin_tag = tk.Label(ventana, text="🛈 Ninguna ruta de origen seleccionada",
                      bg="#f8f9fa", fg="#212529",
                      wraplength=600, justify="center", font=("Segoe UI", 10))
origin_tag.pack(pady=(20, 5))

destination_tag = tk.Label(ventana, text="🛈 Ninguna ruta de destino seleccionada",
                           bg="#f8f9fa", fg="#212529",
                           wraplength=600, justify="center", font=("Segoe UI", 10))
destination_tag.pack(pady=5)

# Barra de progreso
progress = ttk.Progressbar(
    ventana, orient="horizontal", length=600, mode="determinate")
progress.pack(pady=(20, 5))

# Etiqueta de estado
progress_label = tk.Label(ventana, text="Estado: Esperando acción...",
                          bg="#f8f9fa", fg="#495057", font=("Segoe UI", 10, "italic"))
progress_label.pack()

if __name__ == "__main__":
    # Ejecutar
    ventana.mainloop()
