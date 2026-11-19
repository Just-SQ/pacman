import time
from typing import Any

import pyglet
from pyglet.window import key

from src import constants, types
from src.entities.pacman import Pacman
from src.game import Game, State
from src.ghost import GhostMode
from src.maze import Board
from src.utils.entity import Direction
from src.views import View
from src.views.results import ResultsView


class GameView(View):
    def __init__(self, menu_view: View, settings: dict[str, Any]) -> None:
        self.menu_view: View = menu_view
        self.settings: dict[str, Any] = settings
        self.game: Game = Game(self.settings)

        self._build_maze()

        self.pacman: Pacman = Pacman()

        self.supergum: pyglet.image.AbstractImage = self.image("supergum")

        self.ghosts: list[pyglet.image.AbstractImage] = [
            self.image(f"ghost_{i}") for i in range(4)
        ]
        self.eaten_ghost: pyglet.image.AbstractImage = self.image("ghost_eyes")
        self.scared_ghost: pyglet.image.AbstractImage = self.image(
            "ghost_scared"
        )

        self.infos: dict[str, pyglet.text.Label] = {
            "score": self.text(
                f"SCORE/ {0}",
                15,
                constants.WINDOW_HEIGHT - 25,
                12,
                constants.LIGHT_GREY,
            ),
            "time": self.text(
                f"TIME/ {
                    time.strftime('%M:%S', time.gmtime(self.game.time_left))
                }",
                25,
                25,
                12,
                constants.LIGHT_GREY,
            ),
            "level": self.text(
                f"LEVEL/ {1}",
                constants.WINDOW_WIDTH - 85,
                constants.WINDOW_HEIGHT - 25,
                12,
                constants.LIGHT_GREY,
            ),
            "lives": self.text(
                f"LIVES/ {self.game.lives}",
                constants.WINDOW_WIDTH - 85,
                25,
                12,
                constants.LIGHT_GREY,
            ),
        }

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

        self.maze_start_x: int = (
            constants.WINDOW_WIDTH // 2 - self.image_width // 2
        )
        self.maze_start_y: int = (
            constants.WINDOW_HEIGHT // 2 - self.image_height // 2
        )

        wall_size = round(self.tile * 0.6)
        self._paint_walls(wall_size, constants.BLUE)
        self._paint_walls(round(wall_size * 0.3), constants.BLACK)

        self.maze: pyglet.image.ImageData = pyglet.image.ImageData(
            self.image_width,
            self.image_height,
            "RGBA",
            b"".join(b"".join(line) for line in self.pixels),
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
    ) -> None:
        for line in range(y, y + height):
            end = x + width
            self.pixels[line][x:end] = [bytes(color)] * width

    def _draw_supergums(self) -> None:
        for pos in self.game.sup_gums:
            x, y = self.get_center_tile(*pos)
            self.supergum.blit(x + 4, y + 4)

    def _draw_ghosts(self) -> None:
        for ghost, image in zip(self.game.ghosts, self.ghosts):
            x, y = self.get_center_tile(*ghost.visual_position())
            if ghost.mode is GhostMode.FRIGHTENED:
                self.scared_ghost.blit(x, y)
            elif ghost.mode is GhostMode.EATEN:
                self.eaten_ghost.blit(x, y)
            else:
                image.blit(x, y)

    def update_info(self) -> None:
        self.infos["score"].text = f"SCORE/ {self.game.score}"
        self.infos[
            "time"
        ].text = (
            f"TIME/ {time.strftime('%M:%S', time.gmtime(self.game.time_left))}"
        )
        self.infos["level"].text = f"LEVEL/ {self.game.level}"
        self.infos["lives"].text = f"LIVES/ {self.game.lives}"

    def get_center_tile(self, col: float, row: float) -> tuple[int, int]:
        x = self.maze_start_x + col * self.tile
        y = self.maze_start_y + self.image_height - (row + 1) * self.tile
        return int(x), int(y)

    def update(self, dt: float) -> View | None:
        if self.game.state in (State.VICTORY, State.GAME_OVER):
            return ResultsView(
                self.menu_view,
                self.settings["highscore_filename"],
                self.game.state is State.VICTORY,
                self.game.score,
            )

        if self.board is not self.game.board:
            self._build_maze()

        self.game.update(dt)

        self.pacman.update(dt)
        self.pacman.x, self.pacman.y = self.get_center_tile(
            *self.game.player.visual_position()
        )
        self.pacman.face(self.game.player.direction)

        self.update_info()

        return None

    def draw(self) -> None:
        self.maze.blit(self.maze_start_x, self.maze_start_y)
        self.pacman.draw()
        self._draw_supergums()
        self._draw_ghosts()

        for info in self.infos.values():
            info.draw()

    def key_handler(self, symbol: int) -> View | None:
        if symbol in (key.UP, key.W, key.K):
            self.game.player.dir_wanted = Direction.UP
        if symbol in (key.DOWN, key.S, key.J):
            self.game.player.dir_wanted = Direction.DOWN
        if symbol in (key.LEFT, key.A, key.H):
            self.game.player.dir_wanted = Direction.LEFT
        if symbol in (key.RIGHT, key.D, key.L):
            self.game.player.dir_wanted = Direction.RIGHT
        return None
