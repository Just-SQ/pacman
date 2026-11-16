import pyglet
from pyglet.window import key

from src import constants
from src.views import View


class CreditView(View):
    def __init__(
        self,
        prev_view: View,
    ) -> None:
        self.prev_view: View = prev_view
        self.background: pyglet.image.AbstractImage = pyglet.image.load(
            "assets/images/menu_bg.png"
        )
        self.title: list[pyglet.text.Label] = self.make_title(
            "Credit", constants.WINDOW_HEIGHT - 200, 44
        )
        lines = [
            "A 42 project",
            "Made by rkadri and asaqi",
        ]
        self.lines: list[pyglet.text.Label] = [
            self.make_label(
                line,
                size=18,
                y=constants.WINDOW_HEIGHT - 480 - i * 56,
            )
            for i, line in enumerate(lines)
        ]
        self.hint: pyglet.text.Label = self.make_label(
            "press esc to go back", size=14, y=90, color=constants.GREY
        )

    def draw(self) -> None:
        self.background.blit(0, 0)
        for layer in self.title:
            layer.draw()
        for line in self.lines:
            line.draw()
        self.hint.draw()

    def key_handler(self, symbol: int) -> View | None:
        if symbol == key.ESCAPE:
            return self.prev_view
        return None
