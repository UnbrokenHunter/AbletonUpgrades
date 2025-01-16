import ctypes
from tkinter import font
from utils.logging_utils import log
import os

FONT_PATH = "rsc/DIN-Regular.ttf"  # Path to the DIN font

# Utility: Load Font
def load_custom_font(size):
    """Temporarily load a font from file into Tkinter."""
    try:
        if not os.path.exists(FONT_PATH):
            raise FileNotFoundError(f"Font file '{FONT_PATH}' not found.")

        # Load the font into the Windows GDI (Windows-only solution)
        if os.name == 'nt':
            ctypes.windll.gdi32.AddFontResourceW(FONT_PATH)
        
        # Use the family name of the font
        family_name = "DIN-Regular"  # Replace with the actual family name
        return font.Font(family=family_name, size=size)
    except Exception as e:
        log.error(f"Failed to load font '{FONT_PATH}': {e}")
        return font.Font(size=size)  # Fallback to default font
