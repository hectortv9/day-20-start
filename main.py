from snake import Snake
from food import FoodGrid
from bounded_screen import Screen
from scoreboard import Scoreboard
import time

snake = Snake(3)


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
    delay = 0.08
    score_threshold = 2
    delay_decrement = 0.008
    screen_width = 620
    screen_height = 620
    bounded_screen = Screen(screen_width, screen_height)
    s = bounded_screen.screen
    s.bgcolor("black")
    s.title("Snake Game")
    scoreboard = Scoreboard(bounded_screen.up_bound)
    grid = FoodGrid(bounded_screen, scoreboard, snake.SNAKE_PART_SIZE)
    grid.draw_grid_edges(grid.screen, grid.boundaries)

    # grid.draw_grid(grid.screen, grid.boundaries, grid.gap_size)
    # bounded_screen.get_visual_help()
    # grid.get_visual_help()

    start_listening(s)
    while True:

        interactions = snake.move(grid)
        if interactions["did_collide"]:
            stop_listening(s)
            scoreboard.print_game_over()
            break
        elif interactions["did_eat"]:
            scoreboard.increase_score()
            if scoreboard.score % score_threshold == 0:  # increase speed
                delay = delay - delay_decrement
        time.sleep(delay)
    s.exitonclick()


play()
