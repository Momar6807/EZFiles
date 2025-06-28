import customtkinter as ctk


class FormInput(ctk.CTkEntry):
    def __init__(self, master=None, placeholder_text="", **kwargs):
        super().__init__(master, placeholder_text=placeholder_text, fg_color="#ffffff", placeholder_text_color="black", **kwargs)