import keyboard
from core.config_manager import validate_and_update_config
from core.action_registry import action_registry
from utils.logging_utils import log

def register_hotkeys(config_file):
    # Validate and update the config file
    config = validate_and_update_config(config_file)

    # Create a dictionary of hotkeys mapped to actions
    registered_hotkeys = {}
    for hotkey, action_name in config["hotkeys"].items():
        action = action_registry.get(action_name)
        if action:
            registered_hotkeys[hotkey] = action
            log.info(f"Registered hotkey '{hotkey}' for action '{action_name}'.")
        else:
            log.exception(f"Warning: Action '{action_name}' not found in registry.")
    return registered_hotkeys

def process_hotkeys(hotkeys):
    for hotkey, action in hotkeys.items():
        if keyboard.is_pressed(hotkey):
            action()
