import customtkinter as ctk
from components.forminput import FormInput


class Table(ctk.CTkFrame):
    def __init__(self, parent, data=None, on_select=None, on_add=None, on_delete=None, headers=("Nombre",),
                 allow_add_new=True, allow_delete=True, input_text="Buscar..."):
        super().__init__(parent, fg_color="#fff")

        self.data = data or []
        self.filtered_data = self.data.copy()
        self.on_select = on_select
        self.on_add = on_add
        self.on_delete = on_delete
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
        header = ctk.CTkFrame(
            self.scroll_frame, fg_color="#f2f2f2", corner_radius=12)
        header.pack(fill='x', pady=(0, 6))

        for col_index, col_name in enumerate(self.headers):
            label = ctk.CTkLabel(
                header,
                text=col_name,
                font=("Segoe UI Emoji", 14, "bold"),
                text_color="black"
            )
            label.grid(row=0, column=col_index, sticky="w", padx=10, pady=6)

        # Filas de datos
        if self.filtered_data:
            for idx, item in enumerate(self.filtered_data):
                row = ctk.CTkFrame(self.scroll_frame,
                                   corner_radius=8, fg_color="#ffffff")
                row.pack(fill='x', pady=4)

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

        # Hint row for adding new items
        if self.allow_add_new:
            query = self.input.get().strip()
            # Only show hint if there's something typed and it's not already in data
            if query and query.lower() not in [d.lower() for d in self.data]:
                hint_row = ctk.CTkFrame(
                    self.scroll_frame, corner_radius=8, fg_color="#f0f0f0")  # Lighter background
                hint_row.pack(fill='x', pady=4)

                hint_label = ctk.CTkLabel(
                    hint_row,
                    text=f"Presiona Enter para agregar '{query}\"",
                    anchor="w",
                    font=("Segoe UI Emoji", 12, "italic"),  # Italic font
                    text_color="#888888"  # Greyed out text
                )
                hint_label.pack(fill='x', padx=10, pady=6)
                # Do NOT bind select_row to the hint row, it's not selectable

    def on_key_release(self, event):
        query = self.input.get().strip().lower()
        self.filtered_data = [
            item for item in self.data if query in item.lower()]
        self.selected_index = None
        self.build_table()  # Rebuild table to show/hide hint row

    def on_enter(self, event):
        if not self.allow_add_new:
            return

        query = self.input.get().strip()
        if query and query not in self.data:
            self.data.append(query)
            self.input.delete(0, 'end')
            # After adding, clear the filter and rebuild to show all data including new item
            self.filtered_data = self.data.copy()
            self.build_table()
            if self.on_add:
                self.on_add(query)
        else:  # If query is empty or item already exists, still rebuild to clear hint
            self.build_table()

    def select_row(self, index):
        self.selected_index = index

        # skip header
        for idx, row in enumerate(self.scroll_frame.winfo_children()[1:]):
            color = "#e0eaff" if idx == index else "#ffffff"
            # Ensure we don't try to configure the hint row if it exists at the end
            # and it's not the one selected (which it shouldn't be).
            # This relies on the hint row being the last element if present.
            if len(self.filtered_data) > idx:  # Only apply selection color to data rows
                row.configure(fg_color=color)
            else:  # This is potentially the hint row
                row.configure(fg_color="#f0f0f0")  # Reset its color

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
            if self.on_delete:
                self.on_delete(selected)
            else:
                self.data.remove(selected)
                self.filtered_data.remove(selected)
                self.selected_index = None
                self.build_table()
        # Rebuild table to update hint row visibility after deletion
        self.build_table()
