import pyglet
from pyglet.window import key

from src import constants
from src.views.view import View


class InstructionsView(View):
    LINES: tuple[str, ...] = (
        "Move: arrow keys, WASD or HJKL",
        "Pause: Esc to resume, Q for the main menu",
        "Eat every pacgum to clear the level",
        "Touching a ghost costs one life",
        "A super-pacgum makes the ghosts edible for a while",
        "Clear 10 levels to win, before the time runs out",
        "Cheats: I = invincible, N = next level, E = extra life",
    )

    def __init__(self, menu_view: View) -> None:
        self.menu_view: View = menu_view
        self.background: pyglet.image.AbstractImage = self.image("menu_bg")
        self.title: pyglet.image.AbstractImage = self.image(
            "title_instructions"
        )
        self.lines: list[pyglet.text.Label] = [
            self.text(line, 380, 680 - i * 60, 30)
            for i, line in enumerate(self.LINES)
        ]
        self.lines.append(
            self.text("Esc to go back", 650, 80, 20, color=constants.GREY)
        )

    def draw(self) -> None:
        self.background.blit(0, 0)
        self.title.blit(0, 800)
        for line in self.lines:
            line.draw()

    def key_handler(self, symbol: int) -> View | None:
        if symbol == key.ESCAPE:
            return self.menu_view
        return None
