from typing import Literal

import pyglet

from src import constants, types


class View:
    def draw(self) -> None: ...

    def update(self, dt: float) -> None: ...

    def key_handler(self, symbol: int) -> View | None:
        return None

    @staticmethod
    def make_label(
        text: str,
        size: int,
        y: int,
        x: int = constants.WINDOW_WIDTH // 2,
        color: types.Color = constants.WHITE,
        anchor_x: Literal["left", "center", "right"] = "center",
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
        depth = max(2, size // 8)
        layers = (
            (depth, -depth, constants.BROWN),
            (depth // 2, -depth // 2, constants.GOLD),
            (0, 0, constants.YELLOW),
        )
        labels: list[pyglet.text.Label] = []
        for dx, dy, color in layers:
            label = View.make_label(text, size, y + dy, color=color)
            label.x += dx
            labels.append(label)
        return labels
