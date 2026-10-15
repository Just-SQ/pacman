from typing import Any

import pyglet
from pyglet.window import key

from src import constants, types
from src.entities.pacman import Pacman
from src.game import Game
from src.ghost import GhostMode
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
            (constants.WINDOW_HEIGHT - constants.INFO_HEIGHT) // self.rows,
            (constants.WINDOW_WIDTH - constants.INFO_WIDTH) // self.cols,
        )

        self.image_width: int = self.cols * self.tile
        self.image_height: int = self.rows * self.tile
        self.pixels: bytearray = bytearray(
            bytes(constants.BLACK) * (self.image_width * self.image_height)
        )

        wall_size = round(self.tile * 0.4)
        gap = round(wall_size * 0.4)

        self.gums_on_screen: set[tuple[int, int]] = set(self.game.pacgums)

        self._paint_walls(wall_size, constants.BLUE)
        self._paint_walls(gap, constants.TRANSPARENT_BLUE)
        self._paint_gums()

        self.maze_image: pyglet.image.ImageData = pyglet.image.ImageData(
            self.image_width,
            self.image_height,
            "RGBA",
            bytes(self.pixels),
            pitch=-self.image_width * 4,
        )
        self.maze: pyglet.sprite.Sprite = pyglet.sprite.Sprite(
            self.maze_image,
            x=(constants.WINDOW_WIDTH - self.image_width) // 2,
            y=(constants.WINDOW_HEIGHT - self.image_height) // 2,
        )
        self.supergums: dict[tuple[int, int], pyglet.sprite.Sprite] = (
            self._make_supergums()
        )
        self.pacman: Pacman = Pacman(self.tile / 13)

        left = constants.INFO_WIDTH // 2
        right = constants.WINDOW_WIDTH - left
        top = constants.WINDOW_HEIGHT - 60
        bottom = 60
        self.infos: dict[str, pyglet.text.Label] = {
            "score": self.make_label("SCORE", 20, top, left),
            "score_val": self.make_label(
                "0", 18, top - 48, left, constants.YELLOW
            ),
            "time": self.make_label("TIME", 20, top, right),
            "time_val": self.make_label(
                "0", 18, top - 48, right, constants.YELLOW
            ),
            "lives": self.make_label("LIVES", 20, bottom + 48, right),
            "level": self.make_label("LEVEL", 20, bottom + 48, left),
            "level_val": self.make_label(
                str(self.game.level), 18, bottom, left, constants.YELLOW
            ),
        }
        self.life_info_icon: Pacman = Pacman(self.tile / 13)
        self.life_info_icon.image = self.life_info_icon.frames[2]
        self.life_info_icon.y = bottom
        self.life_info_icon_x: int = constants.WINDOW_WIDTH - left - 38

        self.ghost_images: list[pyglet.image.AbstractImage] = [
            self._load_image(f"ghost_{n}") for n in range(4)
        ]
        self.scared_image: pyglet.image.AbstractImage = self._load_image(
            "ghost_scared"
        )
        self.eyes_image: pyglet.image.AbstractImage = self._load_image(
            "ghost_eyes"
        )
        self.ghosts: list[pyglet.sprite.Sprite] = self._make_ghosts()

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
        margin: int = (self.tile - size) // 2
        for col, row in self.game.pacgums:
            left: int = col * self.tile + margin
            top: int = row * self.tile + margin
            self._paint_rectangle(left, top, size, size, constants.PINK)

    def _make_supergums(self) -> dict[tuple[int, int], pyglet.sprite.Sprite]:
        image = pyglet.image.load("assets/images/supergum.png")
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2

        sprites: dict[tuple[int, int], pyglet.sprite.Sprite] = {}
        for col, row in self.game.sup_gums:
            x, y = self._tile_center(col, row)
            sprite = pyglet.sprite.Sprite(image, x=x, y=y)
            sprite.scale = self.tile * 0.6 / image.width
            sprites[col, row] = sprite
        return sprites

    def _make_ghosts(self) -> list[pyglet.sprite.Sprite]:
        sprites: list[pyglet.sprite.Sprite] = []
        for ghost in self.game.ghosts:
            image = self.ghost_images[ghost.g_id]
            image.anchor_x = image.width // 2
            image.anchor_y = image.height // 2
            sprite = pyglet.sprite.Sprite(image)
            sprite.scale = self.tile / image.width
            sprites.append(sprite)
        return sprites

    def _place_pacman(self) -> None:
        col, row = self.game.player.visual_position()
        self.pacman.x, self.pacman.y = self._tile_center(col, row)

    def _place_ghosts(self) -> None:
        for ghost, sprite in zip(self.game.ghosts, self.ghosts):
            col, row = ghost.visual_position()
            sprite.x, sprite.y = self._tile_center(col, row)
            if ghost.mode is GhostMode.FRIGHTENED:
                sprite.image = self.scared_image
            elif ghost.mode is GhostMode.EATEN:
                sprite.image = self.eyes_image
            else:
                sprite.image = self.ghost_images[ghost.g_id]

    def _tile_center(self, col: float, row: float) -> tuple[float, float]:
        left = (constants.WINDOW_WIDTH - self.image_width) // 2
        bottom = (constants.WINDOW_HEIGHT - self.image_height) // 2
        x = left + round(col * self.tile) + self.tile / 2
        y = bottom + round((self.rows - row - 1) * self.tile) + self.tile / 2
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

    def _erase_eaten_gums(self) -> None:
        eaten = self.gums_on_screen - self.game.pacgums
        for cor in eaten:
            self._erase_eaten_gum(*cor)
        self.gums_on_screen -= eaten

    def _erase_eaten_gum(self, col: int, row: int) -> None:
        size = round(self.tile * 0.2)
        margin = (self.tile - size) // 2
        black = pyglet.image.ImageData(
            size, size, "RGBA", bytes(constants.BLACK) * size**2
        )
        x = col * self.tile + margin
        top = row * self.tile + margin
        y = self.image_height - top - size
        self.maze_image.get_texture().blit_into(black, x, y, 0)

    def _draw_infos(self) -> None:
        self.infos["score_val"].text = str(self.game.score)
        self.infos["time_val"].text = str(int(self.game.time_left))
        self.infos["level_val"].text = str(self.game.level)

        for info in self.infos.values():
            info.draw()

        self.life_info_icon.x = self.life_info_icon_x
        for _ in range(self.game.lives):
            self.life_info_icon.draw()
            self.life_info_icon.x += 38

    def update(self, dt: float) -> None:
        self.game.update(constants.FPS)
        self._erase_eaten_gums()

        self._place_pacman()
        direction = self.game.player.direction
        if direction != Direction.NONE:
            self.pacman.face(direction)
            self.pacman.animate(dt)

        self._place_ghosts()

    def draw(self) -> None:
        self.maze.draw()
        for corr, supergum in self.supergums.items():
            if corr in self.game.sup_gums:
                supergum.draw()
        self.pacman.draw()
        self._draw_infos()

        for ghost in self.ghosts:
            ghost.draw()

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
