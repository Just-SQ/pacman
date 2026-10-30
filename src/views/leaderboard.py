import pyglet
from pyglet.window import key

from src import constants
from src.views import View


class LeaderboardView(View):
    def __init__(
        self,
        prev_view: View,
    ) -> None:
        self.prev_view: View = prev_view
        self.background: pyglet.sprite.Sprite = pyglet.sprite.Sprite(
            pyglet.image.load("assets/images/menu_bg.png"),
            x=0,
            y=0,
        )
        self.title: list[pyglet.text.Label] = self.make_title(
            "Leaderboard", constants.WINDOW_HEIGHT - 200, 44
        )

    def draw(self) -> None:
        self.background.draw()
        for line in self.title:
            line.draw()

    def key_handler(self, symbol: int) -> View | None:
        if symbol == key.ESCAPE:
            return self.prev_view
        return None
