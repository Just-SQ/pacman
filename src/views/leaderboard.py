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
        self.rows: list[pyglet.text.Label] = [
            self.make_label(
                f"{i + 1}. {name} {score}",
                size=18,
                y=constants.WINDOW_HEIGHT - 364 - i * 56,
            )
            for i, (name, score) in enumerate(scores)
        ]

    @staticmethod
    def load_scores() -> list[tuple[str, int]]:
        try:
            with open("leaderboard.json", "r") as f:
                highscores: list[dict[Any, Any]] = json.load(f)
        except OSError:
            return []
        except json.JSONDecodeError:
            print("[Warning]: leaderboard.json is not a valid json, ignored")
            return []
        if not isinstance(highscores, list):
            print("[Warning]: leaderboard.json must be a list, ignored")
            return []

        valid_scores: list[tuple[str, int]] = []
        valid_scores_counts: int = min(10, len(highscores))
        print(valid_scores_counts, len(highscores))
        idx = 0
        while idx < valid_scores_counts and idx < len(highscores):
            name, score = next(iter(highscores[idx].items()))
            if isinstance(name, str) and isinstance(score, int):
                valid_scores.append((name, score))
            else:
                valid_scores_counts += 1
            idx += 1
        print(valid_scores_counts)

        return sorted(valid_scores, key=lambda item: item[1], reverse=True)

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
