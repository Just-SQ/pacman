import pyglet

from src import constants

from .views import View
from .views.menu import MenuView


class GameWindow(pyglet.window.Window):
    def __init__(self) -> None:
        super().__init__(
            constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT, caption="Pac-Man"
        )
        pyglet.font.add_file("assets/fonts/PressStart2P-Regular.ttf")
        self.current_view: View = MenuView()
        pyglet.clock.schedule_interval(self.update, 1 / constants.FPS)

    def update(self, dt: float) -> None:
        self.current_view.update(dt)

    def on_draw(self) -> None:
        self.clear()
        self.current_view.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        next_view = self.current_view.key_handler(symbol)
        if next_view is not None:
            self.current_view = next_view
