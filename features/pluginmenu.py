from utils.logging_utils import log
from core.create_menu import get_menu

# Entry Point
def run():
    """Load the menu system and execute it."""
    manager = get_menu()
    manager.show_menu()
