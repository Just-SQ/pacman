import math

import pyglet

from src import constants


class Pacman(pyglet.sprite.Sprite):
    MOUTHS: tuple[int, ...] = (0, 30, 60, 90, 60, 30)

    def __init__(self, block: int = 3) -> None:
        self.frames: list[pyglet.image.ImageData] = [
            self._make_image(mouth, block) for mouth in self.MOUTHS
        ]
        super().__init__(self.frames[0], x=0, y=0)

        self.mouth_step: int = 0
        self.chomp_timer: float = 0.0

    def animate(self, dt: float) -> None:
        self.chomp_timer += dt
        if self.chomp_timer >= 0.1:
            self.chomp_timer = 0.0
            self.mouth_step = (self.mouth_step + 1) % len(self.frames)
            self.image: pyglet.image.ImageData = self.frames[self.mouth_step]

    def _make_image(self, mouth: float, block: int) -> pyglet.image.ImageData:
        size = 13 * block
        pixels = bytearray(size * size * 4)
        for py in range(size):
            for px in range(size):
                if self._is_yellow(px // block, py // block, mouth):
                    i = (py * size + px) * 4
                    pixels[i:(i + 4)] = bytes(constants.YELLOW)  # fmt: skip
        image = pyglet.image.ImageData(size, size, "RGBA", bytes(pixels))
        image.anchor_x = image.anchor_y = size // 2
        return image

    @staticmethod
    def _is_yellow(cx: int, cy: int, mouth: float) -> bool:
        dx, dy = cx - 6, cy - 6
        if math.hypot(dx, dy) > 6:
            return False
        return abs(math.degrees(math.atan2(dy, dx))) >= mouth / 2
