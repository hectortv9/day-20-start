from turtle import Turtle
import random

X, Y = 0, 1
COLORS = ("red", "blue", "green", "magenta", "yellow", "orange", "purple", "cyan")
UP, DOWN, LEFT, RIGHT = "up", "down", "left", "right"
GRID_EDGE_COLOR = "white"
FOOD_SHAPE = "circle"
# Visual help variables
GRID_COLOR = "yellow"
FILL_GAP_COLOR = "orange"
FILL_GAP_SHAPE = "circle"


class Food(Turtle):

    def __init__(self, x, y):
        super().__init__(shape=FOOD_SHAPE, visible=True)
        self.penup()
        self.speed(0)
        self.set_position(x, y)
        self.showturtle()

    def set_position(self, x, y):
        self.setposition(x, y)
        self.color(random.choice(COLORS))


class FoodGrid:

    def __init__(self, bounded_screen, scoreboard, gap_size):
        self.screen = bounded_screen
        self.gap_size = gap_size
        self.scoreboard = scoreboard

        self.boundaries = self.get_grid_bounds()
        self.up_bound = self.boundaries[UP]
        self.left_bound = self.boundaries[LEFT]
        self.right_bound = self.boundaries[RIGHT]
        self.down_bound = self.boundaries[DOWN]

        self.lowest_gap = (int(self.left_bound + gap_size / 2), int(self.down_bound + gap_size / 2))
        self.horizontal_gap_count = int((abs(self.left_bound) + abs(self.right_bound)) / gap_size)
        self.vertical_gap_count = int((abs(self.up_bound) + abs(self.down_bound)) / gap_size)

        self.food = Food(*self.get_random_coordinate())
        self.eaten_distance = gap_size * 0.7  # distance at which food can be considered eaten by snake

    def get_random_coordinate(self):
        x = int(random.random() * self.horizontal_gap_count) * self.gap_size + self.lowest_gap[X]
        y = int(random.random() * self.vertical_gap_count) * self.gap_size + self.lowest_gap[Y]
        return x, y

    def has_snake_eaten_food(self, snake_head):
        distance = self.food.distance(snake_head.position())
        if distance < self.eaten_distance:
            self.get_more_food()
            return True
        return False

    def get_more_food(self):
        self.food.set_position(*self.get_random_coordinate())

    def get_visual_help(self):
        self.draw_grid(self.screen, self.boundaries, self.gap_size)
        self.draw_grid_edges(self.screen, self.boundaries)
        self.fill_lowest_gaps()

    @staticmethod
    def draw_grid_edges(bounded_screen, boundaries):
        color = bounded_screen.utility_turtle.pencolor()
        speed = bounded_screen.utility_turtle.speed()
        bounded_screen.utility_turtle.speed(0)
        bounded_screen.utility_turtle.pencolor(GRID_EDGE_COLOR)
        turtle = bounded_screen.utility_turtle
        turtle.goto(boundaries[LEFT], boundaries[UP])
        turtle.pendown()
        turtle.goto(boundaries[RIGHT], boundaries[UP])
        turtle.goto(boundaries[RIGHT], boundaries[DOWN])
        turtle.goto(boundaries[LEFT], boundaries[DOWN])
        turtle.goto(boundaries[LEFT], boundaries[UP])
        turtle.penup()
        bounded_screen.utility_turtle.pencolor(color)
        bounded_screen.utility_turtle.speed(speed)

    @staticmethod
    def draw_grid(bounded_screen, boundaries, gap_size):
        color = bounded_screen.utility_turtle.pencolor()
        speed = bounded_screen.utility_turtle.speed()
        bounded_screen.utility_turtle.speed(0)
        bounded_screen.utility_turtle.pencolor(GRID_COLOR)
        turtle = bounded_screen.utility_turtle
        for y in range(boundaries[DOWN], boundaries[UP] + 1, gap_size):
            turtle.goto(boundaries[LEFT], y)
            turtle.pendown()
            turtle.goto(boundaries[RIGHT], y)
            turtle.penup()
        for x in range(boundaries[LEFT], boundaries[RIGHT] + 1, gap_size):
            turtle.goto(x, boundaries[UP])
            turtle.pendown()
            turtle.goto(x, boundaries[DOWN])
            turtle.penup()
        bounded_screen.utility_turtle.pencolor(color)
        bounded_screen.utility_turtle.speed(speed)

    def fill_lowest_gaps(self):
        for x in range(self.horizontal_gap_count):
            turtle = Turtle(shape=FILL_GAP_SHAPE)
            turtle.speed(0)
            turtle.color(FILL_GAP_COLOR)
            turtle.setposition(self.lowest_gap[X] + (x * self.gap_size), self.lowest_gap[Y])
        for y in range(self.vertical_gap_count):
            turtle = Turtle(shape=FILL_GAP_SHAPE)
            turtle.speed(0)
            turtle.color(FILL_GAP_COLOR)
            turtle.setposition(self.lowest_gap[X], self.lowest_gap[Y] + (y * self.gap_size))

    @staticmethod
    def adjust_boundary(boundary, gap_size):
        # boundary is the distance between origin (0, 0) and a point at a coordinate axes
        # boundary is signed indicating the direction of axis (e.g. +x, -x, +y, -y)
        # grid will be aligned with coordinate axes but they won't overlap
        adjusted_boundary = abs(boundary)  # remove sign to work only with magnitudes
        adjusted_boundary -= abs(boundary) % (gap_size / 2)  # round down to multiples of half gap size
        if adjusted_boundary % gap_size == 0:  # means grid is aligned with origin (0, 0)
            adjusted_boundary -= gap_size / 2  #
        adjusted_boundary = int(adjusted_boundary * (abs(boundary) / boundary))  # recover sign
        return adjusted_boundary

    def get_grid_bounds(self):
        left_bound = self.screen.left_bound
        right_bound = self.screen.right_bound
        up_bound = self.screen.up_bound - self.scoreboard.scoreboard_height
        down_bound = self.screen.down_bound

        # calculate amount of gaps that can fit horizontally
        raw_width = abs(left_bound) + abs(right_bound)
        raw_width -= raw_width % self.gap_size
        # calculate amount of gaps that can fit vertically
        raw_height = abs(up_bound) + abs(down_bound)
        raw_height -= raw_height % self.gap_size
        if raw_width < self.gap_size or raw_height < self.gap_size:
            raise Exception(f"ERROR: INSUFFICIENT SPACE FOR FOOD GRID. raw_width={raw_width}, raw_height={raw_height}")
        # adjust top boundary with respect to origin and size of grid's gaps
        up = self.adjust_boundary(up_bound, self.gap_size)
        # adjust left boundary with respect to origin and size of grid's gaps
        left = self.adjust_boundary(left_bound, self.gap_size)
        # adjust right boundary with respect to origin and size of grid's gaps
        right = self.adjust_boundary(right_bound, self.gap_size)
        # adjust bottom boundary with respect to origin and size of grid's gaps
        down = self.adjust_boundary(down_bound, self.gap_size)
        if not(up > down and right > left):
            raise Exception(f"ERROR: INSUFFICIENT SPACE FOR FOOD GRID. raw_width={raw_width}, raw_height={raw_height}")

        return {UP: up, DOWN: down, LEFT: left, RIGHT: right, }
