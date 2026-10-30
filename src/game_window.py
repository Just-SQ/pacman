from typing import Any

import pyglet
from pyglet.gl import GL_NEAREST, glViewport

from src import constants

from .views import View
from .views.menu import MenuView

pyglet.image.Texture.default_min_filter = GL_NEAREST
pyglet.image.Texture.default_mag_filter = GL_NEAREST


class GameWindow(pyglet.window.Window):
    def __init__(self, settings: dict[str, Any]) -> None:
        super().__init__(fullscreen=True, caption="Pac-Man")
        pyglet.font.add_file("assets/fonts/PressStart2P-Regular.ttf")
        pyglet.clock.schedule_interval(self.update, 1 / constants.FPS)

        self.margin_x: int = (self.width - constants.WINDOW_WIDTH) // 2
        self.margin_y: int = (self.height - constants.WINDOW_HEIGHT) // 2

        self.current_view: View = MenuView(settings)
        self.settings: dict[str, Any] = settings

    def update(self, dt: float) -> None:
        next_view = self.current_view.update(dt)
        if next_view is not None:
            self.current_view = next_view

    def on_draw(self) -> None:
        self.clear()
        glViewport(
            self.margin_x,
            self.margin_y,
            self.width,
            self.height,
        )
        self.current_view.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        next_view = self.current_view.key_handler(symbol)
        if next_view is not None:
            self.current_view = next_view
