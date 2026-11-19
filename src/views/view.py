import pyglet

from src import constants, types


class View:
    def draw(self) -> None: ...

    def update(self, dt: float) -> View | None: ...

    def key_handler(self, symbol: int) -> View | None:
        return None

    @staticmethod
    def image(name: str) -> pyglet.image.AbstractImage:
        return pyglet.image.load(f"assets/images/{name}.png")

    @staticmethod
    def text(
        string: str,
        x: int,
        y: int,
        size: int = 28,
        color: types.Color = constants.WHITE,
    ) -> pyglet.text.Label:
        return pyglet.text.Label(string, x=x, y=y, font_size=size, color=color)
