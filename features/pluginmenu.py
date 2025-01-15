from utils.logging_utils import log
import tkinter as tk
from features import addplugin
from utils.font_utils import load_custom_font
from utils.json_utils import load_menu_config
from utils.window_utils import focus_ableton
from PIL import Image, ImageTk, ImageDraw

# Global variables
timer_id = None  # To track mouse leave timer
MENU_CONFIG_PATH = "config/menu_config.json"  # Config file path

# Utility: Create Rounded Rectangle Image
def create_rounded_rectangle_image(width, height, corner_radius, bg_color, border_color=None, border_width=0):
    """Create a rounded rectangle image using Pillow."""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))  # Transparent background
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        (border_width, border_width, width - border_width, height - border_width),
        radius=corner_radius,
        fill=bg_color,
        outline=border_color,
        width=border_width
    )
    return img


# Core: Command Execution
def execute_command(label):
    """Execute a command associated with a menu item."""
    log.info(f"Executed: {label}")
    focus_ableton()
    addplugin.run(label)


# Core: Create Menu
def create_menu(root, options, layer, x_offset=0, y_offset=0):
    """Create a menu at the given position with the provided options."""
    # Load custom font
    menu_font = load_custom_font(size=12)

    # Calculate dimensions dynamically
    padding_x = 20  # Horizontal padding
    padding_y = 15  # Vertical padding
    corner_radius = 20
    max_label_width = max(menu_font.measure(option["label"]) for option in options) + padding_x
    label_height = menu_font.metrics("linespace")
    menu_width = max_label_width + padding_x * 2
    menu_height = (label_height + padding_y) * len(options)

    # Create rounded background image
    rounded_img = create_rounded_rectangle_image(
        menu_width, menu_height, corner_radius, bg_color="#2C2C2C"
    )
    rounded_img_tk = ImageTk.PhotoImage(rounded_img)

    # Create a new top-level menu
    menu = tk.Toplevel(root)
    menu.overrideredirect(True)
    menu.attributes('-topmost', True)
    menu.geometry(f"{menu_width}x{menu_height}+{x_offset}+{y_offset}")
    menu.attributes('-transparentcolor', 'black')  # Make the black parts transparent
    menu.config(bg="black")

    # Set the background image
    bg_label = tk.Label(menu, image=rounded_img_tk, bg="black", bd=0)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = rounded_img_tk  # Keep a reference to avoid garbage collection

    # Add the current menu to the layer stack
    if layer >= len(root.layers):
        root.layers.append(menu)
    else:
        root.layers[layer] = menu

    # Add menu items
    submenus = []
    for i, option in enumerate(options):
        label = tk.Label(
            menu,
            text=option["label"],
            bg="#2C2C2C",
            fg="white",
            font=menu_font,
            anchor="w",
            padx=5,
            pady=5
        )
        label.place(
            x=padding_x,
            y=i * (label_height + padding_y),
            width=max_label_width,
            height=label_height + padding_y
        )

        # Hover effects
        label.bind("<Enter>", lambda e, lbl=label: lbl.config(bg="#3C3C3C"))
        label.bind("<Leave>", lambda e, lbl=label: lbl.config(bg="#2C2C2C"))

        # Command execution or submenu
        if "command" in option:
            label.bind("<Button-1>", lambda e, cmd=option["command"]: execute_command(cmd))
        elif "submenu" in option:
            def open_submenu(event, opt=option, idx=i):
                # Remove menus deeper than this layer
                for l in range(layer + 1, len(root.layers)):
                    root.layers[l].destroy()
                root.layers = root.layers[:layer + 1]

                # Create the submenu
                submenu_x = menu.winfo_x() + menu_width
                submenu_y = menu.winfo_y() + idx * (label_height + padding_y)
                submenu = create_menu(root, opt["submenu"], layer + 1, x_offset=submenu_x, y_offset=submenu_y)
                submenus.append(submenu)

            label.bind("<Enter>", open_submenu, add="+")

    # Timer-based close logic
    def close_menu_with_buffer(event):
        """Start a timer to check if the mouse is outside the menu."""
        global timer_id

        def check_mouse_position():
            if not menu.winfo_containing(event.x_root, event.y_root):
                # Destroy all submenus
                for l in range(layer, len(root.layers)):
                    if root.layers[l].winfo_exists():
                        root.layers[l].destroy()
                root.layers = root.layers[:layer]
                menu.destroy()
                root.destroy()

        timer_id = root.after(200, check_mouse_position)  # Delay before checking

    def cancel_timer(event):
        """Cancel the timer if the mouse re-enters the menu."""
        global timer_id
        if timer_id:
            root.after_cancel(timer_id)
            timer_id = None

    # Bind events for timer-based closing
    menu.bind("<Leave>", close_menu_with_buffer, add="")  # Trigger buffer on leave
    menu.bind("<Enter>", cancel_timer, add="")  # Cancel buffer when re-entering

# Core: Run Function
def run():
    """Load menu structure and display the menu."""
    # Initialize the root windowe
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Load menu structure
    menu_structure = load_menu_config(MENU_CONFIG_PATH)
    
    if not menu_structure:
        log.error("Menu structure is empty.")
        return

    # Create Layers Variable (Set layer 0 in first create)
    root.layers = []

    # Get mouse position and show menu
    x, y = root.winfo_pointerx(), root.winfo_pointery()
    create_menu(root, menu_structure, 0, x_offset=x - 20, y_offset=y - 20)

    root.mainloop()
