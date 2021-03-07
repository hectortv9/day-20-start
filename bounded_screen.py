import turtle
import math

WINDOW_BORDER = 11  # fixed value. Do not modify
LARGE_OFFSET = 10  # tentative fixed value. Do not modify
SMALL_OFFSET = WINDOW_BORDER - LARGE_OFFSET  # fixed formula. Do not modify


class Screen:

    def __init__(self, window_width, window_height, screen=turtle.Screen(), mode="standard", colormode=255):
        self.screen = Screen.initialize_screen(screen, window_width, window_height)
        self.mode = mode
        self.screen.colormode(colormode)
        self.right_bound = int(math.floor(window_width / 2)) - LARGE_OFFSET
        self.left_bound = -(int(math.floor(window_width / 2)) - SMALL_OFFSET)
        self.up_bound = int(math.floor(window_height / 2)) - SMALL_OFFSET
        self.down_bound = -(int(math.floor(window_height / 2)) - LARGE_OFFSET)
        self.utility_turtle = Screen.initialize_turtle()

    def get_visual_help(self):
        self.draw_boundaries()

    def draw_boundaries(self):
        self.utility_turtle.goto(self.left_bound, self.up_bound)
        self.utility_turtle.pendown()
        self.utility_turtle.goto(self.right_bound, self.up_bound)
        self.utility_turtle.goto(self.left_bound, self.down_bound)
        self.utility_turtle.goto(self.right_bound, self.down_bound)
        self.utility_turtle.goto(self.left_bound, self.up_bound)
        self.utility_turtle.goto(self.left_bound, self.down_bound)
        self.utility_turtle.penup()
        self.utility_turtle.goto(self.right_bound, self.up_bound)
        self.utility_turtle.pendown()
        self.utility_turtle.goto(self.right_bound, self.down_bound)
        self.utility_turtle.penup()

        color = self.utility_turtle.pencolor()
        self.utility_turtle.pencolor("blue")
        self.utility_turtle.goto(self.right_bound, 0)
        self.utility_turtle.pendown()
        self.utility_turtle.goto(self.left_bound, 0)
        self.utility_turtle.penup()
        self.utility_turtle.goto(0, self.up_bound)
        self.utility_turtle.pendown()
        self.utility_turtle.goto(0, self.down_bound)
        self.utility_turtle.pencolor(color)
        self.utility_turtle.penup()

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
        utility_turtle.pencolor("red")
        utility_turtle.penup()
        return utility_turtle

    @staticmethod
    def get_complementary_color(r, g, b):
        pass