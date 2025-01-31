from PIL import Image, ImageTk, ImageDraw

def create_gradient_background(self, width: int, height: int, start_color: str, end_color: str) -> ImageTk.PhotoImage:
    img = Image.new("RGB", (width, height), color=start_color)
    draw = ImageDraw.Draw(img)
    for i in range(height):
        ratio = i / height
        r, g, b = (
            int(start_color[1:3], 16) * (1 - ratio) + int(end_color[1:3], 16) * ratio,
            int(start_color[3:5], 16) * (1 - ratio) + int(end_color[3:5], 16) * ratio,
            int(start_color[5:7], 16) * (1 - ratio) + int(end_color[5:7], 16) * ratio,
        )
        draw.line((0, i, width, i), fill=(int(r), int(g), int(b)))
    return ImageTk.PhotoImage(img)

def create_glow_effect(self, size: int, glow_color: str) -> ImageTk.PhotoImage:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((0, 0, size, size), fill=glow_color + "30")  # Add alpha for transparency
    return ImageTk.PhotoImage(img)
