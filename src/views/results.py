import pyglet
from pyglet.window import key

from src import constants
from src.views import View


class ResultsView(View):
    def __init__(self, menu_view: View, victory: bool, score: int) -> None:
        self.menu_view: View = menu_view
        self.score: int = score
        self.name: str = ""

        self.background: pyglet.sprite.Sprite = pyglet.sprite.Sprite(
            pyglet.image.load("assets/images/menu_bg.png"),
            x=0,
            y=0,
        )
        self.title: list[pyglet.text.Label] = self.make_title(
            "YOU WIN!" if victory else "GAME OVER",
            constants.WINDOW_HEIGHT - 260,
            64,
        )
        self.score_label: pyglet.text.Label = self.make_label(
            f"SCORE {score}", 24, 640, color=constants.YELLOW
        )
        self.prompt: pyglet.text.Label = self.make_label(
            "ENTER YOUR NAME", 18, 520, color=constants.GREY
        )
        self.name_label: pyglet.text.Label = self.make_label(
            f"{self.name:_<10}", 36, 440
        )
        self.hint: pyglet.text.Label = self.make_label(
            "press enter to save", 14, 90, color=constants.GREY
        )

    def draw(self) -> None:
        self.background.draw()
        for layer in self.title:
            layer.draw()
        self.score_label.draw()
        self.prompt.draw()
        self.name_label.draw()
        self.hint.draw()

    def key_handler(self, symbol: int) -> View | None:
        if symbol == key.RETURN:
            return self.menu_view
        return None
