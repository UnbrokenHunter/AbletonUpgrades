from core.hotkey_manager import register_hotkeys, process_hotkeys
from utils.window_utils import is_ableton_active

def main():
    print("Starting the Ableton Helper...")

    # Locate Hotkey config file is present
    CONFIG_PATH = "config/hotkeys_config.json"
    hotkeys = register_hotkeys(CONFIG_PATH) # Locates and validates configs

    print("Hotkeys registered. Listening for inputs...")

    try:
        while True:
            if is_ableton_active():
                process_hotkeys(hotkeys)
                print("Ableton Active")
            else:
                print("Ableton is not active.")
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()
