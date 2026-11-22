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
        self.invicible_text: pyglet.text.Label = self.text(
            "INVINCIBLE",
            25,
            constants.WINDOW_HEIGHT - 85,
            14,
            constants.YELLOW,
        )

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
                f"SCORE: {0}",
                25,
                constants.WINDOW_HEIGHT - 25,
                14,
                constants.LIGHT_GREY,
            ),
            "time": self.text(
                f"TIME: {
                    time.strftime('%M:%S', time.gmtime(self.game.time_left))
                }",
                25,
                25,
                14,
                constants.LIGHT_GREY,
            ),
            "level": self.text(
                f"LEVEL: {1}",
                constants.WINDOW_WIDTH - 95,
                constants.WINDOW_HEIGHT - 25,
                14,
                constants.LIGHT_GREY,
            ),
            "lives": self.text(
                f"LIVES: {self.game.lives}",
                constants.WINDOW_WIDTH - 95,
                25,
                14,
                constants.LIGHT_GREY,
            ),
        }

        self.paused: bool = False
        self.pause_title: pyglet.image.AbstractImage = self.image(
            "title_paused"
        )
        pause_hints = [
            "Esc to resume",
            "Q for main menu",
            "Arrows, WASD or HJKL to move",
            "I for invincibility, N to skip level, E for extra life",
        ]
        self.pause_hints: list[pyglet.text.Label] = [
            self.text(
                pause_hint,
                500,
                constants.WINDOW_HEIGHT // 2 - (80 + 34 * i),
                16,
                color=constants.GREY,
            )
            for i, pause_hint in enumerate(pause_hints)
        ]
        self.pause_shade: pyglet.image.ImageData = pyglet.image.ImageData(
            constants.WINDOW_WIDTH,
            constants.WINDOW_HEIGHT,
            "RGBA",
            bytes(
                bytes(constants.BLACK)
                * constants.WINDOW_WIDTH
                * constants.WINDOW_HEIGHT
            ),
        )

    def _make_maze_image(self) -> None:
        self.maze: pyglet.image.ImageData = pyglet.image.ImageData(
            self.image_width,
            self.image_height,
            "RGBA",
            b"".join(b"".join(line) for line in self.pixels),
            pitch=-self.image_width * 4,
        )

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

        self.pacgums_position: set[tuple[int, int]] = set(self.game.pacgums)
        for col, row in self.pacgums_position:
            x = col * self.tile + 8
            y = row * self.tile + 8
            self._paint_rectangle(x, y, 4, 4, constants.PINK)

        self._make_maze_image()

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

    def _erase_eaten_gums(self) -> None:
        eaten_gums = self.pacgums_position - self.game.pacgums
        for col, row in eaten_gums:
            x = col * self.tile + 8
            y = row * self.tile + 8
            self._paint_rectangle(x, y, 4, 4, constants.BLACK)
        if eaten_gums:
            self._make_maze_image()
        self.pacgums_position = set(self.game.pacgums)

    def _draw_supergums(self) -> None:
        for pos in self.game.sup_gums:
            x, y = self._get_center_tile(*pos)
            self.supergum.blit(x + 4, y + 4)

    def _draw_ghosts(self) -> None:
        for ghost, image in zip(self.game.ghosts, self.ghosts):
            x, y = self._get_center_tile(*ghost.visual_position())
            if ghost.mode is GhostMode.FRIGHTENED:
                self.scared_ghost.blit(x, y)
            elif ghost.mode is GhostMode.EATEN:
                self.eaten_ghost.blit(x, y)
            else:
                image.blit(x, y)

    def _update_info(self) -> None:
        self.infos["score"].text = f"SCORE: {self.game.score}"
        self.infos[
            "time"
        ].text = (
            f"TIME: {time.strftime('%M:%S', time.gmtime(self.game.time_left))}"
        )
        self.infos["level"].text = f"LEVEL: {self.game.level}"
        self.infos["lives"].text = f"LIVES: {self.game.lives}"

    def _get_center_tile(self, col: float, row: float) -> tuple[int, int]:
        x = self.maze_start_x + col * self.tile
        y = self.maze_start_y + self.image_height - (row + 1) * self.tile
        return int(x), int(y)

    def update(self, dt: float) -> View | None:
        if self.paused:
            return None
        self.game.update(dt)

        if self.game.state in (State.VICTORY, State.GAME_OVER):
            return ResultsView(
                self.menu_view,
                self.settings["highscore_filename"],
                self.game.state is State.VICTORY,
                self.game.score,
            )

        if self.board is not self.game.board:
            self._build_maze()
        self._erase_eaten_gums()

        self.pacman.update(dt)
        self.pacman.x, self.pacman.y = self._get_center_tile(
            *self.game.player.visual_position()
        )
        self.pacman.face(self.game.player.direction)

        self._update_info()

        return None

    def draw(self) -> None:
        self.maze.blit(self.maze_start_x, self.maze_start_y)
        self._draw_supergums()
        self.pacman.draw()
        self._draw_ghosts()

        for info in self.infos.values():
            info.draw()
        if self.game.invicible:
            self.invicible_text.draw()

        if self.paused:
            self.pause_shade.blit(0, 0)
            self.pause_title.blit(0, 555)
            for hint in self.pause_hints:
                hint.draw()

    def key_handler(self, symbol: int) -> View | None:
        if symbol == key.ESCAPE:
            self.paused = not self.paused
        if symbol == key.Q and self.paused:
            return self.menu_view
        if self.paused:
            return None

        if symbol in (key.UP, key.W, key.K):
            self.game.player.dir_wanted = Direction.UP
        if symbol in (key.DOWN, key.S, key.J):
            self.game.player.dir_wanted = Direction.DOWN
        if symbol in (key.LEFT, key.A, key.H):
            self.game.player.dir_wanted = Direction.LEFT
        if symbol in (key.RIGHT, key.D, key.L):
            self.game.player.dir_wanted = Direction.RIGHT

        if symbol == key.I:
            self.game.invicible = not self.game.invicible
        if symbol == key.N:
            self.game.sup_gums.clear()
            self.game.pacgums.clear()
        if symbol == key.E:
            self.game.lives += 1

        return None
