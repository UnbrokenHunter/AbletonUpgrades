import pyautogui
import threading
from utils import macro_utils
from utils.window_utils import focus_ableton
from utils.logging_utils import log

def run(plugin):
    if (macro_utils.check_busy() == False):
        macro_utils.make_busy()
        t1 = threading.Thread(target=exectute, args=[plugin], daemon=True)
        t1.start()

def exectute(plugin):
    print(f"Attempting Add Plugin: {plugin}")
    
    focus_ableton()

    pyautogui.hotkey("ctrl", "f")  # Search
    pyautogui.write(str(plugin), interval=0)
    pyautogui.press("down")
    pyautogui.press("enter")

    macro_utils.stop_busy()

