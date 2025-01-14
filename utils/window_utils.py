import win32gui
import win32process
import psutil
from utils.logging_utils import log

def is_ableton_active():
    """
    Check if the active window belongs to Ableton Live or its plugins using process-based validation.
    """
    try:
        # Get the handle of the active window
        hwnd = win32gui.GetForegroundWindow()
        if not hwnd:
            return False

        # Get the process ID associated with the active window
        _, pid = win32process.GetWindowThreadProcessId(hwnd)

        # Get the process name and parent processes
        process = psutil.Process(pid)
        process_name = process.name().lower()
        parent_name = process.parent().name().lower() if process.parent() else None

        # log.info(f"Active window process: {process_name}, Parent process: {parent_name}")

        # Check if the process name or parent process name matches Ableton
        if "ableton" in process_name or (parent_name and "ableton" in parent_name) or "python":
            return True

        return False

    except Exception as e:
        log.error(f"Error checking active window process: {e}")
        return False
