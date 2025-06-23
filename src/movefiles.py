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
import json


# Variables globales
selected_origin = None
selected_destination = None
include_folders = False
include_categories = True


class MoveFiles:
    def __init__(self, frame):
        self.frame = frame
        # Obtener categorias guardadas desde el json de saved_categories.json
        # revisar si existe el archivo
        exists = os.path.exists("saved_categories.json")
        if exists:
            with open("saved_categories.json", "r") as f:
                self.categories = json.load(f)
        else:
            # crear un archivo con las categorias por defecto (Imagenes, documentos, hojas de cálculo, etc.)
            self.categories = {
                "Imagenes": ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg'],
                "Documentos": ['.doc', '.docx', '.pdf', '.ppt', '.pptx'],
                "Audio": ['.mp3', '.wav', '.ogg', '.flac'],
                "Video": ['.mp4', '.avi', '.mkv'],
                "Hojas de cálculo": ['.csv', '.xlsx', '.xls'],
                "Diseños e Ilustraciones": ['.ai', '.psd', '.eps'],
                "Archivos de texto": ['.txt', '.md', '.html', '.css', '.js', '.json'],
                "Ejecutables": ['.exe', '.msi', '.bat'],
                "Archivos comprimidos": ['.zip', '.rar', '.7z'],
                "Código fuente y Scripts": ['.py', '.js', '.html', '.css', '.json',
                                            '.php', '.java', '.lua', '.r', '.c', '.cpp', '.cs',
                                            '.go', '.swift', '.kt', '.kts', '.csx', '.csproj',
                                            '.ino', '.asm', '.h', '.cob', '.jsx', '.ts', '.tsx', '.dart', '.e', '.f'],
                "Otros": []  # La categoría "Otros" no necesita extensiones predefinidas
            }
            with open("saved_categories.json", "w") as f:
                json.dump(self.categories, f)

    def render(self):

        ###### funciones #######

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

        def recursive_file_search(base_path, current_folder):
            files = []
            full_current_path = os.path.join(base_path, current_folder)
            for item in os.listdir(full_current_path):
                item_full_path = os.path.join(full_current_path, item)
                if os.path.isfile(item_full_path):
                    files.append(item_full_path)
                elif os.path.isdir(item_full_path):
                    files.extend(recursive_file_search(
                        base_path, os.path.join(current_folder, item)))
            return files
        # función principal, par mover o copiar los archivos según move_check

        def move_files():
            if not selected_origin or not selected_destination:
                messagebox.showwarning(
                    "Advertencia", "Selecciona ambas carpetas.")
                return

            archivos = []
            for f in os.listdir(selected_origin):
                full_path = os.path.join(selected_origin, f)
                if os.path.isfile(full_path):
                    archivos.append(full_path)

            if include_categories:
                for item in os.listdir(selected_origin):
                    full_item_path = os.path.join(selected_origin, item)
                    if os.path.isdir(full_item_path):
                        archivos.extend(recursive_file_search(
                            selected_origin, item))

            total = len(archivos)

            if total == 0:
                messagebox.showinfo("Info", "No hay archivos para mover.")
                return

            progress["maximum"] = total
            progress["value"] = 0

            def groupFilesByFileType():
                filesByType = {}
                for full_file_path in archivos:
                    extension = os.path.splitext(full_file_path)[1].lower()
                    if extension in filesByType:
                        filesByType[extension].append(full_file_path)
                    else:
                        filesByType[extension] = [full_file_path]
                return filesByType

            def groupFilesByCategory():
                filesByCategory = {}
                for full_file_path in archivos:
                    extension = os.path.splitext(full_file_path)[1].lower()
                    found_category = False
                    for key in self.categories.keys():
                        if extension in self.categories[key]:
                            if key in filesByCategory:
                                filesByCategory[key].append(full_file_path)
                            else:
                                filesByCategory[key] = [full_file_path]
                            found_category = True
                            break
                    if not found_category:
                        if "Otros" in filesByCategory:
                            filesByCategory["Otros"].append(full_file_path)
                        else:
                            filesByCategory["Otros"] = [full_file_path]
                return filesByCategory

            def mover():
                nonlocal total
                errors = []
                omit_errors = False
                if include_categories:
                    groupedFiles = groupFilesByCategory()
                    for category_name in groupedFiles.keys():
                        for source_path in groupedFiles[category_name]:
                            final_destination = os.path.join(
                                selected_destination, category_name)

                            if not os.path.isdir(final_destination):
                                os.makedirs(final_destination)

                            destination_path = os.path.join(
                                final_destination, os.path.basename(source_path))

                            try:
                                if move_check.get():
                                    shutil.move(source_path, destination_path)
                                else:
                                    shutil.copy(source_path, destination_path)
                                progress["value"] += 1
                                progress_label.config(
                                    text=f"Procesando: {os.path.basename(source_path)}")
                            except Exception as e:
                                if not omit_errors:
                                    omit_errors = messagebox.askyesno(
                                        "Error al mover/copiar", f"No se pudo procesar {os.path.basename(source_path)}{" por ser un archivo duplicado" if "are the same file" in str(e) else ": " + str(e)}\n\n¿Deseas omitir los errores y continuar? (Solo se migrarán los archivos que no tengan errores)")
                                total -= 1
                                if "are the same file" in str(e):
                                    errors.append(
                                        f"{os.path.basename(source_path)}: Archivo duplicado")
                                else:
                                    errors.append(
                                        f"{os.path.basename(source_path)}: {e}")
                                pass  # Continuar
                            self.frame.update_idletasks()

                    if (move_check.get()):
                        messagebox.showinfo(
                            "Éxito", f"Se movieron {total} archivos."
                            + (f"\nErrores: {', \n'.join(errors)}" if len(errors) > 0 else ""))
                    else:
                        messagebox.showinfo(
                            "Éxito", f"Se copiaron {total} archivos.\nRevisa las carpetas generadas y elimina lo que no necesites del origen 🤓"
                            + (f"\nErrores: {', \n'.join(errors)}" if len(errors) > 0 else ""))

                    progress_label.config(text="✔ Movimiento completado")
                    progress["value"] = total
                    progress["maximum"] = total
                    progress_label.config(text="✔ Movimiento completado")
                else:
                    # mover archivos según el tipo de archivo (similar adjustments)
                    groupedFiles = groupFilesByFileType()
                    for extension_name in groupedFiles.keys():
                        for source_path in groupedFiles[extension_name]:
                            final_destination = os.path.join(
                                selected_destination, extension_name.upper().replace(".", ""))

                            if not os.path.isdir(final_destination):
                                os.makedirs(final_destination)

                            destination_path = os.path.join(
                                final_destination, os.path.basename(source_path))

                            try:
                                if move_check.get():
                                    shutil.move(source_path, destination_path)
                                else:
                                    shutil.copy(source_path, destination_path)
                                progress["value"] += 1
                                progress_label.config(
                                    text=f"Procesando: {os.path.basename(source_path)}")
                            except Exception as e:
                                if not omit_errors:
                                    omit_errors = messagebox.askyesno(
                                        "Error al mover/copiar", f"No se pudo procesar {os.path.basename(source_path)}{" por ser un archivo duplicado" if "are the same file" in str(e) else ": " + str(e)}\n\n¿Deseas omitir los errores y continuar? (Solo se migrarán los archivos que no tengan errores)")
                                total -= 1
                                if "are the same file" in str(e):
                                    errors.append(
                                        f"{os.path.basename(source_path)}: Archivo duplicado")
                                else:
                                    errors.append(
                                        f"{os.path.basename(source_path)}: {e}")
                                pass  # Continuar
                            self.frame.update_idletasks()

                    if (move_check.get()):
                        messagebox.showinfo(
                            "Éxito", f"Se movieron {total} archivos."
                            + (f"\nErrores: {', \n'.join(errors)}" if len(errors) > 0 else ""))
                    else:
                        messagebox.showinfo(
                            "Éxito", f"Se copiaron {total} archivos.\nRevisa las carpetas generadas y elimina lo que no necesites del origen 🤓\n\n"
                            + (f"\nErrores: {', \n'.join(errors)}" if len(errors) > 0 else ""))

                    progress_label.config(text="✔ Movimiento completado")
                print(errors)
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
