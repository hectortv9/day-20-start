from screen_box import ScreenBox
import snake
import food
import scoreboard
import time

INITIAL_DELAY = 0.08
SCORE_THRESHOLD = 2
DELAY_DECREMENT = 0.008
UP, DOWN, LEFT, RIGHT = "Up", "Down", "Left", "Right"  # Key names
SCREEN_TITLE = "Snake Game"


class Game:

    def __init__(self):
        self.screen_box = ScreenBox(title=SCREEN_TITLE)
        self.screen = self.screen_box.screen
        self.snake = snake.Snake(3, self.screen_box.complementary_color)
        self.scoreboard = scoreboard.Scoreboard(self.screen_box.up_bound, self.screen_box.complementary_color)
        self.grid = food.FoodGrid(self.scoreboard, self.snake.SNAKE_PART_SIZE)
        self.initialize_game()
        # self.get_visual_help()

    def start_listening(self):
        self.screen.onkeypress(self.snake.left, LEFT)
        self.screen.onkeypress(self.snake.right, RIGHT)
        self.screen.onkeypress(self.snake.up, UP)
        self.screen.onkeypress(self.snake.down, DOWN)
        self.screen.listen()

    def initialize_game(self):
        self.grid.draw_grid_edges(self.screen_box.complementary_color)
        self.start_listening()

    def get_visual_help(self):
        self.screen_box.get_visual_help()
        self.grid.draw_grid()
        self.grid.get_visual_help()

    def stop_listening(self):
        self.screen.onkeypress(None, LEFT)
        self.screen.onkeypress(None, RIGHT)
        self.screen.onkeypress(None, UP)
        self.screen.onkeypress(None, DOWN)

    def do_start_game(self):
        player_input = self.screen.textinput(
            "Get ready", "Close this window whenever you are ready to start playing;\n "
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
        self.screen.textinput(
            "GAME OVER", f"Your final score is {self.scoreboard.score}. Close this dialog to continue.")
        self.screen_box.clear_screen()
