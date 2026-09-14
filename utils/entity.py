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
    def __init__(
        self, spawn: tuple[int, int], speed: float, board: Board
    ) -> None:
        self.x, self.y = spawn
        self.speed: float = speed  # speed=1 -> "crosses 1 tiles per second"
        self.direction = Direction.NONE
        self.progress: float = 0.0
        self.board: Board = board

    @abstractmethod
    def _choose_direction(self) -> None:
        pass

    @property
    def next_tile(self) -> tuple[int, int]:
        dx, dy = self.direction.value
        return (self.x + dx, self.y + dy)

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
