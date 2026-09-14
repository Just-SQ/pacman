from utils.entity import Direction, Entity
from .maze import Board


class Player(Entity):
    def __init__(
        self, spawn: tuple[int, int], speed: float, board: Board
    ) -> None:
        super().__init__(spawn, speed, board)
        self.dir_wanted: Direction = Direction.NONE  # last key pressed

    def _choose_direction(self) -> None:
        if self._can_move(self.dir_wanted):
            self.direction = self.dir_wanted
        elif not self._can_move(self.direction):
            self.direction = Direction.NONE
