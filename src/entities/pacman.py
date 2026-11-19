import pyglet

from src.utils.entity import Direction


class Pacman:
    CHOMP: tuple[int, ...] = (0, 1, 2, 3, 2, 1)

    def __init__(self) -> None:
        self.dir_name: dict[Direction, str] = {
            Direction.DOWN: "down",
            Direction.LEFT: "left",
            Direction.RIGHT: "right",
            Direction.UP: "up",
        }

        self.images: dict[Direction, list[pyglet.image.AbstractImage]] = {}
        for dir, name in self.dir_name.items():
            self.images[dir] = [
                pyglet.image.load(f"assets/images/pacman_{name}_{i}.png")
                for i in range(4)
            ]

        self.x: int = 0
        self.y: int = 0
        self.dir: Direction = Direction.RIGHT

        self.chomp_step: int = 0
        self.chomp_timer: float = 0.0

    def draw(self) -> None:
        self.images[self.dir][self.CHOMP[self.chomp_step]].blit(self.x, self.y)

    def update(self, dt: float) -> None:
        self.chomp_timer += dt
        if self.chomp_timer >= 0.1:
            self.chomp_timer = 0
            self.chomp_step = (self.chomp_step + 1) % len(self.CHOMP)

    def face(self, direction: Direction) -> None:
        if direction is not Direction.NONE:
            self.dir = direction
