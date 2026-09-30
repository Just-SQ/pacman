from abc import ABC, abstractmethod
from enum import Enum

from src.maze import Board


class Direction(Enum):
    NONE = (0, 0)
    UP = (0, -1)
    DOWN = (0, 1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)


class Entity(ABC):
    MOVES: tuple[Direction, Direction, Direction, Direction] = (
        Direction.UP,
        Direction.DOWN,
        Direction.LEFT,
        Direction.RIGHT,
    )

    OPPOSITE: dict[Direction, Direction] = {
        Direction.NONE: Direction.NONE,
        Direction.UP: Direction.DOWN,
        Direction.DOWN: Direction.UP,
        Direction.LEFT: Direction.RIGHT,
        Direction.RIGHT: Direction.LEFT,
    }

    def __init__(
        self, spawn: tuple[int, int], speed: float, board: Board
    ) -> None:
        self.spawn: tuple[int, int] = spawn
        self.x: int = self.spawn[0]
        self.y: int = self.spawn[1]
        self.speed: float = speed  # speed=1 -> "crosses 1 tiles per second"
        self.direction: Direction = Direction.NONE
        self.progress: float = 0.0
        self.board: Board = board

    @abstractmethod
    def _choose_direction(self) -> None:
        pass

    @property
    def next_tile(self) -> tuple[int, int]:
        dx, dy = self.direction.value
        return (self.x + dx, self.y + dy)

    def reset(self) -> None:
        self.x, self.y = self.spawn
        self.direction = Direction.NONE
        self.progress = 0.0

    def update(self, fps: int = 60) -> None:
        if self.direction == Direction.NONE:
            self._choose_direction()
            if self.direction == Direction.NONE:
                return
        self.progress += self.speed / fps  # maybe xdt later
        if self.progress >= 1.00:
            self.progress -= 1.00
            self.x, self.y = self.next_tile
            self._choose_direction()

    def visual_position(self) -> tuple[float, float]:
        dx, dy = self.direction.value
        return (self.x + dx * self.progress, self.y + dy * self.progress)

    def _can_move(self, direction: Direction) -> bool:
        if direction == Direction.NONE:
            return False
        dx, dy = direction.value
        return self.board.is_walkable((self.x + dx, self.y + dy))
