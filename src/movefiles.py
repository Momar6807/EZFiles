import subprocess
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import sys
import os
import shutil
import threading
from tkinter import simpledialog
from components.modal import Modal
from components.roundedbutton import RoundedButton as Button
from components.label import Label
from components.checkbutton import Checkbutton
from components.tooltip import Tooltip
from components.table import Table
import json


class MoveFiles:
    def __init__(self, frame):
        self.frame = frame
        # Obtener categorias guardadas desde el json de saved_categories.json
        # revisar si existe el archivo
        exists = os.path.exists("saved_categories.json")

        # Variables globales
        self.selected_origin = None
        self.selected_destination = None
        self.include_folders = tk.BooleanVar(value=False)
        self.include_categories = tk.BooleanVar(value=True)
        self.open_when_done = tk.BooleanVar(value=False)
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
            selected = filedialog.askdirectory(title="Selecciona una carpeta")
            if not selected:
                messagebox.showinfo(
                    "Info", "No se seleccionó ninguna carpeta.")
                return

            if dir_type == "origin":
                self.selected_origin = selected
                origin_tag.config(text=f"📁 Origen:\n{selected}")
            elif dir_type == "destination":
                self.selected_destination = selected
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
            if not self.selected_origin or not self.selected_destination:
                messagebox.showwarning(
                    "Advertencia", "Selecciona ambas carpetas.")
                return

            archivos = []
            for f in os.listdir(self.selected_origin):
                full_path = os.path.join(self.selected_origin, f)
                if os.path.isfile(full_path):
                    archivos.append(full_path)

            if self.include_categories.get():
                for item in os.listdir(self.selected_origin):
                    full_item_path = os.path.join(self.selected_origin, item)
                    if os.path.isdir(full_item_path):
                        archivos.extend(recursive_file_search(
                            self.selected_origin, item))

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
                if self.include_categories.get():
                    groupedFiles = groupFilesByCategory()
                    for category_name in groupedFiles.keys():
                        for source_path in groupedFiles[category_name]:
                            final_destination = os.path.join(
                                self.selected_destination, category_name)

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
                                        "Error al mover/copiar", f"No se pudo procesar {os.path.basename(source_path)}{" por ser un archivo duplicado" if "are the same file" in str(e) else ": " + str(e)}\n\n¿Deseas omitir los errores y continuar? (Solo se organizarán los archivos que no tengan errores)")
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
                                self.selected_destination, extension_name.upper().replace(".", ""))

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
                                        "Error al mover/copiar", f"No se pudo procesar {os.path.basename(source_path)}{" por ser un archivo duplicado" if "are the same file" in str(e) else ": " + str(e)}\n\n¿Deseas omitir los errores y continuar? (Solo se organizarán los archivos que no tengan errores)")
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
                if (self.open_when_done.get()):
                    subprocess.Popen(["explorer", self.selected_destination])
            threading.Thread(target=mover).start()

        def save_categories():
            with open("saved_categories.json", "w") as f:
                # Añadido indent para mejor legibilidad del JSON
                json.dump(self.categories, f, indent=4)

        def delete_category(event):
            # Obtener el ítem seleccionado con el clic derecho
            selected_item_id = categories_treeview.identify_row(event.y)
            if not selected_item_id:
                return

            category_name = categories_treeview.item(selected_item_id)['text']
            if category_name in self.categories:
                if messagebox.askyesno("Eliminar Categoría", f"¿Estás seguro de que quieres eliminar la categoría '{category_name}'?"):
                    del self.categories[category_name]
                    save_categories()
                    populate_categories_treeview(categories_treeview)
                    # Limpiar extensiones al eliminar categoría
                    populate_extensions_treeview(extensions_treeview, None)
            else:
                messagebox.showwarning(
                    "Advertencia", "No se pudo encontrar la categoría seleccionada.")

        def delete_extension(event):
            selected_extension_id = extensions_treeview.identify_row(event.y)
            if not selected_extension_id:
                return

            extension_name = extensions_treeview.item(
                selected_extension_id)['text']
            selected_category_id = categories_treeview.selection()
            if not selected_category_id:
                messagebox.showwarning(
                    "Advertencia", "Selecciona primero una categoría.")
                return

            category_name = categories_treeview.item(
                selected_category_id[0])['text']

            if category_name in self.categories and extension_name in self.categories[category_name]:
                if messagebox.askyesno("Eliminar Extensión", f"¿Estás seguro de que quieres eliminar la extensión '{extension_name}' de la categoría '{category_name}'?"):
                    self.categories[category_name].remove(extension_name)
                    save_categories()
                    populate_extensions_treeview(
                        extensions_treeview, category_name)
            else:
                messagebox.showwarning(
                    "Advertencia", "No se pudo encontrar la extensión o categoría seleccionada.")

        def populate_categories_treeview(widget):
            # Limpiar el treeview antes de poblarlo
            for i in widget.get_children():
                widget.delete(i)
            for category in self.categories:
                widget.insert(
                    "",
                    "end",
                    text=category,
                    iid=category
                )

        def populate_extensions_treeview(widget, category):
            # Limpiar el treeview de extensiones antes de poblarlo
            for i in widget.get_children():
                widget.delete(i)

            if category and category in self.categories:
                for extension in self.categories[category]:
                    widget.insert(
                        "",  # Parent item
                        "end",
                        text=extension,
                        iid=extension,
                    )

        ############## Creacion de los componentes ################
        move_check = tk.BooleanVar()

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
        move_btn = Button(button_frame, text="🚀 Comenzar",
                          command=move_files,
                          variant="warning")
        move_btn.grid(row=0, column=2, padx=10)

        # Contenedor para configuraciones (checkboxes y treeviews)
        config_container = tk.Frame(self.frame, bg="#FBFEF9")
        config_container.pack(pady=10, padx=10, fill="both", expand=True)

        # Configurar las columnas para que distribuyan el espacio
        config_container.grid_columnconfigure(0, weight=1)  # Checkboxes
        config_container.grid_columnconfigure(
            1, weight=2)  # Treeview de categorías
        config_container.grid_columnconfigure(
            2, weight=2)  # Treeview de extensiones

        # Frame para los checkboxes (columna 0)
        checkbox_frame = tk.Frame(config_container, bg="#FBFEF9")
        checkbox_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=5)

        # Checkbox para incluir categorías
        checkbox_include_categories = Checkbutton(
            checkbox_frame,
            text="Incluir categorías",
            variable=self.include_categories,
            onvalue=True,
            offvalue=False,
        )
        checkbox_include_categories.pack(anchor="w")
        Tooltip(
            checkbox_include_categories,
            "Si seleccionas esta opción, se organizarán los archivos en carpetas por categoría."
            "\n\nSi no, se organizarán todos los archivos en carpetas con el nombre de la extensión."
            "\n(e.g PNG, PDF, etc.)"
        )

        # Checkbox mover o copiar
        checkbox_move = Checkbutton(checkbox_frame,
                                    text="Mover Archivos",
                                    variable=move_check,
                                    onvalue=True, offvalue=False)
        checkbox_move.pack(anchor="w")
        Tooltip(
            checkbox_move,
            "Si seleccionas esta opción, se moverán los archivos a la carpeta de destino."
            "\n\nSi no, se copiarán los archivos a la carpeta de destino, sin alterar los archivos originales."
        )

        # Checkbox abrir al finalizar
        checkbox_open = Checkbutton(checkbox_frame,
                                    text="Abrir al finalizar",
                                    variable=self.open_when_done,
                                    onvalue=True, offvalue=False)
        checkbox_open.pack(anchor="w")

        # Texto para indicar como eliminar
        delete_text = tk.Label(
            config_container,
            text="🛈 Para agregar categorias o extensiones, ingresa el nombre en el buscador y presiona enter" \
                "\n🛈 Para eliminar, haz click en un elemento y presiona el botón para eliminar",  # Texto actualizado
            bg="#FBFEF9",
            fg="#343a40",
            font=("Segoe UI Emoji", 10),
        )
        delete_text.grid(row=1, column=1, columnspan=2, pady=1)

       # Contenedor para las dos tablas (categorías y extensiones)
        tables_frame = ctk.CTkFrame(config_container, fg_color="white")
        tables_frame.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Variable para rastrear categoría seleccionada
        selected_category = {"name": None}

        # Función para actualizar extensiones
        def update_extensions_table(category):
            selected_category["name"] = category
            extensions = self.categories.get(category, [])
            extensions_table.data = extensions.copy()
            extensions_table.filtered_data = extensions.copy()
            extensions_table.selected_index = None
            extensions_table.build_table()

        # Función para manejar eliminación de categoría
        def on_delete_category(item):
            if item in self.categories:
                if messagebox.askyesno("Eliminar Categoría", f"¿Eliminar la categoría '{item}'?"):
                    del self.categories[item]
                    save_categories()
                    categories_table.data.remove(item)
                    categories_table.filtered_data.remove(item)
                    categories_table.build_table()
                    update_extensions_table(None)

        # Función para manejar eliminación de extensión
        def on_delete_extension(item):
            category = selected_category["name"]
            if not category:
                return
            if item in self.categories.get(category, []):
                if messagebox.askyesno("Eliminar Extensión", f"¿Eliminar la extensión '{item}' de '{category}'?"):
                    self.categories[category].remove(item)
                    save_categories()
                    update_extensions_table(category)

        # Tabla de categorías
        categories_table = Table(
            tables_frame,
            headers=["Categorías"],
            data=list(self.categories.keys()),
            on_select=update_extensions_table,
            allow_add_new=True,
            allow_delete=True,
            input_text="Buscar categoría..."
        )
        categories_table.pack(side="left", expand=True, fill="both", padx=(0, 10))

        # Tabla de extensiones
        extensions_table = Table(
            tables_frame,
            headers=["Extensiones",],
            data=[],
            on_select=None,
            allow_add_new=True,
            allow_delete=True,
            input_text="Buscar extensión..."
        )
        extensions_table.pack(side="left", expand=True, fill="both", padx=(10, 0))

        # Conectar eliminaciones
        categories_table.on_delete = on_delete_category
        extensions_table.on_delete = on_delete_extension


        #! Demás contenido
        # Etiquetas de ruta
        origin_tag = Label(self.frame, text="🛈 Ninguna ruta de origen seleccionada",
                           wraplength=600)
        origin_tag.pack(pady=(5, 5))

        destination_tag = Label(self.frame, text="🛈 Ninguna ruta de destino seleccionada",
                                wraplength=600)
        destination_tag.pack(pady=0)

        # Barra de progreso
        progress = ttk.Progressbar(
            self.frame, orient="horizontal", length=600, mode="determinate")
        progress.pack(pady=5)

        # Etiqueta de estado
        progress_label = Label(self.frame, text="Estado: Esperando acción...",
                               bg="#FBFEF9", fg="#495057", font=("Segoe UI Emoji", 10, "italic"))
        progress_label.pack(pady=(0, 20))
