from typing import Any

import pyglet
from pyglet.window import key

from src import constants
from src.game import Game
from src.maze import Board
from src.views import View

Color = tuple[int, int, int, int]


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

        self.image_width: int = self.cols * self.tile
        self.image_height: int = self.rows * self.tile
        self.pixels: bytearray = bytearray(
            bytes(constants.OPAQUE) * (self.image_width * self.image_height)
        )

        line = max(1, self.tile // 10)
        gap = max(2, self.tile // 5)
        self._draw_walls(2 * line + gap, constants.BLUE)
        self._draw_walls(gap, constants.OPAQUE)

        self.walls: pyglet.sprite.Sprite = self._make_sprite()

    def _make_sprite(self) -> pyglet.sprite.Sprite:
        image = pyglet.image.ImageData(
            self.image_width,
            self.image_height,
            "RGBA",
            bytes(self.pixels),
            pitch=-self.image_width * 4,
        )
        return pyglet.sprite.Sprite(
            image,
            x=(constants.WINDOW_WIDTH - self.image_width) // 2,
            y=(constants.WINDOW_HEIGHT - self.image_height) // 2,
        )

    def _fill_rect(
        self,
        left: int,
        top: int,
        width: int,
        height: int,
        color: Color,
    ) -> None:
        for y in range(top, top + height):
            start = (left + y * self.image_width) * 4
            end = start + width * 4
            self.pixels[start:end] = bytes(color) * width

    def _draw_walls(self, size: int, color: Color) -> None:
        margin = (self.tile - size) // 2
        arm_length = self.tile + size
        for row in range(self.rows):
            for col in range(self.cols):
                if not self._is_wall(col, row):
                    continue
                left = col * self.tile + margin
                top = row * self.tile + margin

                self._fill_rect(left, top, size, size, color)

                if self._is_wall(col + 1, row):
                    self._fill_rect(left, top, arm_length, size, color)

                if self._is_wall(col, row + 1):
                    self._fill_rect(left, top, size, arm_length, color)
                if (
                    self._is_wall(col + 1, row)
                    and self._is_wall(col, row + 1)
                    and self._is_wall(col + 1, row + 1)
                ):
                    self._fill_rect(left, top, arm_length, arm_length, color)

    def _is_wall(self, col: int, row: int) -> bool:
        inside = 0 <= col < self.cols and 0 <= row < self.rows
        return inside and not self.board.is_walkable((col, row))

    def update(self, dt: float) -> None:
        self.game.update(constants.FPS)

    def draw(self) -> None:
        self.walls.draw()

    def key_handler(self, symbol: int) -> View | None:
        if symbol == key.ESCAPE:
            return self.menu_view
        return None
