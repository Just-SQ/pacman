from typing import Any

import pyglet
from pyglet.window import key

from src import constants, types
from src.game import Game
from src.maze import Board
from src.views import View

WALL_DEBUG = False


class GameView(View):
    def __init__(self, menu_view: View, settings: dict[str, Any]) -> None:
        self.menu_view: View = menu_view
        self.settings: dict[str, Any] = settings
        self.game: Game = Game(self.settings)

        self.board: Board = self.game.board
        self.cols: int = len(self.board.grid[0])
        self.rows: int = len(self.board.grid)
        self.tile: int = min(
            constants.WINDOW_HEIGHT // self.rows,
            constants.WINDOW_WIDTH // self.cols,
        )

        self.image_width: int = self.cols * self.tile
        self.image_height: int = self.rows * self.tile
        self.pixels: bytearray = bytearray(
            bytes(constants.BLACK) * (self.image_width * self.image_height)
        )

        line = max(1, self.tile // 10)
        gap = max(1, self.tile // 5)

        self.wall_debug: bool = WALL_DEBUG
        self._paint_walls(2 * line + gap, constants.BLUE)
        self.wall_debug = False
        self._paint_walls(gap, constants.BLACK)

        self.maze: pyglet.sprite.Sprite = pyglet.sprite.Sprite(
            pyglet.image.ImageData(
                self.image_width,
                self.image_height,
                "RGBA",
                bytes(self.pixels),
                pitch=-self.image_width * 4,
            ),
            x=(constants.WINDOW_WIDTH - self.image_width) // 2,
            y=(constants.WINDOW_HEIGHT - self.image_height) // 2,
        )

    def _paint_walls(self, size: int, color: types.Color) -> None:
        if self.wall_debug:
            for row in range(self.rows):
                for col in range(self.cols):
                    tile_color = (
                        constants.LIGHT_GREY
                        if (col + row) % 2
                        else constants.BROWN
                    )
                    if not self.board.is_walkable((col, row)):
                        self._paint_rectangle(
                            col * self.tile,
                            row * self.tile,
                            self.tile,
                            self.tile,
                            tile_color,
                        )

        margin = (self.tile - size) // 2
        wall_extention = self.tile - size

        for row in range(self.rows):
            for col in range(self.cols):
                if self.board.is_walkable((col, row)):
                    continue

                top = row * self.tile + margin
                left = col * self.tile + margin

                self._paint_rectangle(left, top, size, size, color)

                if col + 1 < self.cols and not self.board.is_walkable(
                    (col + 1, row)
                ):
                    self._paint_rectangle(
                        left + size, top, wall_extention, size, color
                    )
                if row + 1 < self.rows and not self.board.is_walkable(
                    (col, row + 1)
                ):
                    self._paint_rectangle(
                        left, top + size, size, wall_extention, color
                    )
                if (
                    col + 1 < self.cols
                    and row + 1 < self.rows
                    and not self.board.is_walkable((col + 1, row))
                    and not self.board.is_walkable((col, row + 1))
                    and not self.board.is_walkable((col + 1, row + 1))
                ):
                    self._paint_rectangle(
                        left + size,
                        top + size,
                        wall_extention,
                        wall_extention,
                        color,
                    )

    def _paint_rectangle(
        self, left: int, top: int, width: int, height: int, color: types.Color
    ) -> None:
        for y in range(top, top + height):
            start = (left + y * self.image_width) * 4
            end = start + width * 4
            self.pixels[start:end] = bytes(color) * width

    def update(self, dt: float) -> None: ...

    def draw(self) -> None:
        self.maze.draw()

    def key_handler(self, symbol: int) -> View | None:
        if symbol == key.ESCAPE:
            return self.menu_view
        return None
