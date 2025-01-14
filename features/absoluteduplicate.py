import pyautogui
import time
from utils.macro_utils import start_macro, stop_macro
from utils.logging_utils import log

def run():
    print("Attempting Absolute Duplicate")
    try:        
        start_macro()

        pyautogui.hotkey("ctrl", "c")  # Copy
        pyautogui.hotkey("ctrl", "d")  # Duplicate or Delete
        pyautogui.press("backspace")  # Backspace
        pyautogui.hotkey("ctrl", "v")  # Paste
        
    finally:
        stop_macro()