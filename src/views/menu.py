import pyglet
from pyglet.window import key

from src import constants

from .view import View


class MenuView(View):
    OPTIONS: tuple[str, ...] = (
        "Start game",
        "Leaderboard",
        "Instructions",
        "Credit",
        "Exit",
    )

    def __init__(self) -> None:
        self.background: pyglet.sprite.Sprite = pyglet.sprite.Sprite(
            pyglet.image.load("assets/images/menu_bg.png"),
            x=0,
            y=0,
        )
        self.tagline: pyglet.text.Label = self.make_label(
            "ghosts! skcus iqasA!", 24, y=882, color=constants.YELLOW
        )
        self.title: list[pyglet.text.Label] = self.make_title(
            "PAC-MAN", size=96, y=768
        )
        self.rule: pyglet.sprite.Sprite = pyglet.sprite.Sprite(
            pyglet.image.SolidColorImagePattern(constants.YELLOW).create_image(
                864, 6
            ),
            x=290,
            y=682,
        )
        self.version: pyglet.text.Label = self.make_label(
            "v13.37",
            20,
            y=646,
            x=1154,
            anchor_x="right",
        )
        self.hint: pyglet.text.Label = self.make_label(
            "arrow keys to choose, enter to select",
            14,
            y=84,
            color=constants.GREY,
        )

    def draw(self) -> None:
        self.background.draw()
        self.tagline.draw()
        for layer in self.title:
            layer.draw()
        self.rule.draw()
        self.version.draw()
        self.hint.draw()

    def key_handler(self, symbol: int) -> View | None:
        if symbol == key.ESCAPE:
            pyglet.app.exit()
        return None
