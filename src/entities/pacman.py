import pyglet


class Pacman(pyglet.sprite.Sprite):
    CHOMP: tuple[int, ...] = (0, 1, 2, 3, 2, 1)

    def __init__(self, block: float = 3) -> None:
        self.frames: list[pyglet.image.AbstractImage] = []
        for number in range(4):
            image = pyglet.image.load(f"assets/images/pacman_{number}.png")
            image.anchor_x = image.width // 2
            image.anchor_y = image.height // 2
            self.frames.append(image)
        super().__init__(self.frames[0], x=0, y=0)
        self.scale = block

        self.chomp_step: int = 0
        self.chomp_timer: float = 0.0

    def animate(self, dt: float) -> None:
        self.chomp_timer += dt
        if self.chomp_timer >= 0.1:
            self.chomp_timer = 0.0
            self.chomp_step = (self.chomp_step + 1) % len(self.CHOMP)
            self.image = self.frames[self.CHOMP[self.chomp_step]]
