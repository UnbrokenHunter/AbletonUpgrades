import tkinter as tk
from core.hotkey_manager import InputHandler
from core.create_plugin_menu import create_plugin_menu
from utils.window_utils import is_ableton_active
from utils.logging_utils import log

root = None
handler = None

def process_inputs():    
    try:
        if is_ableton_active():
            handler.process_inputs()
    except KeyboardInterrupt:
        log.info("Exiting...")
        
    root.after(5, process_inputs)


def main():
    log.info("Starting the Ableton Helper...")

    # Hotkeys
    # ----------------------------------------

    # Locate Hotkey config file is present
    CONFIG_PATH = "config/hotkeys_config.json"

    # Locates and validates configs
    global handler
    handler = InputHandler(CONFIG_PATH)
    handler.register_hotkeys()

    # Window
    # ----------------------------------------

    # Init Menu Tkinter
    global root
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    root.after(1000, process_inputs)
    create_plugin_menu(root)

    


if __name__ == "__main__":
    main()
