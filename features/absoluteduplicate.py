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
    print("Attempting Absolute Duplicate")

    # start = time.perf_counter()

    pause = pyautogui.PAUSE
    pyautogui.PAUSE = 0

    pyautogui.keyUp("ctrl")
    pyautogui.keyUp("shift")
    pyautogui.keyUp("alt")

    pyautogui.PAUSE = pause # Small number to still allow it all to be registered

    pyautogui.hotkey("ctrl", "c")  # Copy
    pyautogui.hotkey("ctrl", "d")  # Duplicate
    pyautogui.press("backspace")  # Backspace
    pyautogui.hotkey("ctrl", "v")  # Paste

    pyautogui.PAUSE = pause

    macro_utils.stop_busy()

    # end = time.perf_counter()

    # log.debug("Time: " + str(end - start))