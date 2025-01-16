import tkinter as tk
import time
from features import addplugin
from utils.logging_utils import log
from utils.window_utils import focus_ableton
from utils.font_utils import load_custom_font
from utils.json_utils import load_menu_config
from typing import List, Dict, Any

# Constants
MENU_CONFIG_PATH = "config/menu_config.json"  # Config file path
PADDING_X = 20  # Horizontal padding
PADDING_Y = 15  # Vertical padding
BG_COLOR = "#2C2C2C"  # Default background color
HOVER_COLOR = "#3C3C3C"  # Hover background color

menu = None
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
        
    def hide_menu(self):
        for l in range(0, len(self.layers)):
            if self.layers[l].winfo_exists():
                self.layers[l].withdraw()
                
    def show_menu(self):
        log.debug("Show Menu")
        log.debug(len(self.layers))
        if self.layers[0].winfo_exists():
            self.layers[0].deiconify()
        
        x, y = self.root.winfo_pointerx(), self.root.winfo_pointery()
        self.set_position_at_mouse(x_offset=x - 20, y_offset=y - 20)
            
    def set_position_at_mouse(self, x_offset: int = 0, y_offset: int = 0):
        if 0 < len(self.layers):
            layer = self.layers[0]
            if isinstance(layer, tk.Toplevel):  # Ensure it's a Toplevel
                layer.geometry(f"+{x_offset}+{y_offset}")
            else:
                print("Error: Layer is not a Toplevel")
        else:
            print("Error: Index out of range")

        
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
            self.max_label_width = max(menu_font.measure(option.get("label", "")) for option in options if option.get("type") != "divider") + PADDING_X * 2 + 10  # Extra space for chevrons
        except KeyError as e:
            log.error(f"Menu option missing required field: {e}")
            return

        label_height = menu_font.metrics("linespace")
        menu_width = self.max_label_width
        menu_height = sum((label_height + PADDING_Y) if option.get("type") != "divider" else 5 for option in options)

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

        current_y = 0
        for option in options:
            if option.get("type") == "divider":
                divider = tk.Frame(menu, bg="white", height=2, bd=0, highlightthickness=0)
                divider.place(x=0, y=current_y, width=menu_width, height=2)
                current_y += 5
                continue

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
                y=current_y,
                width=self.max_label_width,
                height=label_height + PADDING_Y
            )
            current_y += label_height + PADDING_Y

            chevron = None  # Initialize chevron as None for items without submenus
            # Command execution or submenu
            if "command" in option:
                label.bind("<Button-1>", lambda e, cmd=option["command"]: self.execute_command(cmd))
            elif "submenu" in option:
                label.bind("<Enter>", lambda e, opt=option, lbl=label: self.create_submenu(opt, lbl, menu_width, label_height, PADDING_Y, layer), add="+")

                # Add chevron indicator for submenu
                chevron = tk.Label(
                    menu,
                    text="\u25B6",
                    bg=BG_COLOR,
                    fg="white",
                    font=menu_font
                )
                chevron.place(
                    x=menu_width - 30,  # Position chevron on the right
                    y=current_y - (label_height + PADDING_Y),
                    width=20,
                    height=label_height + PADDING_Y
                )

            # Fix late binding by using default arguments
            def on_hover_enter(event, lbl=label, chev=chevron):
                lbl.config(bg=HOVER_COLOR)
                if chev:  # Update chevron color only if it exists
                    chev.config(bg=HOVER_COLOR)

            def on_hover_leave(event, lbl=label, chev=chevron):
                lbl.config(bg=BG_COLOR)
                if chev:  # Reset chevron color only if it exists
                    chev.config(bg=BG_COLOR)

            # Bind hover events to both label and chevron
            label.bind("<Enter>", on_hover_enter, add="+")
            label.bind("<Leave>", on_hover_leave, add="+")
            
            if chevron:
                chevron.bind("<Enter>", on_hover_enter, add="+")  # Ensure chevron triggers the hover effect
                chevron.bind("<Leave>", on_hover_leave, add="+")

        def close_menu_with_buffer(event):
            """Start a timer to check if the mouse is outside the menu."""
            global timer_id

            def check_mouse_position():
                if not menu.winfo_containing(self.root.winfo_pointerx(), self.root.winfo_pointery()):
                    self.hide_menu()                    
                    
            timer_id = self.root.after(800, check_mouse_position)  # Delay before checking

        def cancel_timer(event):
            """Cancel the timer if the mouse re-enters the menu."""
            global timer_id
            if timer_id:
                self.root.after_cancel(timer_id)
                timer_id = None

        menu.bind("<Leave>", close_menu_with_buffer, add="+")  # Trigger buffer on leave
        menu.bind("<Enter>", cancel_timer, add="+")  # Cancel buffer when re-entering

    def create_submenu(self, option: Dict[str, Any], label: tk.Label, menu_width: int, label_height: int, padding_y: int, layer: int):
        """Create a submenu at the appropriate position."""
        submenu_x = label.winfo_rootx() + menu_width
        submenu_y = label.winfo_rooty()
        self.create_menu(option["submenu"], layer + 1, x_offset=submenu_x, y_offset=submenu_y)

    def run(self):
        """Load menu structure and display the menu."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window

        menu_structure = load_menu_config(MENU_CONFIG_PATH)
        if not menu_structure:
            log.error("Menu structure is empty.")
            return

        x, y = self.root.winfo_pointerx(), self.root.winfo_pointery()
        self.create_menu(menu_structure, 0, x_offset=x - 20, y_offset=y - 20)
        self.hide_menu()

        self.root.mainloop()

# Entry Point
def create_menu():
    """Load the menu system and execute it."""
    global menu
    menu = MenuManager()
    menu.run()

def get_menu():
    return menu