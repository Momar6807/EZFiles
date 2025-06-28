import customtkinter as ctk
from components.forminput import FormInput


class Table(ctk.CTkFrame):
    def __init__(self, parent, data=None, on_select=None, headers=("Nombre",),
                 allow_add_new=True, allow_delete=True, input_text="Buscar..."):
        super().__init__(parent, fg_color="#fff")

        self.data = data or []
        self.filtered_data = self.data.copy()
        self.on_select = on_select
        self.headers = headers
        self.allow_add_new = allow_add_new
        self.allow_delete = allow_delete
        self.selected_index = None

        # Buscador
        self.input = FormInput(
            self, placeholder_text=input_text, text_color="black")
        self.input.pack(fill='x', padx=10, pady=(10, 0))
        self.input.bind("<KeyRelease>", self.on_key_release)
        self.input.bind("<Return>", self.on_enter)

        # Tabla scrollable
        self.scroll_frame = ctk.CTkScrollableFrame(
            self, fg_color="#ffffff", corner_radius=12)
        self.scroll_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Botones
        self.button_frame = ctk.CTkFrame(self, fg_color="#fff")
        self.button_frame.pack(pady=(0, 10))

        if self.allow_delete:
            self.delete_button = ctk.CTkButton(
                self.button_frame, text="Eliminar selección", command=self.delete_selected)
            self.delete_button.pack()

        self.build_table()

    def build_table(self):
        # Limpiar contenido previo
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Header
        header = ctk.CTkFrame(self.scroll_frame, fg_color="#f2f2f2", corner_radius=12)
        header.pack(fill='x', pady=(0, 6))

        for col_index, col_name in enumerate(self.headers):
            label = ctk.CTkLabel(
                header,
                text=col_name,
                font=("Segoe UI Emoji", 14, "bold"),
                text_color="black"
            )
            label.grid(row=0, column=col_index, sticky="w", padx=10, pady=6)

        # Filas
        if self.filtered_data:
            for idx, item in enumerate(self.filtered_data):
                row = ctk.CTkFrame(self.scroll_frame, corner_radius=8, fg_color="#ffffff")
                row.pack(fill='x', pady=4)

                # Suponiendo que cada item es texto simple
                cell = ctk.CTkLabel(
                    row,
                    text=item,
                    anchor="w",
                    font=("Segoe UI Emoji", 13),
                    text_color="black"
                )
                cell.pack(fill='x', padx=10, pady=6)

                row.bind("<Button-1>", lambda e, i=idx: self.select_row(i))
                cell.bind("<Button-1>", lambda e, i=idx: self.select_row(i))


    def on_key_release(self, event):
        query = self.input.get().strip().lower()
        self.filtered_data = [
            item for item in self.data if query in item.lower()]
        self.selected_index = None
        self.build_table()

    def on_enter(self, event):
        if not self.allow_add_new:
            return

        query = self.input.get().strip()
        if query and query not in self.data:
            self.data.append(query)
            self.input.delete(0, 'end')
            self.filtered_data = [
                item for item in self.data if query.lower() in item.lower()]
            self.build_table()

    def select_row(self, index):
        self.selected_index = index

        # skip header
        for idx, row in enumerate(self.scroll_frame.winfo_children()[1:]):
            color = "#e0eaff" if idx == index else "#ffffff"
            row.configure(fg_color=color)

        if self.on_select:
            try:
                self.on_select(self.filtered_data[index])
            except IndexError:
                pass

    def get_selected(self):
        if self.selected_index is not None:
            try:
                return self.filtered_data[self.selected_index]
            except IndexError:
                return None
        return None

    def delete_selected(self):
        selected = self.get_selected()
        if selected and selected in self.data:
            self.data.remove(selected)
            self.filtered_data.remove(selected)
            self.selected_index = None
            self.build_table()


if __name__ == "__main__":
    def on_item_selected(item):
        print("Seleccionado:", item)

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.geometry("500x500")
    root.title("Tabla Visual Clara")

    frame = ctk.CTkFrame(root)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    tabla = Table(frame, data=["Manzana", "Banana",
                  "Cereza"], on_select=on_item_selected)
    tabla.pack(fill='both', expand=True)

    root.mainloop()
