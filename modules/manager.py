from customtkinter import filedialog
import bisect

from modules.config import *


class StudentManager:
    def __init__(self, order: str = "name"):
        self.extensions = [("Text Document", "*.txt")]
        self.order = order
        self.query = ""
        self.list = []
        self.filtered = []

    def add(self, student: tuple[str, float]):
        if self.order == "name":
            bisect.insort(self.list, student, key=lambda student: student[0])
        else:
            bisect.insort(self.list, student, key=lambda student: -student[1])

        self.search("")

    def delete(self, index: int):
        self.list.pop(index)
        self.filter_students()
        self.refresh()

    def sort(self, order: str):
        self.order = order
        self.sort_students()
        self.filter_students()
        self.refresh()

    def search(self, query: str):
        self.query = query.lower()
        self.filter_students()
        self.refresh()

    def sort_students(self):
        if self.order == "name":
            self.list.sort(key=lambda student: student[0])
        else:
            self.list.sort(key=lambda student: -student[1])

    def filter_students(self):
        if self.query == "":
            self.filtered = self.list
        else:
            self.filtered = []

            for student in self.list:
                name_split = student[0].split(" ")
                for segment in name_split:
                    if segment.lower().find(self.query) == 0:
                        bisect.insort(self.filtered, student)
                        break

    def load_students(self):
        filepath = filedialog.askopenfile(
            filetypes=self.extensions, defaultextension=self.extensions
        )
        if filepath is None:
            return

        fallback = self.list
        self.list = []
        valid_file = True

        with open(filepath.name, "r") as f:
            lines = f.readlines()
            for i in range(0, len(lines), 2):
                name = lines[i].rstrip()
                grade = lines[i + 1].rstrip()
                if NAME_MATCHER.fullmatch(name) and FLOAT_MATCHER.fullmatch(grade):
                    self.add((name, float(grade)))
                else:
                    valid_file = False
                    break

        if valid_file:
            self.search("")
        else:
            self.list = fallback

    def save_students(self):
        filepath = filedialog.asksaveasfile(
            filetypes=self.extensions, defaultextension=self.extensions
        )
        if filepath is None:
            return

        with open(filepath.name, "w") as f:
            for student in self.list:
                f.write(f"{student[0]}\n{student[1]}\n")

    def set_refresh(self, refresh):
        self.refresh = refresh
