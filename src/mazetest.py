from mazegenerator import MazeGenerator


class MazeRenderer:
    """
    Renders a maze to the terminal using Unicode block characters.

    Supports optional colorization of the solution path, entry, and exit
    points using ANSI escape codes.

    Args:
        maze: A MazeGenerator instance with a generated grid.
    """

    _COLORS = {
        "entry": "\033[94m",
        "exit": "\033[95m",
        "path": "\033[92m",
        "reset": "\033[0m",
    }

    def __init__(self, maze: MazeGenerator) -> None:
        self.maze: MazeGenerator = maze

    def render(
        self,
        colors: str = "\033[37m",
        solution_path: list[tuple[int, int]] | None = None,
    ) -> None:
        """
        Prints the maze to the terminal.

        Draws each cell row by row using block characters. Walls are drawn
        as filled blocks, passages as spaces. Entry, exit, and solution path
        cells are highlighted in distinct colors.

        Args:
            colors: ANSI color code applied to walls. Defaults to white.
            solution_path: Optional list of (x, y) coordinates to highlight
                as the solution. If None, no path is drawn.
        """

        solution_coordinates: set[tuple[int, int]] = set(solution_path or [])
        PATH_COLOR: str = self._COLORS["path"]
        RESET: str = self._COLORS["reset"]
        WALL: str = f"{colors}██"

        for y in range(self.maze._height):
            top_line: str = ""
            mid_line: str = ""

            for x in range(self.maze._width):
                cell = self.maze.maze[y][x]
                in_solution = (x, y) in solution_coordinates

                if cell & 0b0001:
                    top_line += WALL * 2
                else:
                    if in_solution and (x, y - 1) in solution_coordinates:
                        top_line += f"{WALL}{PATH_COLOR}██{RESET}"
                    else:
                        top_line += f"{WALL}  "

                if cell & 0b1000:
                    mid_line += f"{WALL}"
                else:
                    if in_solution and (x - 1, y) in solution_coordinates:
                        mid_line += f"{PATH_COLOR}██{RESET}"
                    else:
                        mid_line += "  "

                if cell == 0xF:
                    mid_line += "░░"
                elif (x, y) == (self.maze._entryx, self.maze._entryy):
                    mid_line += f"{self._COLORS['entry']}██{RESET}"
                elif (x, y) == (self.maze._exitx, self.maze._exity):
                    mid_line += f"{self._COLORS['exit']}██{RESET}"
                elif in_solution:
                    mid_line += f"{PATH_COLOR}██{RESET}"
                else:
                    mid_line += "  "

            top_line += f"{WALL}"
            mid_line += f"{WALL}"

            print(top_line)
            print(mid_line)

        print("██" * (self.maze._width * 2 + 1))
        print(f"{RESET}")


# Create a simple 20x20 maze
maze_gen = MazeGenerator((60, 70))
rendrer = MazeRenderer(maze_gen)

# Get the maze structure
maze_grid = maze_gen.maze
shortest_path = maze_gen.shortest_path

print(f"Maze dimensions: {len(maze_grid[0])}x{len(maze_grid)}")
print(f"Entry: {maze_gen.maze_entry}, Exit: {maze_gen.maze_exit}")
rendrer.render()
from json import load

with open("src/config.json") as f:
    conf = f.read()
print(conf)
