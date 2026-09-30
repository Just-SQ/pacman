from enum import Enum, auto
from typing import Any

from mazegenerator import MazeGenerator

from .ghost import Ghost, GhostMode
from .maze import Board
from .player import Player


class State(Enum):
    RUNNING = auto()
    LEVEL_WON = auto()
    GAME_OVER = auto()
    VICTORY = auto()


class Game:
    POWER_DURATION: float = 10.0
    MAX_LEVEL: int = 10
    PLAYER_SPEED: float = 5.0
    GHOST_SPEED: float = 2.5  # level 1: half the player speed
    GHOST_UP: float = 0.27  # per level half the player / max_level + 10%
    TIME_PER_GUM: float = 0.30  # it's a guess maybe change later
    TIME_DECAY: float = 0.90  # time decrease by 10% in each level

    def __init__(self, config: dict[str, Any]) -> None:
        self.config: dict[str, Any] = config
        self.score: int = 0
        self.lives: int = self.config["lives"]
        self.level: int = 1
        self.state: State = State.RUNNING
        self.invicible: bool = False
        self.load_level()

    def load_level(self) -> None:
        seed: int = 42 if self.level == 1 else 0
        self.board: Board = Board(
            MazeGenerator(size=self.config["level"], seed=seed)
        )
        self.pacgums: set[tuple[int, int]] = self.board.pacgums()
        self.sup_gums: set[tuple[int, int]] = self.board.supgums_spawn()
        self.player_spawn: tuple[int, int] = self.board.pacman_spawn()
        self.player: Player = Player(
            spawn=self.player_spawn, speed=self.PLAYER_SPEED, board=self.board
        )
        ghost_sp: float = self.GHOST_SPEED + self.GHOST_UP * (self.level - 1)
        self.ghosts: list[Ghost] = [
            Ghost(spawn=corner, speed=ghost_sp, board=self.board, g_id=id)
            for id, corner in enumerate(self.sup_gums)
        ]
        self.time_left: float = (
            len(self.pacgums)
            * self.TIME_PER_GUM
            * self.TIME_DECAY ** (self.level - 1)
        )
        self.power_time: float = 0.0

    def update(self, fps: int) -> None:
        if self.state is not State.RUNNING:
            return

        step: float = 1 / fps
        self.time_left -= step
        if self.time_left <= 0:
            self.state = State.GAME_OVER
            return

        if self.power_time > 0:
            self.power_time -= step
            if self.power_time <= 0:
                self.power_time = 0.0
                for ghost in self.ghosts:
                    if ghost.mode is GhostMode.FRIGHTENED:
                        ghost.set_mode(GhostMode.CHASE)

        self.player.update(fps)
        for ghost in self.ghosts:
            ghost.set_target(self.player)
            ghost.update(fps)

        self._eat_gums()
        self._check_collisions()
        self._check_level_complete()

    def _eat_gums(self) -> None:
        block: tuple[int, int] = (self.player.x, self.player.y)
        if block in self.pacgums:
            self.pacgums.discard(block)
            self.score += self.config["points_per_pacgum"]
        elif block in self.sup_gums:
            self.sup_gums.discard(block)
            self.score += self.config["points_per_super_pacgum"]
            self.power_time = self.POWER_DURATION
            for ghost in self.ghosts:
                if ghost.mode is not GhostMode.EATEN:
                    ghost.set_mode(GhostMode.FRIGHTENED)

    def _check_collisions(self) -> None:
        px, py = self.player.visual_position()
        for ghost in self.ghosts:
            if ghost.mode is GhostMode.EATEN:
                continue
            gx, gy = ghost.visual_position()
            if abs(px - gx) >= 0.5 or abs(py - gy) >= 0.5:
                continue
            if ghost.mode is GhostMode.FRIGHTENED:
                self.score += self.config["points_per_ghost"]
                ghost.set_mode(GhostMode.EATEN)
            elif not self.invicible:
                self._lose_life()
                return

    def _lose_life(self) -> None:
        self.lives -= 1
        if self.lives <= 0:
            self.state = State.GAME_OVER
            return
        self.player.reset()
        for ghost in self.ghosts:
            ghost.reset()
        self.power_time = 0.0

    def _check_level_complete(self) -> None:
        if self.pacgums or self.sup_gums:
            return
        if self.level >= self.MAX_LEVEL:
            self.state = State.VICTORY
        else:
            self.level += 1
            # self.state = State.LEVEL_WON when ui is ready
            self.load_level()
