import tkinter as tk
from tkinter import font

def execute_command(label):
    print(f"Executed: {label}")

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
            label.bind("<Button-1>", lambda e, cmd=option["command"]: (cmd(), root.destroy()))
        elif "submenu" in option:
            def open_submenu(event, opt=option, lbl=label):
                close_submenus()
                x, y, w, h = menu.winfo_x(), menu.winfo_y(), menu_width, lbl.winfo_height()
                submenu_x = x + w
                submenu_y = y + i * h
                submenu = create_menu(root, opt["submenu"], x_offset=submenu_x, y_offset=submenu_y)
                submenus.append(submenu)

            label.bind("<Enter>", lambda e: open_submenu(e, option))

    # Close menu if clicked outside
    def on_click_outside(event):
        if not menu.winfo_containing(event.x_root, event.y_root):
            close_submenus()
            menu.destroy()
            root.destroy()
            print("Clicked Outside")

    menu.bind("<Leave>", on_click_outside)

    return menu


def run():        
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Example menu structure
    menu_structure = [
        {"label": "Plugin A", "command": lambda: execute_command("Plugin A")},
        {"label": "Plugin B", "submenu": [
            {"label": "Sub-plugin B1", "command": lambda: execute_command("Sub-plugin B1")},
            {"label": "Sub-plugin B2", "command": lambda: execute_command("Sub-plugin B2")},
            {"label": "Sub-plugin B3", "submenu": [
                {"label": "Sub-sub-plugin B3.1", "command": lambda: execute_command("Sub-sub-plugin B3.1")},
                {"label": "Sub-sub-plugin B3.2", "command": lambda: execute_command("Sub-sub-plugin B3.2")},
            ]},
        ]},
        {"label": "Plugin C", "command": lambda: execute_command("Plugin C")},
        {"label": "Plugin D", "submenu": [
            {"label": "Sub-plugin D1", "command": lambda: execute_command("Sub-plugin D1")},
            {"label": "Sub-plugin D2", "command": lambda: execute_command("Sub-plugin D2")},
        ]},
    ]

    # Get mouse position and show menu
    x, y = root.winfo_pointerx(), root.winfo_pointery()
    create_menu(root, menu_structure, x_offset=x, y_offset=y)

    # Run the event loop in the background
    # root.after(5000, root.quit)
    root.mainloop()
    # root.destroy()
