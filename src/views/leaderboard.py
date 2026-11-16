import json
from typing import Any

import pyglet
from pyglet.window import key

from src import constants
from src.views import View


class LeaderboardView(View):
    def __init__(self, prev_view: View, highscore_filename: str) -> None:
        self.prev_view: View = prev_view
        self.highscore_filename: str = highscore_filename

        self.background: pyglet.image.AbstractImage = pyglet.image.load(
            "assets/images/menu_bg.png"
        )
        self.title: list[pyglet.text.Label] = self.make_title(
            "Leaderboard", constants.WINDOW_HEIGHT - 200, 44
        )
        self.hint: pyglet.text.Label = self.make_label(
            "press esc to go back", size=14, y=90, color=constants.GREY
        )

        self.header: pyglet.text.Label = self.make_label(
            f"{'#':<3} {'NAME':<10} {'SCORE':>8}",
            size=18,
            y=constants.WINDOW_HEIGHT - 300,
            color=(220, 220, 225, 255),
        )
        self.rule: pyglet.image.ImageData = pyglet.image.ImageData(
            self.header.content_width,
            4,
            "RGBA",
            bytes((220, 220, 225, 255)) * (self.header.content_width * 4),
        )

        scores: list[tuple[str, int]] = self.load_scores()
        self.rows: list[pyglet.text.Label] = (
            [
                self.make_label(
                    f"{i + 1:<3} {name:<10} {score:>8}",
                    size=18,
                    y=constants.WINDOW_HEIGHT - 364 - i * 56,
                    color=constants.LIGHT_GREY,
                )
                for i, (name, score) in enumerate(scores)
            ]
            if scores
            else [
                self.make_label(
                    "no scores yet",
                    size=18,
                    y=constants.WINDOW_HEIGHT // 2,
                    color=constants.GREY,
                )
            ]
        )
        for i, color in enumerate(
            [constants.YELLOW, constants.SILVER, constants.BRONZE]
        ):
            if i < len(scores):
                self.rows[i].color = color

    def load_scores(self) -> list[tuple[str, int]]:
        try:
            with open(self.highscore_filename, "r") as f:
                scores: list[dict[Any, Any]] = json.load(f)
        except OSError:
            return []
        except json.JSONDecodeError:
            print(
                f"[Warning]: {self.highscore_filename} is not"
                + "a valid json, ignored"
            )
            return []
        if not isinstance(scores, list):
            print(
                f"[Warning]: {self.highscore_filename} must be a list, ignored"
            )
            return []

        valid_scores: list[tuple[str, int]] = []
        for score in scores:
            if not isinstance(score, dict) or len(score) != 1:
                continue

            name, val = next(iter(score.items()))
            if type(val) is int and val >= 0:
                valid_scores.append((name, val))

        valid_scores.sort(key=lambda item: item[1], reverse=True)
        return valid_scores[:10]

    def draw(self) -> None:
        self.background.blit(0, 0)
        for line in self.title:
            line.draw()
        self.header.draw()
        self.rule.blit(
            x=(constants.WINDOW_WIDTH - self.header.content_width) // 2,
            y=int(self.header.y - 28),
        )
        for row in self.rows:
            row.draw()
        self.hint.draw()

    def key_handler(self, symbol: int) -> View | None:
        if symbol == key.ESCAPE:
            return self.prev_view
        return None
