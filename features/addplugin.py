import pyautogui
import time
from utils.window_utils import focus_ableton
from utils.logging_utils import log

def run(plugin):
    start = time.perf_counter()

    focus_ableton()

    # print(f"Attempting Add Plugin: {plugin}")
    # try:        
    #     start_macro()

    pyautogui.hotkey("ctrl", "f")  # Search
    pyautogui.write(str(plugin), interval=0)
    pyautogui.press("down")
    pyautogui.press("enter")

    # finally:
    #     stop_macro()

