from mazegenerator import MazeGenerator


class Board:
    WALL: int = 0
    CORRIDOR: int = 1

    def __init__(self, maze_gen: MazeGenerator) -> None:
        self.maze: list[list[int]] = maze_gen.maze
        self.height: int = len(self.maze)
        self.width: int = len(self.maze[0])
        self.grid: list[list[int]] = self._create_grid()

    def _create_grid(self) -> list[list[int]]:
        grid: list[list[int]] = [
            [self.WALL for _ in range(2 * self.width + 1)]
            for _ in range(2 * self.height + 1)
        ]
        for y in range(self.height):
            for x in range(self.width):
                cell: int = self.maze[y][x]
                if cell == 15:
                    continue
                grid[2 * y + 1][2 * x + 1] = self.CORRIDOR
                if not cell & 2:  # no east wall
                    grid[2 * y + 1][2 * x + 2] = self.CORRIDOR
                if not cell & 4:  # no south wall
                    grid[2 * y + 2][2 * x + 1] = self.CORRIDOR
        return grid

    def is_walkable(self, square: tuple[int, int]) -> bool:
        x, y = square
        if not (0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid)):
            return False
        return self.grid[y][x] == self.CORRIDOR

    def supgums_spawn(self) -> set[tuple[int, int]]:
        return {
            (1, 1),
            (2 * self.width - 1, 2 * self.height - 1),
            (2 * self.width - 1, 1),
            (1, 2 * self.height - 1)
        }

    def pacman_spawn(self) -> tuple[int, int]:
        logo_w, logo_h = 7, 5
        x: int = (self.width - logo_w) // 2 + 3
        y: int = (self.height - logo_h) // 2 + 2
        return x * 2 + 1, y * 2 + 1

    def pacgums(self) -> set[tuple[int, int]]:
        pacgums: set[tuple[int, int]] = set()
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.is_walkable((x, y)):
                    pacgums.add((x, y))
        pacgums -= self.supgums_spawn()
        pacgums.discard(self.pacman_spawn())
        return pacgums
