import pyautogui
import pyperclip
import time
from utils.macro_utils import release_pressed_keys, block_input
from utils.logging_utils import log

def run():
    print("Attempting Add Plugin")
    try:        
        # Release all currently pressed keys
        release_pressed_keys()

        # Block user input
        block_input(True)
        log.info("User input blocked. Starting automation.")

        pyautogui.hotkey("ctrl", "f")  # Search
        pyautogui.write("Utility")
        pyautogui.press("down")
        pyautogui.press("enter")

    finally:
        # Always re-enable input
        block_input(False)
        log.info("User input restored.")
