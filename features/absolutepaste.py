import pyautogui
import threading
import time
from utils import macro_utils
from utils.logging_utils import log

def run():
    if (macro_utils.check_busy() == False):
        macro_utils.make_busy()
        t1 = threading.Thread(target=exectute, args=[], daemon=True)
        t1.start()

def exectute():
    print("Attempting Absolute Paste")

    pause = pyautogui.PAUSE
    pyautogui.PAUSE = 0

    pyautogui.keyUp("ctrl")
    pyautogui.keyUp("shift")
    pyautogui.keyUp("alt")

    pyautogui.PAUSE = 0.1 # Small number to still allow it all to be registered

    # For some reason it only works when i double it Please Fix 
    pyautogui.hotkey("ctrl", "v")  # Paste
    pyautogui.press("backspace")  # Backspace
    pyautogui.hotkey("ctrl", "v")  # Paste
    pyautogui.press("backspace")  # Backspace
    pyautogui.hotkey("ctrl", "v")  # Paste

    pyautogui.PAUSE = pause

    macro_utils.stop_busy()