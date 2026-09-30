from typing import Any

from pyglet.window import key

from src import constants
from src.game import Game
from src.views import View


class GameView(View):
    def __init__(self, menu_view: View, settings: dict[str, Any]) -> None:
        self.menu_view: View = menu_view
        self.settings: dict[str, Any] = settings
        self.game: Game = Game(self.settings)

        print(len(self.game.board.grid))

    def update(self, dt: float) -> None:
        self.game.update(constants.FPS)

    def draw(self) -> None: ...

    def key_handler(self, symbol: int) -> View | None:
        if symbol == key.ESCAPE:
            return self.menu_view
        return None
