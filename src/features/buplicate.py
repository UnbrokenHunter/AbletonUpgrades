import pyautogui
import threading
from utils import macro_utils
from utils.logging_utils import log

def run():
    if (macro_utils.check_busy() == False):
        macro_utils.make_busy()
        t1 = threading.Thread(target=exectute, args=[], daemon=True)
        t1.start()

def exectute():
    print("Attempting Buplicate")
    
    for i in range(8):
        pyautogui.hotkey("ctrl", "d")  # duplicate
    pyautogui.press("b")

    macro_utils.stop_busy()

            
