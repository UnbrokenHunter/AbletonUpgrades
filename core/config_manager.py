import json
import os
from core.action_registry import action_registry

def validate_and_update_config(config_file):
    if not os.path.exists(config_file):
        config = {"hotkeys": {}}
    else:
        with open(config_file, "r") as file:
            try:
                config = json.load(file)
            except json.JSONDecodeError:
                print("Invalid config file format. Starting fresh.")
                config = {"hotkeys": {}}

    hotkeys = config.get("hotkeys", {})
    updated = False

    for action_name in action_registry.keys():
        if action_name not in hotkeys.values():
            default_hotkey = f"ctrl+alt+{action_name[-1]}"  # Example default hotkey
            hotkeys[default_hotkey] = action_name
            updated = True
            print(f"Added missing action '{action_name}' with default hotkey '{default_hotkey}'.")

    if updated:
        config["hotkeys"] = hotkeys
        with open(config_file, "w") as file:
            json.dump(config, file, indent=4)
        print("Config file updated with new hotkeys.")
    else:
        print("Config file is up to date.")

    return config
