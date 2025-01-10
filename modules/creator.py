import customtkinter as ctk

from modules.config import *
from modules.utils import *


class EntryCreator(ctk.CTkFrame):
    def __init__(self, parent, root):
        super().__init__(parent, fg_color="transparent", corner_radius=0)
        self.root = root

        self.header = Header(self, title="Interface de travail", underliner=158)
        self.input = InputFrame(self, self.add_entry)
        self.grid(row=1, column=0, sticky="ew", pady=(32, 32))

    def add_entry(self, name: str, grade: float):
        self.root.add((name, grade))


class InputFrame(ctk.CTkFrame):
    def __init__(self, parent, parent_action):
        super().__init__(parent, fg_color="transparent", corner_radius=0)
        self.parent_action = parent_action
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure((0, 1), weight=1, uniform="#")

        self.name = NameInput(self)
        self.grade = GradeInput(self)
        self.validate = ValidateButton(self, self.add_entry)

        self.pack(fill="both")

    def add_entry(self):
        name = self.name.input.get()
        grade = self.grade.input.get()

        self.name.input.delete(0, len(name))
        self.grade.input.delete(0, len(grade))
        self.focus()

        matched_name = NAME_MATCHER.fullmatch(name)
        matched_grade = FLOAT_MATCHER.fullmatch(grade)

        if matched_name and matched_grade:
            self.parent_action(name, float(grade))
        else:
            if not matched_name:
                self.name.configure(border_color=COLORS["red-400"])
                self.name.input.configure(
                    placeholder_text="Nom invalide",
                    placeholder_text_color=COLORS["red-400"],
                )
            if not matched_grade:
                self.grade.configure(border_color=COLORS["red-400"])
                self.grade.input.configure(
                    placeholder_text="Note invalide",
                    placeholder_text_color=COLORS["red-400"],
                )


class NameInput(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent",
            border_width=1,
            border_color=COLORS["gray-200"],
            corner_radius=0,
        )
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.input = ctk.CTkEntry(
            self,
            fg_color="transparent",
            text_color=COLORS["zinc-900"],
            placeholder_text="Nom de l'étudiant",
            placeholder_text_color=COLORS["gray-400"],
            font=FONTS["framed"],
            border_width=0,
        )

        self.input.bind("<Button-1>", self.reset_error)

        self.input.grid(row=0, column=0, sticky="nsew", padx=(8, 1), pady=(1, 1))
        self.grid(row=0, column=0, sticky="nsew", padx=(0, 8), ipady=2)

    def reset_error(self, e):
        self.configure(border_color=COLORS["gray-200"])
        self.input.configure(
            placeholder_text="Nom de l'étudiant",
            placeholder_text_color=COLORS["gray-400"],
        )


class GradeInput(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent",
            border_width=1,
            border_color=COLORS["gray-200"],
            corner_radius=0,
        )
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.input = ctk.CTkEntry(
            self,
            fg_color="transparent",
            text_color=COLORS["zinc-900"],
            placeholder_text="Note de l'étudiant",
            placeholder_text_color=COLORS["gray-400"],
            font=FONTS["framed"],
            border_width=0,
        )

        self.input.bind("<Button-1>", self.reset_error)

        self.input.grid(row=0, column=0, sticky="nsew", padx=(8, 1), pady=(1, 1))
        self.grid(row=0, column=1, sticky="nsew", padx=(8, 0), ipady=2)

    def reset_error(self, e):
        self.configure(border_color=COLORS["gray-200"])
        self.input.configure(
            placeholder_text="Note de l'étudiant",
            placeholder_text_color=COLORS["gray-400"],
        )


class ValidateButton(ctk.CTkButton):
    def __init__(self, parent, parent_action):
        super().__init__(
            parent,
            fg_color=COLORS["indigo-600"],
            hover_color=COLORS["indigo-500"],
            text="Ajouter l'étudiant",
            text_color="white",
            font=FONTS["button"],
            corner_radius=4,
            cursor="hand2",
            command=parent_action,
        )

        self.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(16, 0), ipady=4)
