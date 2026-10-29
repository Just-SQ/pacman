from enum import Enum, auto

from .maze import Board
from .player import Player
from .utils.entity import Direction, Entity


class GhostMode(Enum):
    CHASE = auto()
    FRIGHTENED = auto()
    EATEN = auto()


class Ghost(Entity):
    RESPAWN_DELAY: float = 10.0
    SPEED_MOVE: dict[GhostMode, float] = {
        GhostMode.CHASE: 1,
        GhostMode.FRIGHTENED: 0.5,
    }

    def __init__(
        self, spawn: tuple[int, int], speed: float, board: Board, g_id: int
    ) -> None:
        super().__init__(spawn, speed, board)
        self.base_speed: float = speed
        self.mode: GhostMode = GhostMode.CHASE
        self.respawn_timer: float = 0.0
        self.target: tuple[int, int] = spawn
        self.g_id: int = g_id

    def set_mode(self, mode: GhostMode) -> None:
        if self.mode is GhostMode.CHASE and mode is GhostMode.FRIGHTENED:
            self._reverse()
        self.mode = mode
        self.speed = self.base_speed * self.SPEED_MOVE.get(mode, 0)
        if mode is GhostMode.EATEN:
            self.respawn_timer = self.RESPAWN_DELAY

    def set_target(self, player: Player) -> None:
        px, py = player.x, player.y
        if self.mode is GhostMode.FRIGHTENED:
            self.target = (px, py)
            return
        match self.g_id:
            case 0:
                self.target = (px, py)
            case 1:
                self.target = (px + 2, py + 2)
            case 2:
                self.target = (px + 4, py + 4)
            case 3:
                self.target = (px + 8, py + 8)

    def reset(self) -> None:
        super().reset()
        self.set_mode(GhostMode.CHASE)

    def update(self, fps: int = 60) -> None:
        if self.mode is GhostMode.EATEN:
            self.respawn_timer -= 1 / fps
            if self.respawn_timer <= 0:
                self.reset()
            return
        super().update(fps)

    def _choose_direction(self) -> None:
        options: list[Direction] = [
            d
            for d in self.MOVES
            if self._can_move(d) and d is not self.OPPOSITE[self.direction]
        ]
        if not options:  # dead end must turn back
            options = [d for d in self.MOVES if self._can_move(d)]
        if self.mode is GhostMode.FRIGHTENED:
            self.direction = max(options, key=self._distance)
            if self.next_tile == self.target:
                self._reverse()
        else:
            self.direction = min(options, key=self._distance)

    def _reverse(self) -> None:
        if self.direction is Direction.NONE:
            return
        self.x, self.y = self.next_tile
        self.direction = self.OPPOSITE[self.direction]
        self.progress = 1.0 - self.progress

    def _distance(self, direction: Direction) -> float:
        dx, dy = direction.value
        nx, ny = self.x + dx, self.y + dy
        tx, ty = self.target
        return (nx - tx) ** 2 + (ny - ty) ** 2
