import pyglet
from pyglet.window import key

from src import constants
from src.views.view import View


class CreditView(View):
    def __init__(self, menu_view: View) -> None:
        self.menu_view: View = menu_view
        self.background: pyglet.image.AbstractImage = self.image("menu_bg")
        self.title: pyglet.image.AbstractImage = self.image("title_credit")
        self.lines: list[pyglet.text.Label] = [
            self.text("A 42 project", 613, 540, 30),
            self.text("Made by rkadri and asaqi", 489, 480, 30),
            self.text("Esc to go back", 650, 80, 20, color=constants.GREY),
        ]

    def draw(self) -> None:
        self.background.blit(0, 0)
        self.title.blit(0, 800)
        for line in self.lines:
            line.draw()

    def key_handler(self, symbol: int) -> View | None:
        if symbol == key.ESCAPE:
            return self.menu_view
        return None
