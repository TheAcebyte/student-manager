import customtkinter as ctk

from modules.config import *
from modules.utils import *


class EntryHandler(ctk.CTkFrame):
    def __init__(self, parent, manager):
        super().__init__(parent, fg_color="transparent", corner_radius=0)
        self.header = Header(self, "Gestion des fichiers", underliner=168)
        self.handler = FileHandler(self, manager)

        self.grid(row=0, column=0, sticky="ew", pady=(32, 32))


class FileHandler(ctk.CTkFrame):
    def __init__(self, parent, manager):
        super().__init__(parent, fg_color="transparent", corner_radius=0)
        self.grid_rowconfigure(0, weight=1, uniform="#")
        self.grid_columnconfigure((0, 1), weight=1, uniform="#")

        self.loader = LoaderButton(self, manager)
        self.saver = SaverButton(self, manager)

        self.pack(fill="both")


class LoaderButton(ctk.CTkFrame):
    def __init__(self, parent, manager):
        super().__init__(
            parent,
            fg_color="transparent",
            border_width=1,
            border_color=COLORS["gray-200"],
            corner_radius=0,
            cursor="hand2",
        )
        self.manager = manager
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1)

        self.icon_loader = get_icon("handler/folder-open", size=20)
        self.label = ctk.CTkLabel(
            self,
            fg_color="transparent",
            text="Charger",
            text_color=COLORS["zinc-900"],
            font=FONTS["framed"],
            anchor="w",
            cursor="hand2",
        )
        self.icon = ctk.CTkLabel(
            self,
            fg_color="transparent",
            text="",
            font=FONTS["framed"],
            image=self.icon_loader,
            cursor="hand2",
        )

        for widget in (self, self.label, self.icon):
            widget.bind("<Enter>", self.on_enter)
            widget.bind("<Leave>", self.on_leave)
            widget.bind("<Button-1>", self.load)

        self.label.grid(row=0, column=0, sticky="nsew", padx=(16, 1), pady=(1, 1))
        self.icon.grid(row=0, column=1, padx=(1, 16), pady=(1, 1))
        self.grid(row=0, column=0, sticky="nsew", padx=(0, 8), ipady=2)

    def on_enter(self, e):
        self.configure(fg_color=COLORS["gray-100"])

    def on_leave(self, e):
        self.configure(fg_color="transparent")

    def load(self, e):
        self.manager.load_students()


class SaverButton(ctk.CTkFrame):
    def __init__(self, parent, manager):
        super().__init__(
            parent,
            fg_color="transparent",
            border_width=1,
            border_color=COLORS["gray-200"],
            corner_radius=0,
            cursor="hand2",
        )
        self.manager = manager
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1)

        self.icon_saver = get_icon("handler/floppy-disk", size=20)
        self.label = ctk.CTkLabel(
            self,
            fg_color="transparent",
            text="Enregistrer",
            text_color=COLORS["zinc-900"],
            font=FONTS["framed"],
            anchor="w",
            cursor="hand2",
        )
        self.icon = ctk.CTkLabel(
            self,
            fg_color="transparent",
            text="",
            font=FONTS["framed"],
            image=self.icon_saver,
            cursor="hand2",
        )

        for widget in (self, self.label, self.icon):
            widget.bind("<Enter>", self.on_enter)
            widget.bind("<Leave>", self.on_leave)
            widget.bind("<Button-1>", self.load)

        self.label.grid(row=0, column=0, sticky="nsew", padx=(16, 1), pady=(1, 1))
        self.icon.grid(row=0, column=1, padx=(1, 16), pady=(1, 1))
        self.grid(row=0, column=1, sticky="nsew", padx=(8, 0), ipady=2)

    def on_enter(self, e):
        self.configure(fg_color=COLORS["gray-100"])

    def on_leave(self, e):
        self.configure(fg_color="transparent")

    def load(self, e):
        self.manager.save_students()
