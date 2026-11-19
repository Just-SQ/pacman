from typing import Any

import pyglet
from pyglet.window import key

from src import constants
from src.views import View
from src.views.credit import CreditView
from src.views.game import GameView
from src.views.instructions import InstructionsView
from src.views.leaderboard import LeaderboardView


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

        self.background: pyglet.image.AbstractImage = self.image("menu_bg")
        self.title: pyglet.image.AbstractImage = self.image("title_pacman")

        self.hint: pyglet.text.Label = self.make_label(
            "arrow keys to choose, enter to select",
            14,
            y=84,
            color=constants.GREY,
        )

        self.options: list[pyglet.text.Label] = [
            self.text(
                text,
                300,
                y=constants.WINDOW_HEIGHT - 490 - i * 58,
            )
            for i, text in enumerate(self.OPTIONS)
        ]
        self.selected_option: int = 0
        self._move_cursor()

    def _move_cursor(self) -> None:
        for i, option in enumerate(self.options):
            option.color = (
                constants.YELLOW
                if i == self.selected_option
                else constants.LIGHT_GREY
            )

    def draw(self) -> None:
        self.background.blit(0, 0)
        self.title.blit(0, 700)
        for label in self.options:
            label.draw()
        self.hint.draw()

    def key_handler(self, symbol: int) -> View | None:
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
        if choice == "Leaderboard":
            return LeaderboardView(self, self.settings["highscore_filename"])
        if choice == "Credit":
            return CreditView(self)
        if choice == "Instructions":
            return InstructionsView(self)
        if choice == "Exit":
            pyglet.app.exit()

        return None
