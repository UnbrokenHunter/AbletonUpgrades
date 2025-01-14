from core.hotkey_manager import InputHandler
from utils.window_utils import is_ableton_active
from utils.logging_utils import log

def main():
    log.info("Starting the Ableton Helper...")

    # Locate Hotkey config file is present
    CONFIG_PATH = "config/hotkeys_config.json"

    # Locates and validates configs
    handler = InputHandler(CONFIG_PATH)
    handler.register_hotkeys()

    log.info("Hotkeys registered. Listening for inputs...")

    try:
        while True:
            if is_ableton_active():
                handler.process_inputs()
                # log.info("Ableton Active")
            # else:
            #     log.info("Ableton is not active.")
    except KeyboardInterrupt:
        log.info("Exiting...")

if __name__ == "__main__":
    main()
