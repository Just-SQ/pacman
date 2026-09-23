from __future__ import annotations

import math

import pyglet
from pyglet.window import key

WINDOW_WIDTH = 1448
WINDOW_HEIGHT = 1028

YELLOW = (255, 255, 0, 255)
GOLD = (170, 128, 0, 255)
BROWN = (74, 52, 12, 255)


class View:
    def draw(self) -> None: ...

    def key_handler(self, symbol: int) -> View | None:
        return None

    @staticmethod
    def make_label(
        text: str,
        y: int,
        size: int,
        color: tuple[int, int, int, int] = (255, 255, 255, 255),
        x: int = WINDOW_WIDTH // 2,
        anchor_x: str = "center",
    ) -> pyglet.text.Label:
        return pyglet.text.Label(
            text,
            x=x,
            y=y,
            anchor_x=anchor_x,
            anchor_y="center",
            font_size=size,
            color=color,
            weight="normal",
            font_name="Press Start 2P",
        )

    @staticmethod
    def make_title(text: str, y: int, size: int) -> list[pyglet.text.Label]:
        layers = (
            (8, -8, BROWN),
            (4, -4, GOLD),
            (0, 0, YELLOW),
        )
        labels: list[pyglet.text.Label] = []
        for dx, dy, color in layers:
            label = View.make_label(text, y + dy, size, color)
            label.x += dx
            labels.append(label)
        return labels


class MenuView(View):
    OPTIONS: list[str] = [
        "Start game",
        "Leaderboard",
        "Credit",
    ]
    FIRST_OPTION_Y = 500
    ROW_HEIGHT = 64

    def __init__(self) -> None:
        self.title: list[pyglet.text.Label] = self.make_title(
            "Pac-Man", WINDOW_HEIGHT - 300, 60
        )
        self.background: pyglet.sprite.Sprite = pyglet.sprite.Sprite(
            pyglet.image.load("assets/images/menu_bg.png"),
            x=0,
            y=0,
        )
        self.options: list[pyglet.text.Label] = [
            self.make_label(
                text,
                self.option_y(i),
                24,
                x=WINDOW_WIDTH // 2 - 160,
                anchor_x="left",
            )
            for i, text in enumerate(self.OPTIONS)
        ]

        self.cursor: pyglet.sprite.Sprite = pyglet.sprite.Sprite(
            self._make_pacman(11, 4, 45),
            x=WINDOW_WIDTH // 2 - 240,
            y=0,
        )

        self.selected_view: int = 0
        self._refresh_menu()

    def option_y(self, index: int) -> int:
        return self.FIRST_OPTION_Y - index * self.ROW_HEIGHT

    def _refresh_menu(self) -> None:
        for i, option in enumerate(self.options):
            option.color = (
                (255, 255, 0, 255)
                if i == self.selected_view
                else (170, 170, 170, 255)
            )
        middle = self.option_y(self.selected_view)
        self.cursor.y = middle - self.cursor.height // 2

    def _make_pacman(
        self, cells: int, block: int, mouth: float
    ) -> pyglet.image.ImageData:
        size = cells * block
        centre = (cells - 1) / 2
        half = math.radians(mouth) / 2

        buf = bytearray(size * size * 4)
        row = bytes(YELLOW) * block

        for cy in range(cells):
            for cx in range(cells):
                dx, dy = cx - centre, cy - centre

                if math.hypot(dx, dy) > centre:
                    continue
                if abs(math.atan2(dy, dx)) < half:
                    continue

                for line in range(cy * block, (cy + 1) * block):
                    start = (line * size + cx * block) * 4
                    end = start + len(row)
                    buf[start:end] = row

        return pyglet.image.ImageData(size, size, "RGBA", bytes(buf))

    def draw(self) -> None:
        self.background.draw()
        for layer in self.title:
            layer.draw()
        for option in self.options:
            option.draw()
        self.cursor.draw()

    def key_handler(self, symbol: int) -> View | None:
        if symbol in (key.UP, key.W, key.K):
            self.selected_view = (self.selected_view - 1) % len(self.OPTIONS)
            self._refresh_menu()
        if symbol in (key.DOWN, key.S, key.J):
            self.selected_view = (self.selected_view + 1) % len(self.OPTIONS)
            self._refresh_menu()
        return None


class GameWindow(pyglet.window.Window):
    def __init__(self) -> None:
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, caption="Pac-Man")
        pyglet.font.add_file("assets/fonts/PressStart2P-Regular.ttf")
        self.current_view: View = MenuView()

    def on_draw(self) -> None:
        self.clear()
        self.current_view.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        _ = self.current_view.key_handler(symbol)
        if symbol == key.ESCAPE:
            self.close()


if __name__ == "__main__":
    _ = GameWindow()
    pyglet.app.run()
