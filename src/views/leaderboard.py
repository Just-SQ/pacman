import json
from typing import Any

import pyglet
from pyglet.window import key

from src import constants
from src.views import View


class LeaderboardView(View):
    def __init__(
        self,
        prev_view: View,
    ) -> None:
        self.prev_view: View = prev_view
        self.background: pyglet.sprite.Sprite = pyglet.sprite.Sprite(
            pyglet.image.load("assets/images/menu_bg.png"),
            x=0,
            y=0,
        )
        self.title: list[pyglet.text.Label] = self.make_title(
            "Leaderboard", constants.WINDOW_HEIGHT - 200, 44
        )
        self.hint: pyglet.text.Label = self.make_label(
            "press esc to go back", size=14, y=90, color=constants.GREY
        )

        scores: list[tuple[str, int]] = self.load_scores()
        self.rows: list[pyglet.text.Label] = (
            [
                self.make_label(
                    f"{i + 1}. {name} {score}",
                    size=18,
                    y=constants.WINDOW_HEIGHT - 364 - i * 56,
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

    @staticmethod
    def load_scores() -> list[tuple[str, int]]:
        try:
            with open("leaderboard.json", "r") as f:
                scores: list[dict[Any, Any]] = json.load(f)
        except OSError:
            return []
        except json.JSONDecodeError:
            print("[Warning]: leaderboard.json is not a valid json, ignored")
            return []
        if not isinstance(scores, list):
            print("[Warning]: leaderboard.json must be a list, ignored")
            return []

        valid_scores: list[tuple[str, int]] = []
        for score in scores:
            if not isinstance(score, dict) or len(score) != 1:
                continue

            name, val = next(iter(score.items()))
            if type(val) is int and val > 0:
                valid_scores.append((name, val))

        valid_scores.sort(key=lambda item: item[1], reverse=True)
        return valid_scores[:10]

    def draw(self) -> None:
        self.background.draw()
        for line in self.title:
            line.draw()
        for row in self.rows:
            row.draw()
        self.hint.draw()

    def key_handler(self, symbol: int) -> View | None:
        if symbol == key.ESCAPE:
            return self.prev_view
        return None
