import pyautogui
import time
from utils.macro_utils import start_macro, stop_macro
from utils.logging_utils import log

def run():
    print("Attempting Better Redo")
    pyautogui.keyUp("shift")
    pyautogui.hotkey("ctrl", "y")  # Redo
            
