import customtkinter as ctk

from modules.config import *
from modules.utils import *


class EntryViewer(ctk.CTkFrame):
    def __init__(self, parent, manager):
        super().__init__(parent, fg_color="transparent", corner_radius=0)
        self.manager = manager

        self.header = Header(self, "Liste d'étudiants", 140)
        self.stats = StatFrame(self)
        self.search = SearchFrame(self, manager)
        self.table = TableFrame(self, manager)

        self.grid(row=2, column=0, sticky="nsew", pady=(32, 32))

    def refresh(self):
        self.refresh_stats()
        self.refresh_table()

    def refresh_stats(self):
        n = len(self.manager.list)
        if n == 0:
            self.stats.total.variable.set("0")
            self.stats.mean.variable.set("0.0")
        else:
            mean = 0
            for name, grade in self.manager.list:
                mean += grade

            mean /= n
            self.stats.total.variable.set(f"{n}")
            self.stats.mean.variable.set(f"{mean:.2f}")

    def refresh_table(self):
        self.table.pack_forget()
        self.table.destroy()
        self.table = TableFrame(self, self.manager)


class StatFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent", corner_radius=0)
        self.grid_rowconfigure(0, weight=1, uniform="#")
        self.grid_columnconfigure((0, 1), weight=1, uniform="#")

        self.total = TotalStat(self)
        self.mean = MeanStat(self)

        self.pack(fill="x")


class TotalStat(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent",
            border_width=1,
            border_color=COLORS["gray-200"],
            corner_radius=0,
        )
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.variable = ctk.StringVar(self, "0")
        self.label = ctk.CTkLabel(
            self,
            fg_color="transparent",
            text="Nombre d'étudiants",
            text_color=COLORS["gray-500"],
            font=FONTS["framed"],
            anchor="w",
        )
        self.value = ctk.CTkLabel(
            self,
            fg_color="transparent",
            textvariable=self.variable,
            text_color=COLORS["zinc-900"],
            font=FONTS["framed"],
        )

        self.label.grid(row=0, column=0, sticky="nsew", padx=(16, 1), pady=(1, 1))
        self.value.grid(row=0, column=1, padx=(1, 16), pady=(1, 1))
        self.grid(row=0, column=0, sticky="nsew", padx=(0, 8), ipady=2)


class MeanStat(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent",
            border_width=1,
            border_color=COLORS["gray-200"],
            corner_radius=0,
        )
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.variable = ctk.StringVar(self, "0.0")
        self.label = ctk.CTkLabel(
            self,
            fg_color="transparent",
            text="Moyenne générale",
            text_color=COLORS["gray-500"],
            font=FONTS["framed"],
            anchor="w",
        )
        self.value = ctk.CTkLabel(
            self,
            fg_color="transparent",
            textvariable=self.variable,
            text_color=COLORS["zinc-900"],
            font=FONTS["framed"],
        )

        self.label.grid(row=0, column=0, sticky="nsew", padx=(16, 1), pady=(1, 1))
        self.value.grid(row=0, column=1, padx=(1, 16), pady=(1, 1))
        self.grid(row=0, column=1, sticky="nsew", padx=(8, 0), ipady=2)


class SearchFrame(ctk.CTkFrame):
    def __init__(self, parent, manager):
        super().__init__(parent, fg_color="transparent", corner_radius=0)
        self.grid_rowconfigure(0)
        self.grid_columnconfigure(0, weight=1)

        self.name = SearchInput(self, manager)
        self.pack(side="top", fill="x", pady=(16, 0))


class SearchInput(ctk.CTkFrame):
    def __init__(self, parent, manager):
        super().__init__(
            parent,
            fg_color="transparent",
            border_width=1,
            border_color=COLORS["gray-200"],
            corner_radius=0,
        )
        self.manager = manager
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1)

        self.icon_search = get_icon("table/magnifying-glass", size=20)

        self.input = ctk.CTkEntry(
            self,
            fg_color="transparent",
            text_color=COLORS["zinc-900"],
            placeholder_text="Rechercher un étudiant",
            placeholder_text_color=COLORS["gray-400"],
            font=FONTS["framed"],
            border_width=0,
        )
        self.icon = ctk.CTkLabel(
            self,
            fg_color="transparent",
            text="",
            font=FONTS["framed"],
            image=self.icon_search,
            cursor="hand2",
        )

        self.input.bind("<Return>", self.search_entry)
        self.icon.bind("<Button-1>", self.search_entry)

        self.input.grid(row=0, column=0, sticky="nsew", padx=(8, 4), pady=(1, 1))
        self.icon.grid(row=0, column=1, padx=(4, 16), pady=(1, 1))
        self.grid(row=0, column=0, sticky="nsew", ipady=2)

    def search_entry(self, e):
        query = self.input.get()
        self.input.delete(0, len(query))
        self.focus()
        self.manager.search(query)


class TableFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, manager):
        super().__init__(
            parent,
            fg_color="transparent",
            border_width=1,
            border_color=COLORS["gray-200"],
            scrollbar_button_color=COLORS["gray-300"],
            scrollbar_button_hover_color=COLORS["gray-400"],
            corner_radius=0,
        )
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.header = TableHeader(self, manager)

        j = 0
        for i, (name, grade) in enumerate(manager.list):
            if j >= len(manager.filtered):
                break
            
            query_name, query_grade = manager.filtered[j]
            if name == query_name and grade == query_grade:
                j += 1
                TableEntry(self, manager, i, j, name, grade)

        self.pack(expand=True, fill="both", pady=(16, 0))


class TableHeader:
    def __init__(self, parent, manager):
        self.manager = manager
        
        self.name = ctk.CTkLabel(
            parent,
            fg_color="transparent",
            text="Nom",
            text_color=COLORS["gray-400"],
            font=FONTS["framed"],
            anchor="w",
            cursor="hand2"
        )

        self.grade = ctk.CTkLabel(
            parent,
            fg_color="transparent",
            text="Note",
            text_color=COLORS["gray-400"],
            font=FONTS["framed"],
            anchor="w",
            cursor="hand2"
        )

        self.option = ctk.CTkLabel(
            parent,
            fg_color="transparent",
            text="Options",
            text_color=COLORS["gray-400"],
            font=FONTS["framed"],
            anchor="w",
        )
        
        self.name.bind("<Enter>", self.on_enter_name)
        self.name.bind("<Leave>", self.on_leave_name)
        self.name.bind("<Button-1>", self.on_click_name)
        
        self.grade.bind("<Enter>", self.on_enter_grade)
        self.grade.bind("<Leave>", self.on_leave_grade)
        self.grade.bind("<Button-1>", self.on_click_grade)
             
        self.name.grid(row=0, column=0, sticky="w", padx=(16, 8), pady=(4, 4))
        self.grade.grid(row=0, column=1, sticky="w", padx=(8, 8), pady=(4, 4))
        self.option.grid(row=0, column=2, sticky="w", padx=(8, 16), pady=(4, 4))
        
    def on_enter_name(self, e):
        self.name.configure(text_color=COLORS["gray-500"])

    def on_leave_name(self, e):
        self.name.configure(text_color=COLORS["gray-400"])
        
    def on_enter_grade(self, e):
        self.grade.configure(text_color=COLORS["gray-500"])

    def on_leave_grade(self, e):
        self.grade.configure(text_color=COLORS["gray-400"])
        
    def on_click_name(self, e):
        self.manager.sort("name")
        
    def on_click_grade(self, e):
        self.manager.sort("grade")
        

class TableEntry:
    def __init__(
        self, parent, manager, index: int, grid_index: int, name: str, grade: float
    ):
        self.manager = manager
        self.index = index

        self.name = ctk.CTkLabel(
            parent,
            fg_color="transparent",
            text=name,
            text_color=COLORS["zinc-900"],
            font=FONTS["framed"],
            anchor="w",
        )

        self.grade = ctk.CTkLabel(
            parent,
            fg_color="transparent",
            text=f"{grade:.2f}",
            text_color=COLORS["zinc-900"],
            font=FONTS["framed"],
            anchor="w",
        )

        self.option = ctk.CTkLabel(
            parent,
            fg_color="transparent",
            text="Supprimer",
            text_color=COLORS["red-500"],
            font=FONTS["framed"],
            anchor="w",
            cursor="hand2",
        )

        self.option.bind("<Enter>", self.on_enter)
        self.option.bind("<Leave>", self.on_leave)
        self.option.bind("<Button-1>", self.delete)

        self.name.grid(
            row=grid_index, column=0, sticky="w", padx=(16, 8), pady=(4, 4)
        )
        self.grade.grid(
            row=grid_index, column=1, sticky="w", padx=(8, 8), pady=(4, 4)
        )
        self.option.grid(
            row=grid_index, column=2, sticky="w", padx=(8, 16), pady=(4, 4)
        )

    def on_enter(self, e):
        self.option.configure(text_color=COLORS["red-400"])

    def on_leave(self, e):
        self.option.configure(text_color=COLORS["red-500"])

    def delete(self, e):
        self.manager.delete(self.index)
