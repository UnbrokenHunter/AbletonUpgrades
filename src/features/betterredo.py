import pyautogui
import threading
from utils import macro_utils
from utils.logging_utils import log

def run():
    if (macro_utils.check_busy() == False):
        macro_utils.make_busy()
        t1 = threading.Thread(target=exectute, args=[], daemon=True)
        t1.start()

# BROKEN PLEASE FIX
# When you press ctrl shift z it will undo and redo, canceling itself out
def exectute():
    print("Attempting Better Redo")

    pause = pyautogui.PAUSE
    # pyautogui.PAUSE = 0.05

    pyautogui.keyUp("shift")
    pyautogui.keyUp("z")

    pyautogui.hotkey("ctrl", "y")  # Redo

    pyautogui.keyDown("ctrl")
            
    pyautogui.PAUSE = pause

    macro_utils.stop_busy()
