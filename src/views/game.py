from typing import Any

import pyglet
from pyglet.window import key

from src import constants, types
from src.entities.pacman import Pacman
from src.game import Game
from src.maze import Board
from src.utils.entity import Direction
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
            constants.WINDOW_HEIGHT // self.rows,
            constants.WINDOW_WIDTH // self.cols,
        )

        self.image_width: int = self.cols * self.tile
        self.image_height: int = self.rows * self.tile
        self.pixels: bytearray = bytearray(
            bytes(constants.BLACK) * (self.image_width * self.image_height)
        )

        wall_size = round(self.tile * 0.4)
        gap = round(wall_size * 0.4)

        self._paint_walls(wall_size, constants.BLUE)
        self._paint_walls(gap, constants.TRANSPARENT_BLUE)
        self._paint_gums()

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
        self.supergums: list[pyglet.sprite.Sprite] = self._make_supergums()
        self.pacman: Pacman = Pacman(self.tile / 13)

    def _paint_walls(self, size: int, color: types.Color) -> None:
        margin = (self.tile - size) // 2
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board.is_walkable((col, row)):
                    continue

                left = col * self.tile + margin
                top = row * self.tile + margin
                self._paint_rounded_square(left, top, size, color)

                if col + 1 < self.cols and not self.board.is_walkable(
                    (col + 1, row)
                ):
                    self._paint_rectangle(
                        left + round(size * 0.8),
                        top,
                        self.tile,
                        size,
                        color,
                    )
                if row + 1 < self.rows and not self.board.is_walkable(
                    (col, row + 1)
                ):
                    self._paint_rectangle(
                        left,
                        top + round(size * 0.8),
                        size,
                        self.tile,
                        color,
                    )
                if (
                    col + 1 < self.cols
                    and row + 1 < self.rows
                    and not self.board.is_walkable((col + 1, row))
                    and not self.board.is_walkable((col, row + 1))
                    and not self.board.is_walkable((col + 1, row + 1))
                ):
                    self._paint_rectangle(
                        left + round(size * 0.8),
                        top + round(size * 0.8),
                        self.tile,
                        self.tile,
                        color,
                    )

    def _paint_gums(self) -> None:
        size = round(self.tile * 0.2)
        for col, row in self.game.pacgums:
            margin: int = (self.tile - size) // 2
            left: int = col * self.tile + margin
            top: int = row * self.tile + margin
            self._paint_rectangle(left, top, size, size, constants.PINK)

    def _make_supergums(self) -> list[pyglet.sprite.Sprite]:
        image = pyglet.image.load("assets/images/supergum.png")
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2

        sprites: list[pyglet.sprite.Sprite] = []
        for col, row in self.game.sup_gums:
            x, y = self._tile_center(col, row)
            sprite = pyglet.sprite.Sprite(image, x=x, y=y)
            sprite.scale = self.tile * 0.6 / image.width
            sprites.append(sprite)
        return sprites

    def _place_pacman(self) -> None:
        col, row = self.game.player.visual_position()
        self.pacman.x, self.pacman.y = self._tile_center(col, row)

    def _tile_center(self, col: float, row: float) -> tuple[float, float]:
        left = (constants.WINDOW_WIDTH - self.image_width) // 2
        bottom = (constants.WINDOW_HEIGHT - self.image_height) // 2
        x = left + (col + 0.5) * self.tile
        y = bottom + (self.rows - row - 0.5) * self.tile
        return x, y

    def _paint_rounded_square(
        self, left: int, top: int, size: int, color: types.Color
    ) -> None:
        notch = round(size * 0.2)
        thickness = size - 2 * notch
        self._paint_rectangle(left + notch, top, thickness, size, color)
        self._paint_rectangle(left, top + notch, size, thickness, color)

    def _paint_rectangle(
        self, left: int, top: int, width: int, height: int, color: types.Color
    ) -> None:
        for y in range(top, top + height):
            start = (left + y * self.image_width) * 4
            end = start + width * 4
            self.pixels[start:end] = bytes(color) * width

    def update(self, dt: float) -> None:
        self.game.update(constants.FPS)

        self._place_pacman()
        direction = self.game.player.direction
        if direction != Direction.NONE:
            self.pacman.face(direction)
            self.pacman.animate(dt)

    def draw(self) -> None:
        self.maze.draw()
        for supergum in self.supergums:
            supergum.draw()
        self.pacman.draw()

    def key_handler(self, symbol: int) -> View | None:
        if symbol in (key.UP, key.W, key.K):
            self.game.player.dir_wanted = Direction.UP
        if symbol in (key.DOWN, key.S, key.J):
            self.game.player.dir_wanted = Direction.DOWN
        if symbol in (key.LEFT, key.A, key.H):
            self.game.player.dir_wanted = Direction.LEFT
        if symbol in (key.RIGHT, key.D, key.L):
            self.game.player.dir_wanted = Direction.RIGHT
        if symbol == key.ESCAPE:
            return self.menu_view
        return None
