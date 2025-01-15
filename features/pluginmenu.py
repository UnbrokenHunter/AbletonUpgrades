from utils.logging_utils import log
import tkinter as tk
from features import addplugin
from utils.font_utils import load_custom_font
from utils.json_utils import load_menu_config
from utils import menu_utils
from utils.window_utils import focus_ableton
from typing import List, Dict, Any

# Constants
MENU_CONFIG_PATH = "config/menu_config.json"  # Config file path
PADDING_X = 20  # Horizontal padding
PADDING_Y = 15  # Vertical padding
BG_COLOR = "#2C2C2C"  # Default background color
HOVER_COLOR = "#3C3C3C"  # Hover background color

timer_id = None  # Timer ID for tracking menu close delays

class MenuManager:
    def __init__(self):
        self.root = None
        self.layers = []  # Stack to manage menu layers

    def execute_command(self, label: str):
        """Execute a command associated with a menu item."""
        try:
            log.info(f"Executed: {label}")
            focus_ableton()
            addplugin.run(label)
        except Exception as e:
            log.error(f"Error executing command '{label}': {e}")

    def create_menu(self, options: List[Dict[str, Any]], layer: int, x_offset: int = 0, y_offset: int = 0):
        """Create a menu at the given position with the provided options."""
        global timer_id

        # Destroy menus deeper than the current layer
        for l in range(layer, len(self.layers)):
            if self.layers[l].winfo_exists():
                self.layers[l].destroy()
        self.layers = self.layers[:layer]

        menu_font = load_custom_font(size=12)

        # Calculate dimensions dynamically
        try:
            max_label_width = max(menu_font.measure(option["label"]) for option in options) + PADDING_X * 2 + 10  # Extra space for chevrons
        except KeyError as e:
            log.error(f"Menu option missing required field: {e}")
            return

        label_height = menu_font.metrics("linespace")
        menu_width = max_label_width
        menu_height = (label_height + PADDING_Y) * len(options)

        menu = tk.Toplevel(self.root)
        menu.overrideredirect(True)
        menu.attributes('-topmost', True)
        menu.geometry(f"{menu_width}x{menu_height}+{x_offset}+{y_offset}")
        menu.config(bg=BG_COLOR)

        # Add the current menu to the layer stack
        if layer >= len(self.layers):
            self.layers.append(menu)
        else:
            self.layers[layer] = menu

        # Add menu items
        for i, option in enumerate(options):
            label = tk.Label(
                menu,
                text=option["label"],
                bg=BG_COLOR,
                fg="white",
                font=menu_font,
                anchor="w",
                padx=5,
                pady=5
            )
            label.place(
                x=0,
                y=i * (label_height + PADDING_Y),
                width=max_label_width,
                height=label_height + PADDING_Y
            )

            # Hover effects
            label.bind("<Enter>", lambda e, lbl=label: lbl.config(bg=HOVER_COLOR))
            label.bind("<Leave>", lambda e, lbl=label: lbl.config(bg=BG_COLOR))

            # Command execution or submenu
            if "command" in option:
                label.bind("<Button-1>", lambda e, cmd=option["command"]: self.execute_command(cmd))
            elif "submenu" in option:
                label.bind("<Enter>", lambda e, opt=option, idx=i: self.create_submenu(opt, idx, menu, menu_width, label_height, PADDING_Y, layer))

                # Add chevron indicator for submenu
                chevron = tk.Label(
                    menu,
                    text="▶",
                    bg=BG_COLOR,
                    fg="white",
                    font=menu_font
                )
                chevron.place(
                    x=menu_width - 30,  # Position chevron on the right
                    y=i * (label_height + PADDING_Y),
                    width=20,
                    height=label_height + PADDING_Y
                )

        # Timer-based close logic
        def close_menu_with_buffer(event):
            """Start a timer to check if the mouse is outside the menu."""
            global timer_id

            def check_mouse_position():
                if not menu.winfo_containing(self.root.winfo_pointerx(), self.root.winfo_pointery()):
                    for l in range(layer, len(self.layers)):
                        if self.layers[l].winfo_exists():
                            self.layers[l].destroy()
                    self.layers = self.layers[:layer]
                    self.root.destroy()

            timer_id = self.root.after(200, check_mouse_position)  # Delay before checking

        def cancel_timer(event):
            """Cancel the timer if the mouse re-enters the menu."""
            global timer_id
            if timer_id:
                self.root.after_cancel(timer_id)
                timer_id = None

        # Bind events for timer-based closing
        menu.bind("<Leave>", close_menu_with_buffer, add="")  # Trigger buffer on leave
        menu.bind("<Enter>", cancel_timer, add="")  # Cancel buffer when re-entering

    def create_submenu(self, option: Dict[str, Any], index: int, parent_menu: tk.Toplevel, menu_width: int, label_height: int, padding_y: int, layer: int):
        """Create a submenu at the appropriate position."""
        submenu_x = parent_menu.winfo_x() + menu_width
        submenu_y = parent_menu.winfo_y() + index * (label_height + padding_y)
        self.create_menu(option["submenu"], layer + 1, x_offset=submenu_x, y_offset=submenu_y)

    def destroy_all_menus(self):
        """Destroy all menus in the stack."""
        for menu in self.layers:
            if menu.winfo_exists():
                menu.destroy()
        self.layers.clear()
        self.root.destroy()

    def run(self):
        """Load menu structure and display the menu."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window

        menu_structure = load_menu_config(MENU_CONFIG_PATH)
        if not menu_structure:
            log.error("Menu structure is empty.")
            return

        # Get mouse position and show menu
        x, y = self.root.winfo_pointerx(), self.root.winfo_pointery()
        self.create_menu(menu_structure, 0, x_offset=x - 20, y_offset=y - 20)

        self.root.mainloop()

# Entry Point
def run():
    """Load the menu system and execute it."""
    manager = MenuManager()
    manager.run()
