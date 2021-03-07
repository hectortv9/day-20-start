from turtle import Turtle

RIGHT = 0
UP = 90
LEFT = 180
DOWN = 270

X, Y = 0, 1


class SnakePart(Turtle):

    def __init__(self, x, y):
        super().__init__(shape="square", visible=False)
        self.penup()
        self.speed(0)
        self.color("white")
        self.setposition(x, y)
        self.showturtle()


class Snake:

    def __init__(self, size):
        self.SNAKE_PART_SIZE = 20
        self.turning = False
        self.body = [SnakePart(0, 0)]
        self.head = self.body[0]
        self.screen = self.head.getscreen()
        self.grow_snake(size - 1)  # head counts as part of Snake's size

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
            0: (x + distance * signed_multiplicative_identity, y),
            90: (x, y + distance * signed_multiplicative_identity),
            180: (x - distance * signed_multiplicative_identity, y),
            270: (x, y - distance * signed_multiplicative_identity),
        }[heading]

    def grow_snake(self, number_of_parts):
        self.screen.tracer(0)
        for _ in range(number_of_parts):
            tail = self.body[-1]
            new_position = Snake.get_xy_decrement(tail.xcor(), tail.ycor(), tail.heading(), self.SNAKE_PART_SIZE)
            self.add_part(*new_position)
        self.screen.tracer(1)

    def add_part(self, x, y):
        self.body.append(SnakePart(x, y))

    def move(self, grid):
        self.screen.tracer(0)
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
            for index in range(1, len(self.body)):  # start from one to exclude snake's head
                distance = self.head.distance(self.body[index])
                if distance < (self.SNAKE_PART_SIZE / 2):
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
            for index in range(1, len(self.body)):  # start from one to exclude snake's head
                position = self.body[index].position()
                self.body[index].setposition(original_position)
                original_position = position
            if did_eat:
                self.add_part(*original_position)
        self.screen.tracer(1)
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