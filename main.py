from snake import Snake
from food import FoodGrid
from bounded_screen import Screen
from scoreboard import Scoreboard
import time

snake = None

def start_listening(screen):
    screen.onkeypress(snake.left, "Left")
    screen.onkeypress(snake.right, "Right")
    screen.onkeypress(snake.up, "Up")
    screen.onkeypress(snake.down, "Down")
    screen.listen()

def stop_listening(screen):
    screen.onkeypress(None, "Left")
    screen.onkeypress(None, "Right")
    screen.onkeypress(None, "Up")
    screen.onkeypress(None, "Down")

def play():
    global snake
    screen_width = 620
    screen_height = 620
    bounded_screen = Screen(screen_width, screen_height)
    s = bounded_screen.screen
    s.bgcolor("black")
    s.title("Snake Game")
    #s.tracer(0)
    snake = Snake(3)
    s.tracer(1)
    scoreboard = Scoreboard(bounded_screen.up_bound)
    grid = FoodGrid(bounded_screen, scoreboard, snake.SNAKE_PART_SIZE)
    grid.draw_grid_edges(grid.screen, grid.boundaries)

    # grid.draw_grid(grid.screen, grid.boundaries, grid.gap_size)
    # bounded_screen.get_visual_help()
    # grid.get_visual_help()

    start_listening(s)
    while True:

        did_collided = snake.move(grid)
        if did_collided:
            stop_listening(s)
            scoreboard.print_game_over()
            break
        """
        #did_collided = snake.move2(grid.up_bound, grid.down_bound, grid.left_bound, grid.right_bound)
        heading = snake.get_heading()
        will_eat = snake.will_eat(grid.eaten_distance, grid.food)
        if will_eat and heading == snake.get_heading():
            snake.snake.append(snake.eat(snake.get_snake_head()))
            will_collide = False
        else:
            will_collide = snake.will_collide(grid.up_bound, grid.down_bound, grid.left_bound, grid.right_bound)
            snake.move(will_collide)

        if will_collide:
            stop_listening(s)
            scoreboard.print_game_over()
            break
        was_eaten = grid.has_snake_eaten_food(snake.get_snake_head())
        if was_eaten:
            grid.get_more_food()
            scoreboard.increase_score()
        #snake.block_turning(False)"""
        time.sleep(0.1)
    s.exitonclick()


play()
