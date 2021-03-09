from turtle import Screen

def get_complementary_color(color, colormode):
    screen = Screen()
    canvas = screen.getcanvas()
    root = canvas.winfo_toplevel()
    r, g, b = root.winfo_rgb(color)

    if colormode == 255:
        # the 8-bit shift is because rgb function returns 16 bit integer. Result = 65,535(0xFFFF) to 255(0xFF)
        # Complementary color is the result of subtracting the actual color from the max color value
        r, g, b = colormode - (r >> 8), colormode - (g >> 8), colormode - (b >> 8)
    else:
        pass  # don't know about the other color modes ... research and implement

    return r, g, b
