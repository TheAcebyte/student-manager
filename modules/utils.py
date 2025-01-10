import customtkinter as ctk

from modules.config import *


class Header(ctk.CTkFrame):
    def __init__(self, parent, title: str, underliner: int):
        super().__init__(parent, fg_color="transparent", corner_radius=0)
        self.grid_rowconfigure(0)
        self.grid_rowconfigure(1)
        self.grid_rowconfigure(2)
        self.grid_columnconfigure(0, weight=1)

        self.title = ctk.CTkLabel(
            self,
            text=title,
            text_color=COLORS["indigo-600"],
            fg_color="transparent",
            font=FONTS["header"],
        )
        self.separator = Separator(self, underliner)

        self.title.grid(row=0, column=0, sticky="w")
        self.separator.grid(row=1, column=0, sticky="ew", pady=(4, 16))
        self.pack(side="top", fill="x")


class Separator(ctk.CTkFrame):
    def __init__(self, parent, underliner: int = 0):
        super().__init__(
            parent,
            height=2,
            fg_color=COLORS["gray-200"],
            corner_radius=0,
        )
        self.place(x=0, y=0, relwidth=1.0)

        if underliner != 0:
            self.underliner = ctk.CTkFrame(
                self,
                width=underliner,
                height=2,
                fg_color=COLORS["indigo-600"],
                corner_radius=0,
            )
            self.underliner.place(x=0, y=0)
