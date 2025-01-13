from core.hotkey_manager import register_hotkeys, process_hotkeys
from utils.window_utils import is_ableton_active
from utils.logging_utils import log

def main():
    log.info("Starting the Ableton Helper...")

    # Locate Hotkey config file is present
    CONFIG_PATH = "config/hotkeys_config.json"
    hotkeys = register_hotkeys(CONFIG_PATH) # Locates and validates configs

    log.info("Hotkeys registered. Listening for inputs...")

    try:
        while True:
            if is_ableton_active():
                process_hotkeys(hotkeys)
                log.info("Ableton Active")
            # else:
            #     log.info("Ableton is not active.")
    except KeyboardInterrupt:
        log.info("Exiting...")

if __name__ == "__main__":
    main()
