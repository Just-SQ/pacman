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
        tiles = [self._tile_rows(x, y) for x in range(self.cols)]
        rows: list[bytes] = []
        for py in range(self.tile):
            rows.append(b"".join(tile[py] for tile in tiles))
        return b"".join(rows)

    def _tile_rows(self, x: int, y: int) -> list[bytes]:
        if self.board.is_walkable((x, y)):
            return [bytes(constants.OPAQUE) * self.tile] * self.tile

        def floor_at(dx: int, dy: int) -> bool:
            return self.board.is_walkable((x + dx, y + dy))

        line = bytes(constants.BLUE) * self.tile
        middle = self._wall_row(floor_at(-1, 0), floor_at(1, 0))
        bottom = self._wall_row(
            floor_at(-1, 0) or floor_at(-1, 1),
            floor_at(1, 0) or floor_at(1, 1),
        )
        top = self._wall_row(
            floor_at(-1, 0) or floor_at(-1, -1),
            floor_at(1, 0) or floor_at(1, -1),
        )
        if floor_at(0, 1):
            bottom = line
        if floor_at(0, -1):
            top = line
        return [bottom] * 2 + [middle] * (self.tile - 4) + [top] * 2

    def _wall_row(self, left: bool, right: bool) -> bytes:
        lw = 2 if left else 0
        rw = 2 if right else 0
        return (
            bytes(constants.BLUE) * lw
            + bytes(constants.OPAQUE) * (self.tile - lw - rw)
            + bytes(constants.BLUE) * rw
        )

    def update(self, dt: float) -> None:
        self.game.update(constants.FPS)

    def draw(self) -> None:
        self.walls.draw()

    def key_handler(self, symbol: int) -> View | None:
        if symbol == key.ESCAPE:
            return self.menu_view
        return None
