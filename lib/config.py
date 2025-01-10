from pathlib import Path
from PIL import Image
from customtkinter import CTkImage
import re

WINDOW_TITLE = "Gestion d'étudiants"
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 900

FONTS = {"header": ("Inter", 18), "framed": ("Inter", 14), "button": ("Inter", 16)}
COLORS = {
    "gray-50": "#F9FAFB",
    "gray-100": "#F3F4F6",
    "gray-200": "#E5E7EB",
    "gray-300": "#D1D5DB",
    "gray-400": "#9CA3AF",
    "gray-500": "#6B7280",
    "gray-600": "#4B5563",
    "zinc-900": "#18181B",
    "red-400": "#F87171",
    "red-500": "#EF4444",
    "indigo-500": "#6366F1",
    "indigo-600": "#4F46E5",
}

NAME_MATCHER = re.compile(r"[A-Za-zÀ-ÿ'\-]+( [A-Za-zÀ-ÿ'\-]+)*")
FLOAT_MATCHER = re.compile(r"([0-9]*[.])?[0-9]+")


def get_icon(path: str, size: int, extension: str = ".png") -> str:
    full_path = Path("public") / (path + extension)
    image = Image.open(full_path).convert("RGBA")
    return CTkImage(image, size=(size, size))
