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

        self.background: pyglet.image.AbstractImage = self.image("menu_bg")
        self.title: pyglet.image.AbstractImage = self.image(
            "title_leaderboard"
        )
        self.hint: pyglet.text.Label = self.text(
            "press esc to go back", 632, 90, 14, constants.GREY
        )

        self.header: pyglet.text.Label = self.text(
            f"{'#':<3} {'NAME':<10} {'SCORE':>8}",
            606,
            constants.WINDOW_HEIGHT - 300,
            18,
            (220, 220, 225, 255),
        )
        self.rule: pyglet.image.ImageData = pyglet.image.ImageData(
            236,
            4,
            "RGBA",
            bytes((220, 220, 225, 255)) * (236 * 4),
        )

        scores: list[tuple[str, int]] = self.load_scores()
        self.rows: list[pyglet.text.Label] = (
            [
                self.text(
                    f"{i + 1:<3} {name:<10} {score:>8}",
                    606,
                    constants.WINDOW_HEIGHT - 364 - i * 56,
                    18,
                    constants.LIGHT_GREY,
                )
                for i, (name, score) in enumerate(scores)
            ]
            if scores
            else [
                self.text(
                    "no scores yet",
                    651,
                    constants.WINDOW_HEIGHT // 2,
                    18,
                    constants.GREY,
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
        self.title.blit(0, 800)
        self.header.draw()
        self.rule.blit(
            x=606,
            y=int(self.header.y - 28),
        )
        for row in self.rows:
            row.draw()
        self.hint.draw()

    def key_handler(self, symbol: int) -> View | None:
        if symbol == key.ESCAPE:
            return self.prev_view
        return None
