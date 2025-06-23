"""
En este archivo se crean los componentes de la vista principal del menú de la aplicación, con funciones para su comportamiento, y otra para renderizarlos
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sys
import os
import shutil
import threading
from components.roundedbutton import RoundedButton as Button
from components.label import Label
from components.checkbutton import Checkbutton


# Variables globales
selected_origin = None
selected_destination = None


class MoveFiles:
    def __init__(self, frame):
        self.frame = frame
        pass

    def render(self):

        ###### funciones #######

        # Cambios de color en hover
        def apply_hover_effect(widget, bg_normal, bg_hover):
            widget.bind("<Enter>", lambda e: widget.config(bg=bg_hover))
            widget.bind("<Leave>", lambda e: widget.config(bg=bg_normal))

        # Selección de carpetas y asignación de sus variables
        def select_dir(dir_type):
            global selected_origin, selected_destination
            selected = filedialog.askdirectory(title="Selecciona una carpeta")
            if not selected:
                messagebox.showinfo(
                    "Info", "No se seleccionó ninguna carpeta.")
                return

            if dir_type == "origin":
                selected_origin = selected
                origin_tag.config(text=f"📁 Origen:\n{selected}")
            elif dir_type == "destination":
                selected_destination = selected
                destination_tag.config(text=f"📂 Destino:\n{selected}")

        # función principal, par mover o copiar los archivos según move_check
        def move_files():
            if not selected_origin or not selected_destination:
                messagebox.showwarning(
                    "Advertencia", "Selecciona ambas carpetas.")
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
                    messagebox.showinfo(
                        "Éxito", f"Se movieron {total} archivos.")
                else:
                    messagebox.showinfo(
                        "Éxito", f"Se copiaron {total} archivos.\nRevisa las carpetas generadas y elimina lo que no necesites del origen 🤓")

                progress_label.config(text="✔ Movimiento completado")

            threading.Thread(target=mover).start()

        ############## Creacion de los componentes ################
        move_check = tk.BooleanVar()
        # checkbox_move = ttk.Checkbutton(
        #     self.frame,
        #     text="Mover Archivos",
        #     variable=move_check,
        #     onvalue=True,
        #     offvalue=False,
        #     style="Bootstrap.TCheckbutton",
        # )
        checkbox_move = Checkbutton(self.frame,
                                    text="Mover Archivos",
                                    variable=move_check,
                                    onvalue=True, offvalue=False)

        # Heading
        heading = tk.Label(self.frame, text="Organizar Archivos", font=("Segoe UI Emoji", 16, "bold"),
                           bg="#FBFEF9", fg="#343a40")
        heading.pack(pady=(20, 10))

        # Frame de botones
        button_frame = tk.Frame(self.frame, bg="#FBFEF9")
        button_frame.pack(pady=10)

        # Botón origen
        origin_btn = Button(button_frame,
                            text="📁 Carpeta de Origen",
                            command=lambda: select_dir("origin"),
                            variant="primary")
        origin_btn.grid(row=0, column=0, padx=10)

        # Botón destino
        destination_btn = Button(button_frame, text="📂 Carpeta de Destino",
                                 command=lambda: select_dir("destination"),
                                 variant="success")
        destination_btn.grid(row=0, column=1, padx=10)

        # Botón mover
        move_btn = Button(button_frame, text="🚀 Migrar Archivos",
                          command=move_files,
                          variant="warning")
        move_btn.grid(row=0, column=2, padx=10)

        checkbox_move.pack(pady=10)

        # Etiquetas de ruta
        origin_tag = Label(self.frame, text="🛈 Ninguna ruta de origen seleccionada",
                           wraplength=600)
        origin_tag.pack(pady=(20, 5))

        destination_tag = Label(self.frame, text="🛈 Ninguna ruta de destino seleccionada",
                                wraplength=600)
        destination_tag.pack(pady=5)

        # Barra de progreso
        progress = ttk.Progressbar(
            self.frame, orient="horizontal", length=600, mode="determinate")
        progress.pack(pady=(20, 5))

        # Etiqueta de estado
        progress_label = Label(self.frame, text="Estado: Esperando acción...",
                               bg="#FBFEF9", fg="#495057", font=("Segoe UI Emoji", 10, "italic"))
        progress_label.pack()
