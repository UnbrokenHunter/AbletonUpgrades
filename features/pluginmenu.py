import pyautogui
from utils.logging_utils import log
from core.create_plugin_menu import get_menu

# Entry Point
def run():    
    pause = pyautogui.PAUSE
    pyautogui.PAUSE = 0

    pyautogui.press("esc")
    
    pyautogui.keyUp("ctrl")
    pyautogui.keyUp("shift")
    pyautogui.keyUp("alt")

    pyautogui.PAUSE = pause

    manager = get_menu()
    manager.show_menu()
