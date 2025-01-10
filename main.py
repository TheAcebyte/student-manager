import customtkinter as ctk

from lib.config import *
from lib.manager import *
from lib.handler import *
from lib.creator import *
from lib.viewer import *


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        geometry = self.get_centered_geometry(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.title(WINDOW_TITLE)
        self.geometry(geometry)
        self.resizable(False, False)
        self.configure(fg_color="white")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0)
        self.columnconfigure(1, weight=1)

        self.manager = StudentManager()
        self.sidebar = Sidebar(self, self.manager)
        self.body = Body(self, self.manager)
        
        self.manager.set_refresh(self.body.viewer.refresh)
        self.mainloop()

    def get_centered_geometry(self, width: int, height: int) -> str:
        offset_width = self.winfo_screenwidth() // 2 - width // 2
        offset_height = self.winfo_screenheight() // 2 - height // 2

        return f"{width}x{height}+{offset_width}+{offset_height}"


class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, manager):
        super().__init__(parent, fg_color=COLORS["gray-600"], corner_radius=0)
        self.icon_loader = get_icon("sidebar/folder-open", size=24)
        self.icon_saver = get_icon("sidebar/floppy-disk", size=24)

        self.load = ctk.CTkButton(
            self,
            width=0,
            height=0,
            text="",
            image=self.icon_loader,
            fg_color=COLORS["gray-600"],
            hover_color=COLORS["gray-500"],
            cursor="hand2",
            command=manager.load_students,
        )
        self.save = ctk.CTkButton(
            self,
            width=0,
            height=0,
            text="",
            image=self.icon_saver,
            fg_color=COLORS["gray-600"],
            hover_color=COLORS["gray-500"],
            cursor="hand2",
            command=manager.save_students,
        )

        self.load.pack(pady=(16, 0), ipadx=8, ipady=8)
        self.save.pack(pady=(0, 0), ipadx=8, ipady=8)
        self.grid(row=0, column=0, sticky="nsew", ipadx=16)


class Body(ctk.CTkFrame):
    def __init__(self, parent, manager):
        super().__init__(parent, fg_color="transparent", corner_radius=0)
        self.grid_rowconfigure(0)
        self.grid_rowconfigure(1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.handler = EntryHandler(self, manager)
        self.creator = EntryCreator(self, manager)
        self.viewer = EntryViewer(self, manager)

        self.grid(row=0, column=1, sticky="nsew", padx=16)


if __name__ == "__main__":
    App()
