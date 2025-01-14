import pyautogui
import pyperclip
import time
from utils.macro_utils import release_pressed_keys, block_input
from utils.logging_utils import log

def run():
    print("Attempting Absolute Paste")
    try:        
        # Release all currently pressed keys
        release_pressed_keys()

        # Block user input
        block_input(True)
        log.info("User input blocked. Starting automation.")

        clipboard_saved = pyperclip.paste()  # Save clipboard state
        pyperclip.copy("")  # Clear clipboard

        pyautogui.hotkey("ctrl", "v")  # Paste
        pyautogui.press("backspace")  # Backspace
        pyautogui.hotkey("ctrl", "v")  # Paste

        pyperclip.copy(clipboard_saved)  # Restore clipboard state
    finally:
        # Always re-enable input
        block_input(False)
        log.info("User input restored.")
