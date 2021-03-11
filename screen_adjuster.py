from turtle import Screen

# w*h= 648*648, [2]
# w*h= 649*649, [3]
# w*h= 667*667, [21]
# from 649*649[3] to 667*667[21] there's one-to-one increment between window size and border

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

UP, DOWN, LEFT, RIGHT, SHIFT_L, SHIFT_R, ESCAPE = "Up", "Down", "Left", "Right", "Shift_L", "Shift_R", "Escape"
snapshots = []
recurse = True
window_width = 648
increment = 1
border = 2


def print_snapshots():
    print("\n\n\nSaved snapshots:\n----------------\n")
    for item in snapshots:
        print(item)


def start_adjusting():
    adjust(window_width)
    print_snapshots()


def adjust(size):

    def increase_size():
        global window_width
        window_width += increment
        screen.bye()

    def decrease_size():
        global window_width
        window_width -= increment
        screen.bye()

    def increase_border():
        global border
        border += increment
        screen.bye()

    def decrease_border():
        global border
        border -= increment
        screen.bye()

    def change_increment():
        global increment
        while True:
            user_input = screen.numinput("Change increment",
                                         "Enter a natural number (positive integer grater than zero):", increment)
            if user_input is not None:
                break
        increment = int(user_input)
        print(f"w*h= {size}*{size}, [{border}], +{increment}")

    def save_snapshot():
        global snapshots
        snapshots.append(f"w*h= {size}*{size}, [{border}]")

    def stop_recursion():
        global recurse
        recurse = False
        screen.bye()

    screen = Screen()
    screen.screensize(canvwidth=size - border, canvheight=size - border)
    screen.setup(size, size)
    screen.onkey(decrease_size, LEFT)
    screen.onkey(increase_size, RIGHT)
    screen.onkey(increase_border, UP)
    screen.onkey(decrease_border, DOWN)
    screen.onkey(stop_recursion, ESCAPE)
    screen.onkey(change_increment, SHIFT_L)
    screen.onkey(change_increment, SHIFT_R)
    screen.onkey(save_snapshot, "s")
    screen.listen()
    print(f"w*h= {size}*{size}, [{border}], +{increment}")

    screen.mainloop()
    if recurse:
        adjust(window_width)
