from turtle import Turtle
from tkinter.font import Font

SCORE_FONT = ("Terminal", 16, "bold")
GAME_OVER_FONT = ("Terminal", 50, "bold")
X, Y = 0, 1


class Scoreboard(Turtle):

    def __init__(self, up_bound):
        super().__init__(visible=False)
        self.score = 0
        self.scoreboard_width = 0
        self.scoreboard_height = self.get_font_height(SCORE_FONT)
        self.starting_position = 0, up_bound - self.scoreboard_height
        self.pencolor("white")
        self.speed(0)
        self.penup()
        self.print_score()

    @staticmethod
    def get_font_height(font):
        font_config = Font(font=font)
        font_ascent = font_config.metrics('ascent')
        line_space = font_config.metrics('linespace') - font_ascent
        return int(font_ascent + line_space)  # half size for line spacing is more than enough

    def print_score(self):
        self.clear()
        self.setposition(self.starting_position)
        baseline_start = self.position()[X]
        self.write(f"Score: {self.score}", move=True, align="center", font=SCORE_FONT)
        baseline_end = self.position()[X]
        self.setposition(self.starting_position)

        self.scoreboard_width = baseline_end - baseline_start

    def print_game_over(self):
        x = 0
        y = - int(self.get_font_height(GAME_OVER_FONT) / 2)
        self.color("yellow")
        rotation_degrees = 45
        for _ in range(int(360 / rotation_degrees)):
            self.setposition(x, y)
            self.right(rotation_degrees)
            self.forward(8)
            self.write("GAME OVER", move=False, align="center", font=GAME_OVER_FONT)

        self.setposition(x, y)
        self.color("red")
        self.write("GAME OVER", move=False, align="center", font=GAME_OVER_FONT)

    def increase_score(self):
        self.score += 1
        self.print_score()