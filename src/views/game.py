from typing import Any

import pyglet
from pyglet.window import key

from src import constants
from src.game import Game
from src.maze import Board
from src.views import View


class GameView(View):
    def __init__(self, menu_view: View, settings: dict[str, Any]) -> None:
        self.menu_view: View = menu_view
        self.settings: dict[str, Any] = settings

        self.game: Game = Game(self.settings)
        self.board: Board = self.game.board
        self.cols: int = len(self.board.grid[0])
        self.rows: int = len(self.board.grid)
        self.tile: int = min(
            constants.WINDOW_WIDTH // self.cols,
            constants.WINDOW_HEIGHT // self.rows,
        )

        self.walls: pyglet.sprite.Sprite = self._build_walls()

    def _build_walls(self) -> pyglet.sprite.Sprite:
        maze = [self._build_line(y) for y in reversed(range(self.rows))]

        image = pyglet.image.ImageData(
            self.cols * self.tile,
            self.rows * self.tile,
            "RGBA",
            b"".join(maze),
        )
        return pyglet.sprite.Sprite(image, x=0, y=0)

    def _build_line(self, y: int) -> bytes:
        tiles: list[bytes] = []
        for x in range(self.cols):
            if self.board.is_walkable((x, y)):
                color = constants.OPAQUE
            else:
                color = constants.BLUE
            tiles.append(bytes(color) * self.tile)
        row = b"".join(tiles)
        return row * self.tile

    def update(self, dt: float) -> None:
        self.game.update(constants.FPS)

    def draw(self) -> None:
        self.walls.draw()

    def key_handler(self, symbol: int) -> View | None:
        if symbol == key.ESCAPE:
            return self.menu_view
        return None
