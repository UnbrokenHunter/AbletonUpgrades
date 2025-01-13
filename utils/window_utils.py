import pygetwindow as gw
from utils.logging_utils import log

def is_ableton_active():
    """
    Check if Ableton Live is the active application.
    Cross-platform solution.
    """
    try:
        # Get all open windows
        active_window = gw.getActiveWindow()
        if active_window is not None:
            # Check if "Ableton Live" is part of the window's title
            return "Ableton Live" in active_window.title
        return False
    except Exception as e:
        log.error(f"Error checking active window: {e}")
        return False
