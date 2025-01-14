import tkinter as tk
from tkinter import font
import json

def execute_command(label):
    """Execute a command associated with a menu item."""
    print(f"Executed: {label}")

def load_menu_config(file_path):
    """Load the menu structure from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Menu configuration file '{file_path}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Failed to parse menu configuration file '{file_path}'.")
        return []

def create_menu(root, options, x_offset=0, y_offset=0):
    """Create a menu at the given position with the provided options."""
    menu_font = font.Font(family="Arial", size=12)

    # Calculate dimensions dynamically
    max_label_width = max(menu_font.measure(option["label"]) for option in options)
    label_height = menu_font.metrics("linespace")
    padding_x = 20
    padding_y = 10
    menu_width = max_label_width + padding_x * 2
    menu_height = (label_height + padding_y) * len(options)

    # Create a new top-level menu
    menu = tk.Toplevel()
    menu.overrideredirect(True)
    menu.attributes('-topmost', True)
    menu.geometry(f"{menu_width}x{menu_height}+{x_offset}+{y_offset}")
    menu.config(bg="#2C2C2C")

    submenus = []

    def close_submenus():
        """Close any open submenus."""
        for submenu in submenus:
            if submenu.winfo_exists():
                submenu.destroy()
        submenus.clear()

    # Add menu items
    for i, option in enumerate(options):
        label = tk.Label(
            menu, text=option["label"], bg="#2C2C2C", fg="white",
            font=menu_font, anchor="w", padx=10, pady=5
        )
        label.pack(fill=tk.X)

        # Hover effects
        label.bind("<Enter>", lambda e, lbl=label: lbl.config(bg="#3C3C3C"))
        label.bind("<Leave>", lambda e, lbl=label: lbl.config(bg="#2C2C2C"))

        # Command execution or submenu
        if "command" in option:
            label.bind("<Button-1>", lambda e, cmd=option["command"]: (eval(cmd), root.destroy()))
        elif "submenu" in option:
            def open_submenu(event, opt=option, lbl=label):
                close_submenus()
                x, y, w, h = menu.winfo_x(), menu.winfo_y(), menu_width, lbl.winfo_height()
                submenu_x = x + w
                submenu_y = y + i * h
                submenu = create_menu(root, opt["submenu"], x_offset=submenu_x, y_offset=submenu_y)
                submenus.append(submenu)

            # Pass the current `option` to the lambda as a default argument
            label.bind("<Enter>", lambda e, opt=option: open_submenu(e, opt), add="+")
            label.bind("<Leave>", lambda e: close_submenus(), add="+")

    # Close menu if clicked outside
    def on_click_outside(event):
        if not menu.winfo_containing(event.x_root, event.y_root):
            close_submenus()
            menu.destroy()
            root.destroy()

    menu.bind("<Leave>", on_click_outside)

    return menu


def run():
    """Main function to create and show the menu."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Load menu structure from JSON
    menu_structure = load_menu_config("config/menu_config.json")

    if not menu_structure:
        return  # Exit if the menu structure is empty

    # Get mouse position and show menu
    x, y = root.winfo_pointerx(), root.winfo_pointery()
    create_menu(root, menu_structure, x_offset=x, y_offset=y)

    root.mainloop()
