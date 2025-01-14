import json
from utils.logging_utils import log

def load_menu_config(file_path):
    """Load the menu structure from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            log.info(f"Loading menu configuration from '{file_path}'")
            return json.load(f)
    except FileNotFoundError:
        log.error(f"Error: Menu configuration file '{file_path}' not found.")
        return []
    except json.JSONDecodeError as e:
        log.error(f"Error parsing menu configuration: {e}")
        return []
