import time
from pynput import mouse
import keyboard
from core.config_manager import validate_and_update_config
from core.action_registry import action_registry
from utils.logging_utils import log

class InputHandler:
    def __init__(self, config_file):
        self.config = validate_and_update_config(config_file)
        self.last_click_time = {}
        self.double_click_threshold = 0.3  # 300ms
        self.running = True

    def register_hotkeys(self):
        # Start mouse listener in a separate thread
        mouse_listener = mouse.Listener(on_click=self._on_mouse_click)
        mouse_listener.start()
        
        for hotkey, action_name in self.config["hotkeys"].items():
            action = action_registry.get(action_name)
            if action:
                log.info(f"Registered input '{hotkey}' for action '{action_name}'.")
            else:
                log.warning(f"Action '{action_name}' not found in registry.")

    def process_inputs(self):
        for hotkey, action_name in self.config["hotkeys"].items():
            action = action_registry.get(action_name)
            if action and callable(action) and not hotkey.startswith("mouse.") and keyboard.is_pressed(hotkey):
                action()

    def _on_mouse_click(self, x, y, button, pressed):
        if not pressed:
            return  # Process only press events

        current_time = time.time()
        button_name = f"mouse.{button.name}"  # e.g., mouse.left or mouse.right

        # Check for single and double-click in config
        for hotkey, action_name in self.config["hotkeys"].items():
            if hotkey.startswith(button_name):
                action = action_registry.get(action_name)
                if not action or not callable(action):
                    continue

                if hotkey.endswith(".double"):
                    # Handle double-click
                    if button_name not in self.last_click_time:
                        self.last_click_time[button_name] = current_time
                    elif current_time - self.last_click_time[button_name] <= self.double_click_threshold:
                        action()
                        log.info(f"Executed double-click action: {action_name}")
                        self.last_click_time[button_name] = 0
                    else:
                        self.last_click_time[button_name] = current_time
                else:
                    # Handle single click
                    action()
                    log.info(f"Executed single-click action: {action_name}")

    def stop(self):
        self.running = False
