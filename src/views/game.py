from typing import Any

import pyglet

from src import constants, types
from src.game import Game
from src.maze import Board
from src.views import View


class GameView(View):
    def __init__(self, menu_view: View, settings: dict[str, Any]) -> None:
        self.menu_view: View = menu_view
        self.settings: dict[str, Any] = settings
        self.game: Game = Game(self.settings)

        self._build_maze()

    def _build_maze(self) -> None:
        self.board: Board = self.game.board
        self.cols: int = len(self.board.grid[0])
        self.rows: int = len(self.board.grid)
        self.tile: int = 20

        self.image_width: int = self.cols * self.tile
        self.image_height: int = self.rows * self.tile
        self.pixels: list[list[bytes]] = [
            [bytes(constants.BLACK)] * self.image_width
            for _ in range(self.image_height)
        ]

        wall_size = round(self.tile * 0.6)
        self._paint_walls(wall_size, constants.BLUE)
        self._paint_walls(round(wall_size * 0.3), constants.BLACK)

        self.maze: pyglet.image.ImageData = pyglet.image.ImageData(
            self.image_width,
            self.image_height,
            "RGBA",
            b"".join(pixel for line in self.pixels for pixel in line),
            pitch=-self.image_width * 4,
        )

    def _paint_walls(self, size: int, color: types.Color) -> None:
        margin = (self.tile - size) // 2
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board.is_walkable((col, row)):
                    continue

                x = col * self.tile + margin
                y = row * self.tile + margin
                self._paint_rectangle(x, y, size, size, color)

                if (
                    not self.board.is_walkable((col + 1, row))
                    and col + 1 < self.cols
                ):
                    self._paint_rectangle(x + size, y, margin * 2, size, color)

                if (
                    not self.board.is_walkable((col, row + 1))
                    and row + 1 < self.rows
                ):
                    self._paint_rectangle(x, y + size, size, margin * 2, color)

    def _paint_rectangle(
        self, x: int, y: int, width: int, height: int, color: types.Color
    ):
        for line in range(y, y + height):
            self.pixels[line][x : x + width] = [bytes(color)] * width

    def draw(self) -> None:
        self.maze.blit(
            (constants.WINDOW_WIDTH // 2 - self.image_width // 2),
            (constants.WINDOW_HEIGHT // 2 - self.image_height // 2),
        )
