# Project Analysis and Choices

## 1. Split the Code into Two Layers

- **Problem:** two people building one game at the same time.
- **Choice:** split by layer. asaqi wrote the logic (`Game`, `Board`, `Player`, `Ghost`) with no pyglet. rkadri wrote everything that draws (`views/`).
- **Why:** we rarely edited the same file, and the logic can run without a window.

## 2. Turn Maze Cells into Tiles

- **Problem:** the maze package gives walls as thin lines between cells, but Pac-Man needs square walls we can draw and collide with.
- **Choice:** a grid of `(2 × width + 1) × (2 × height + 1)` tiles, where each tile is a wall or a corridor.
- **Why:** moving and colliding only means checking one tile.

## 3. Screens as Views

- **Problem:** the game has 6 screens (menu, game, results, leaderboard, instructions, credit).
- **Choice:** each screen is a `View` class. Its `update` and `key_handler` return the next view, or `None` to stay.
- **Why:** adding a screen means writing one new class, without touching the window code.
