import keyboard
import ctypes
import pygetwindow as gw
from utils.logging_utils import log

is_busy = False

def make_busy():
    global is_busy
    is_busy = True

def stop_busy():
    global is_busy
    is_busy = False

def check_busy():
    global is_busy
    return is_busy

def start_macro():
    # Release all currently pressed keys
    release_pressed_keys()

    # Block user input
    block_input(True)
    log.info("User input blocked. Starting automation.")

def stop_macro():
    # Always re-enable input
    block_input(False)
    log.info("User input restored.")

def block_input(state: bool):
    """
    Enable or disable user input on Windows.
    :param state: True to disable, False to enable.
    """
    try:
        ctypes.windll.user32.BlockInput(state)
    except Exception as e:
        log.error(f"Failed to change input state: {e}")

def release_pressed_keys():
    """
    Release any keys that are currently pressed to reset the key state.
    """
    try:
        keys = keyboard._pressed_events.keys()
        for key in list(keys):
            keyboard.release(key)
        log.info("Released all pressed keys.")
    except Exception as e:
        log.error(f"Error releasing pressed keys: {e}")
