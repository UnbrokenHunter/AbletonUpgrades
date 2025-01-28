import pyautogui
from utils.logging_utils import log
from core.create_plugin_menu import get_menu

# Entry Point
def run():
    """Load the menu system and execute it."""
    
    pyautogui.press("esc")
    
    pyautogui.keyUp("ctrl")
    pyautogui.keyUp("shift")
    pyautogui.keyUp("alt")

    manager = get_menu()
    manager.show_menu()
