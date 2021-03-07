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
        self.grow_snake(size - 1)  # head counts as part of Snake's size

        self.snake = self.body  # TODO: DELETE

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
        for _ in range(number_of_parts):
            tail = self.body[-1]
            new_position = Snake.get_xy_decrement(tail.xcor(), tail.ycor(), tail.heading(), self.SNAKE_PART_SIZE)
            self.add_part(*new_position)

    def add_part(self, x, y):
        self.body.append(SnakePart(x, y))

    def move(self, grid):
        last_index = len(self.body) - 1
        tail_position = self.body[last_index].position()
        # for loop will move the snake except for its head
        for index in range(last_index, 0, -1):  # exclude head, it will move based on user's input
            next_position = self.body[index - 1].position()
            self.body[index].setposition(next_position[X], next_position[Y])
        else:
            self.turning = True
            heading = self.head.heading()
            position = self.head.position()
            if heading == UP and (abs(position[Y]) + self.SNAKE_PART_SIZE) > abs(grid.up_bound):
                did_collided = True
            elif heading == DOWN and (abs(position[Y]) + self.SNAKE_PART_SIZE) > abs(grid.down_bound):
                did_collided = True
            elif heading == LEFT and (abs(position[X]) + self.SNAKE_PART_SIZE) > abs(grid.left_bound):
                did_collided = True
            elif heading == RIGHT and (abs(position[X]) + self.SNAKE_PART_SIZE) > abs(grid.right_bound):
                did_collided = True
            else:
                did_collided = False
                for index in range(2, len(self.body)):
                    distance = self.head.distance(self.body[index])
                    if distance < (self.SNAKE_PART_SIZE / 2):
                        print(f"index={index}, distance={distance}, "
                              f"head={self.head.position()}, body[index]={self.body[index].position()}")
                        did_collided = True
                        break
        if did_collided:
            print(f"heading={heading}, position={position}")
            self.head.color("red")
            self.head.shape("arrow")
        else:
            self.head.forward(self.SNAKE_PART_SIZE)
            if grid.has_snake_eaten_food(self.head):
                self.add_part(*tail_position)
        self.turning = False
        return did_collided

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
