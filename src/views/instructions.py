import pyglet
from pyglet.window import key

from src import constants
from src.views import View


class InstructionsView(View):
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
            "Instructions", constants.WINDOW_HEIGHT - 200, 44
        )
        lines = [
            "Move: arrow keys, WASD, or HJKL",
            "Pause: Esc (then Q for main menu)",
            "Cheat: I(=invincibility), N(=next level), E(=extra life)",
            "Eat every pacgum to clear the level",
            "Touching a ghost costs one life",
            "Super-pacgums make ghosts temporarily edible",
        ]
        self.lines: list[pyglet.text.Label] = [
            self.make_label(
                line,
                size=18,
                y=constants.WINDOW_HEIGHT - 420 - i * 56,
            )
            for i, line in enumerate(lines)
        ]
        self.hint: pyglet.text.Label = self.make_label(
            "press esc to go back", size=14, y=90, color=constants.GREY
        )

    def draw(self) -> None:
        self.background.draw()
        for layer in self.title:
            layer.draw()
        for line in self.lines:
            line.draw()
        self.hint.draw()

    def key_handler(self, symbol: int) -> View | None:
        if symbol == key.ESCAPE:
            return self.prev_view
        return None
