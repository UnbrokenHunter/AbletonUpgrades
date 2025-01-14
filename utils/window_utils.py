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

def focus_ableton():
    """
    Focus the Ableton Live window if it exists, using its process name.
    """
    try:
        # Iterate over all processes to find Ableton
        for proc in psutil.process_iter(attrs=["pid", "name"]):
            try:
                if "ableton" in proc.info["name"].lower():
                    pid = proc.info["pid"]

                    # Find the window handle associated with the Ableton process
                    def callback(hwnd, found):
                        _, win_pid = win32process.GetWindowThreadProcessId(hwnd)
                        if win_pid == pid and win32gui.IsWindowVisible(hwnd):
                            found.append(hwnd)

                    hwnd_list = []
                    win32gui.EnumWindows(callback, hwnd_list)

                    if hwnd_list:
                        # Focus the first visible Ableton window
                        hwnd = hwnd_list[0]
                        win32gui.ShowWindow(hwnd, 5)  # 5 = SW_SHOW
                        win32gui.SetForegroundWindow(hwnd)
                        log.info(f"Ableton Live focused: HWND={hwnd}")
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        log.warning("Ableton Live process not found.")
        return False

    except Exception as e:
        log.error(f"Error focusing Ableton Live: {e}")
        return False
