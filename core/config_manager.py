import json
import os
from core.action_registry import action_registry
from utils.logging_utils import log

def validate_and_update_config(config_file):
    if not os.path.exists(config_file):
        config = {"hotkeys": {}}
    else:
        with open(config_file, "r") as file:
            try:
                config = json.load(file)
            except json.JSONDecodeError:
                log.info("Invalid config file format. Starting fresh.")
                config = {"hotkeys": {}}

    hotkeys = config.get("hotkeys", {})
    updated = False

    for action_name in action_registry.keys():
        if action_name not in hotkeys.values():
            default_hotkey = f"ctrl+alt+{action_name[-1]}"  # Example default hotkey
            hotkeys[default_hotkey] = action_name
            updated = True
            log.info(f"Added missing action '{action_name}' with default hotkey '{default_hotkey}'.")

    if updated:
        config["hotkeys"] = hotkeys
        with open(config_file, "w") as file:
            json.dump(config, file, indent=4)
        log.info("Config file updated with new hotkeys.")
    else:
        log.info("Config file is up to date.")

    return config
