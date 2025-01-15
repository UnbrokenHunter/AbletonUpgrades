import pyautogui
import time
from utils.logging_utils import log

def run():
    print("Attempting Buplicate")
    
    for i in range(8):
        pyautogui.hotkey("ctrl", "d")  # duplicate
    pyautogui.press("b")
            
