import turtle
import math

X, Y = 0, 1
WINDOW_BORDER = 11  # fixed value. Do not modify
LARGE_OFFSET = 10  # tentative fixed value. Do not modify
SMALL_OFFSET = WINDOW_BORDER - LARGE_OFFSET  # fixed formula. Do not modify
UTILITY_TURTLE_COLOR = "red"
SCREEN_MODE = "standard"
SCREEN_COLORMODE = 255
SCREEN_XY_AXES_COLOR = "blue"
SCREEN_BOUNDARIES_COLOR = "red"


class Screen:

    def __init__(self, window_width, window_height,
                 screen=turtle.Screen(), mode=SCREEN_MODE, colormode=SCREEN_COLORMODE):
        self.screen = Screen.initialize_screen(screen, window_width, window_height)
        self.mode = mode
        self.screen.colormode(colormode)
        self.right_bound = int(math.floor(window_width / 2)) - LARGE_OFFSET
        self.left_bound = -(int(math.floor(window_width / 2)) - SMALL_OFFSET)
        self.up_bound = int(math.floor(window_height / 2)) - SMALL_OFFSET
        self.down_bound = -(int(math.floor(window_height / 2)) - LARGE_OFFSET)
        self.utility_turtle = Screen.initialize_turtle()

    @staticmethod
    def initialize_screen(screen, window_width, window_height):
        screen.screensize(canvwidth=window_width - 2, canvheight=window_height - 2)
        screen.setup(window_width, window_height)
        return screen

    @staticmethod
    def initialize_turtle():
        utility_turtle = turtle.Turtle(visible=False)
        utility_turtle.pensize(1)
        utility_turtle.speed(0)
        utility_turtle.pencolor(UTILITY_TURTLE_COLOR)
        utility_turtle.penup()
        return utility_turtle

    def draw_boundaries(self):
        color = self.utility_turtle.pencolor()
        self.utility_turtle.pencolor(SCREEN_BOUNDARIES_COLOR)
        self.draw_poliline(self.left_bound, self.up_bound,
                           (self.right_bound, self.up_bound),
                           (self.left_bound, self.down_bound),
                           (self.right_bound, self.down_bound),
                           (self.left_bound, self.up_bound),
                           (self.left_bound, self.down_bound))
        self.draw_line(self.right_bound, self.up_bound, self.right_bound, self.down_bound)
        self.utility_turtle.pencolor(color)

        color = self.utility_turtle.pencolor()
        self.utility_turtle.pencolor(SCREEN_XY_AXES_COLOR)
        self.draw_line(self.right_bound, 0, self.left_bound, 0)
        self.draw_line(0, self.up_bound, 0, self.down_bound)
        self.utility_turtle.pencolor(color)

    def get_visual_help(self):
        self.draw_boundaries()

    def draw_line(self, xi, yi, xf, yf):
        self.utility_turtle.goto(xi, yi)
        self.utility_turtle.pendown()
        self.utility_turtle.goto(xf, yf)
        self.utility_turtle.penup()

    def draw_poliline(self, xi, yi, *args):
        self.utility_turtle.goto(xi, yi)
        self.utility_turtle.pendown()
        for coordinate in args:
            self.utility_turtle.goto(coordinate[X], coordinate[Y])
        self.utility_turtle.penup()
