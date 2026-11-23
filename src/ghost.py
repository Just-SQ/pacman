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
        GhostMode.FRIGHTENED: 0.7,
        GhostMode.EATEN: 2,
    }

    def __init__(
        self, spawn: tuple[int, int], speed: float, board: Board, g_id: int
    ) -> None:
        super().__init__(spawn, speed, board)
        self.base_speed: float = speed
        self.mode: GhostMode = GhostMode.CHASE
        self.set_mode(GhostMode.CHASE)
        self.respawn_timer: float = 0.0
        self.target: tuple[int, int] = spawn
        self.g_id: int = g_id
        self.spawn_map: dict[tuple[int, int], int] = self._distance_from(spawn)
        self.current_target: tuple[int, int] | None = None
        self.RADIOUS: int = 7

    def set_mode(self, mode: GhostMode) -> None:
        if self.mode is GhostMode.CHASE and mode is GhostMode.FRIGHTENED:
            self._reverse()
        self.mode = mode
        self.speed = self.base_speed * self.SPEED_MOVE.get(mode, 0)
        if mode is GhostMode.EATEN:
            self.respawn_timer = self.RESPAWN_DELAY

    def set_target(self, player: Player) -> None:
        px, py = player.x, player.y
        match self.g_id:
            case 0:
                self.target = (px, py)
            case 1:
                self.target = (
                    (px + 2, py)
                    if self.board.is_walkable((px + 2, py))
                    else (px, py)
                )
            case 2:
                self.target = (
                    (px, py + 2)
                    if self.board.is_walkable((px, py + 2))
                    else (px, py)
                )
            case 3:
                self.target = (
                    (px - 4, py - 4)
                    if self.board.is_walkable((px - 4, py - 4))
                    else (px, py)
                )
        if self.mode is GhostMode.FRIGHTENED:
            self.target = (px, py)
        if self.current_target != self.target:
            self.player_map: dict[tuple[int, int], int] = self._distance_from(
                self.target
            )
            self.current_target = self.target

    def reset(self) -> None:
        super().reset()
        self.set_mode(GhostMode.CHASE)

    def update(self, dt: float) -> None:
        if self.mode is GhostMode.EATEN:
            self.respawn_timer -= dt
            if self.respawn_timer <= 0:
                self.reset()
        super().update(dt)

    def _choose_direction(self) -> None:
        near: bool = (
            self.mode is GhostMode.FRIGHTENED
            and self.player_map[(self.x, self.y)] <= self.RADIOUS
        )
        options: list[Direction] = [
            d
            for d in self.MOVES
            if self._can_move(d)
            and (near or d is not self.OPPOSITE[self.direction])
        ]
        if not options:  # dead end must turn back
            options = [d for d in self.MOVES if self._can_move(d)]
        if self.mode is GhostMode.FRIGHTENED:
            self.direction = max(options, key=self._distance)
            if self.next_tile == self.target:
                self._reverse()
        elif self.mode is GhostMode.EATEN:
            if (self.x, self.y) == self.spawn:
                self.direction = Direction.NONE
            else:
                self.direction = min(options, key=self._distance)
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
        if self.mode is GhostMode.EATEN:
            return self.spawn_map[(self.x + dx, self.y + dy)]
        return self.player_map[(self.x + dx, self.y + dy)]

    def _distance_from(
        self, start: tuple[int, int]
    ) -> dict[tuple[int, int], int]:
        dist: dict[tuple[int, int], int] = {start: 0}
        q: list[tuple[int, int]] = [start]

        while q:
            current: tuple[int, int] = q.pop(0)
            for neighbor in self._neighbors(current):
                if neighbor not in dist:
                    dist[neighbor] = dist[current] + 1
                    q.append(neighbor)

        return dist

    def _neighbors(self, current: tuple[int, int]) -> list[tuple[int, int]]:
        neighbors: list[tuple[int, int]] = []
        x, y = current
        for direction in self.MOVES:
            dx, dy = direction.value
            nx, ny = x + dx, y + dy
            if self.board.is_walkable((nx, ny)):
                neighbors.append((nx, ny))
        return neighbors
