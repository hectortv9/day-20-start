from turtle import Turtle
from screen_box import ScreenBox

RIGHT = 0
UP = 90
LEFT = 180
DOWN = 270

X, Y = 0, 1
snake_color = "magenta"


class SnakePart(Turtle):

    def __init__(self, x, y, color=None):
        super().__init__(shape="square", visible=False)
        color = snake_color if color is None else color
        self.penup()
        self.speed(0)
        self.color(color)
        self.setposition(x, y)
        self.showturtle()


class Snake:

    def __init__(self, size, color=snake_color):
        self.set_snake_default_color(color)
        self.SNAKE_PART_SIZE = 20
        self.turning = False
        self.body = [SnakePart(0, 0)]
        self.head = self.body[0]
        self.grow_snake(size - 1)  # head counts as part of Snake's size

    @staticmethod
    def set_snake_default_color(color):
        global snake_color
        snake_color = color

    @staticmethod
    def get_xy_increment(x, y, heading, distance):
        """Returns a tuple with the new (x,y) coordinate."""
        return Snake.get_xy_some_crement(x, y, heading, distance, 1)

    @staticmethod
    def get_xy_decrement(x, y, heading, distance):
        """Returns a tuple with the new (x,y) coordinate."""
        return Snake.get_xy_some_crement(x, y, heading, distance, -1)

    @staticmethod
    def get_xy_some_crement(x, y, heading, distance, signed_multiplicative_identity):
        """Returns a tuple with the new (x,y) coordinate."""
        return {
            RIGHT: (x + distance * signed_multiplicative_identity, y),
            UP: (x, y + distance * signed_multiplicative_identity),
            LEFT: (x - distance * signed_multiplicative_identity, y),
            DOWN: (x, y - distance * signed_multiplicative_identity),
        }[heading]

    def grow_snake(self, number_of_parts):
        ScreenBox().screen.tracer(0)
        for _ in range(number_of_parts):
            tail = self.body[-1]
            new_position = Snake.get_xy_decrement(tail.xcor(), tail.ycor(), tail.heading(), self.SNAKE_PART_SIZE)
            self.add_part(*new_position)
        ScreenBox().screen.tracer(1)

    def add_part(self, x, y):
        self.body.append(SnakePart(x, y))

    def move(self, grid):
        ScreenBox().screen.tracer(0)
        original_heading = self.head.heading()
        original_position = self.head.position()
        self.head.forward(self.SNAKE_PART_SIZE)
        position = self.head.position()
        # check collision with boundaries
        did_eat = False
        if (position[X] < grid.left_bound or position[X] > grid.right_bound
                or position[Y] < grid.down_bound or position[Y] > grid.up_bound):
            did_collide = True
        else:
            # check collision with snake's body
            for part in self.body[3:]:  # start from one to exclude snake's head
                if self.head.distance(part) < (self.SNAKE_PART_SIZE / 2):
                    did_collide = True
                    break
            else:
                did_collide = False
                did_eat = grid.has_snake_eaten_food(self.head)
        if did_collide:
            self.turning = True
            self.head.setposition(original_position)
            self.head.setheading(original_heading)
            collision_indicator = SnakePart(*original_position)
            collision_indicator.setheading(original_heading)
            collision_indicator.color("red")
            collision_indicator.shape("arrow")
        else:
            for part in self.body[1:]:  # start from one to exclude snake's head
                position = part.position()
                part.setposition(original_position)
                original_position = position
            if did_eat:
                self.add_part(*original_position)
        ScreenBox().screen.tracer(1)
        return {"did_collide": did_collide, "did_eat": did_eat}

    def left(self):
        if self.turning:
            return
        self.turning = True
        if self.head.heading() in (UP, DOWN):
            self.head.setheading(LEFT)
        self.turning = False

    def right(self):
        if self.turning:
            return
        self.turning = True
        if self.head.heading() in (UP, DOWN):
            self.head.setheading(RIGHT)
        self.turning = False

    def up(self):
        if self.turning:
            return
        self.turning = True
        if self.head.heading() in (LEFT, RIGHT):
            self.head.setheading(UP)
        self.turning = False

    def down(self):
        if self.turning:
            return
        self.turning = True
        if self.head.heading() in (LEFT, RIGHT):
            self.head.setheading(DOWN)
        self.turning = False
