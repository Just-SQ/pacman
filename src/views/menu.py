from typing import Any

import pyglet
from pyglet.window import key

from src import constants
from src.entities.pacman import Pacman
from src.views import View
from src.views.credit import CreditView
from src.views.game import GameView
from src.views.instructions import InstructionsView


class MenuView(View):
    OPTIONS: tuple[str, ...] = (
        "Start Game",
        "Leaderboard",
        "Instructions",
        "Credit",
        "Exit",
    )

    def __init__(self, settings: dict[str, Any]) -> None:
        self.settings: dict[str, Any] = settings

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

        self.options: list[pyglet.text.Label] = [
            self.make_label(
                text,
                24,
                y=constants.WINDOW_HEIGHT - 490 - i * 58,
            )
            for i, text in enumerate(self.OPTIONS)
        ]
        self.selected_option: int = 0

        self.cursor: Pacman = Pacman()

        self._move_cursor()

    def _move_cursor(self) -> None:
        for i, option in enumerate(self.options):
            option.color = (
                constants.YELLOW
                if i == self.selected_option
                else constants.LIGHT_GREY
            )

        selected_option = self.options[self.selected_option]
        self.cursor.x = (
            selected_option.x - selected_option.content_width / 2 - 42
        )
        self.cursor.y = selected_option.y

    def update(self, dt: float) -> None:
        self.cursor.animate(dt)

    def draw(self) -> None:
        self.background.draw()
        self.tagline.draw()
        for layer in self.title:
            layer.draw()
        self.rule.draw()
        self.version.draw()
        for label in self.options:
            label.draw()
        self.cursor.draw()
        self.hint.draw()

    def key_handler(self, symbol: int) -> View | None:
        if symbol == key.ESCAPE:
            pyglet.app.exit()
        if symbol in (key.UP, key.W, key.K):
            self.selected_option = (self.selected_option - 1) % len(
                self.OPTIONS
            )
            self._move_cursor()
        if symbol in (key.DOWN, key.S, key.J):
            self.selected_option = (self.selected_option + 1) % len(
                self.OPTIONS
            )
            self._move_cursor()
        if symbol in (key.RETURN, key.SPACE):
            return self._open_selected()

        return None

    def _open_selected(self) -> View | None:
        choice = self.OPTIONS[self.selected_option]

        if choice == "Start Game":
            return GameView(self, self.settings)
        if choice == "Credit":
            return CreditView(self)
        if choice == "Instructions":
            return InstructionsView(self)
        if choice == "Exit":
            pyglet.app.exit()

        return None
