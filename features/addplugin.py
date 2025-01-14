import pyautogui
import time
from utils.macro_utils import start_macro, stop_macro
from utils.logging_utils import log

def run():
    print("Attempting Add Plugin")
    try:        
        start_macro()

        pyautogui.hotkey("ctrl", "f")  # Search
        pyautogui.write("Utility")
        pyautogui.press("down")
        pyautogui.press("enter")

    finally:
        stop_macro()