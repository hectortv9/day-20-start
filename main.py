from snake import Snake
from food import FoodGrid
from bounded_screen import Screen
from scoreboard import Scoreboard
import time

INITIAL_DELAY = 0.08
SCORE_THRESHOLD = 2
DELAY_DECREMENT = 0.008
SCREEN_WIDTH = 620
SCREEN_HEIGHT = 620
SCREEN_BGCOLOR = "black"
SNAKE_COLOR = "white"
SCREEN_TITLE = "Snake Game"
UP, DOWN, LEFT, RIGHT = "Up", "Down", "Left", "Right"  # Key names


class Game:

    def __init__(self):
        self.bounded_screen = Screen(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = self.bounded_screen.screen
        self.snake = Snake(3, SCREEN_BGCOLOR, True)
        self.scoreboard = Scoreboard(self.bounded_screen.up_bound)
        self.grid = FoodGrid(self.bounded_screen, self.scoreboard, self.snake.SNAKE_PART_SIZE)
        self.initialize_game()
        self.get_visual_help()

    def start_listening(self):
        self.screen.onkeypress(self.snake.left, LEFT)
        self.screen.onkeypress(self.snake.right, RIGHT)
        self.screen.onkeypress(self.snake.up, UP)
        self.screen.onkeypress(self.snake.down, DOWN)
        self.screen.listen()

    def stop_listening(self):
        self.screen.onkeypress(None, LEFT)
        self.screen.onkeypress(None, RIGHT)
        self.screen.onkeypress(None, UP)
        self.screen.onkeypress(None, DOWN)

    def initialize_game(self):
        self.screen.bgcolor(SCREEN_BGCOLOR)
        self.screen.title(SCREEN_TITLE)
        self.grid.draw_grid_edges(self.grid.screen, self.grid.boundaries)
        self.start_listening()

    def get_visual_help(self):
        self.bounded_screen.get_visual_help()
        # self.grid.draw_grid(self.grid.screen, self.grid.boundaries, self.grid.gap_size)
        self.grid.get_visual_help()

    def do_start_game(self):
        player_input = self.screen.textinput("Get ready",
                                             "Close this window whenever you are ready to start playing;\n"
                                             "otherwise, type 'quit' and press [OK] to exit game.")
        return player_input is None or player_input.lower() != "quit"

    def play(self):
        delay = INITIAL_DELAY
        while True:
            interactions = self.snake.move(self.grid)
            if interactions["did_collide"]:
                self.stop_listening()
                self.scoreboard.print_game_over()
                break
            elif interactions["did_eat"]:
                self.scoreboard.increase_score()
                if self.scoreboard.score % SCORE_THRESHOLD == 0:  # increase speed
                    delay = delay - DELAY_DECREMENT
            time.sleep(delay)
        self.screen.textinput("GAME OVER",
                              f"Your final score is {self.scoreboard.score}. Close this dialog to continue.")
        self.screen.clear()


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
if __name__ == '__main__':
    while True:
        game = Game()
        if game.do_start_game():
            game.play()
        else:
            break
