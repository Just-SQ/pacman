import json

import pyglet
from pyglet.window import key

from src import constants
from src.views import View


class ResultsView(View):
    def __init__(
        self,
        menu_view: View,
        highscore_filename: str,
        victory: bool,
        score: int,
    ) -> None:
        self.menu_view: View = menu_view
        self.highscore_filename: str = highscore_filename
        self.score: int = score
        self.name: str = ""

        self.background: pyglet.sprite.Sprite = pyglet.sprite.Sprite(
            pyglet.image.load("assets/images/menu_bg.png"),
            x=0,
            y=0,
        )
        self.title: list[pyglet.text.Label] = self.make_title(
            "YOU WIN!" if victory else "GAME OVER",
            constants.WINDOW_HEIGHT - 260,
            64,
        )
        self.score_label: pyglet.text.Label = self.make_label(
            f"SCORE {score}", 24, 640, color=constants.YELLOW
        )
        self.prompt: pyglet.text.Label = self.make_label(
            "ENTER YOUR NAME", 18, 520, color=constants.GREY
        )
        self.name_label: pyglet.text.Label = self.make_label(
            f"{self.name:_<10}", 36, 440
        )
        self.hint: pyglet.text.Label = self.make_label(
            "press enter to save", 14, 90, color=constants.GREY
        )

    def dump_score(self) -> None:
        scores: list[dict[str, int]] = []
        try:
            with open(self.highscore_filename, "r") as f:
                scores = json.load(f)
        except OSError:
            pass
        except json.JSONDecodeError:
            print(
                f"[Warning]: {self.highscore_filename} is"
                + "not a valid json, ignored"
            )
        if not isinstance(scores, list):
            print(
                f"[Warning]: {self.highscore_filename} must be a list, ignored"
            )
            scores = []

        valid_scores: list[dict[str, int]] = []
        score_updated: bool = False
        for score in scores:
            if isinstance(score, dict) and len(score) == 1:
                name, val = next(iter(score.items()))
                if type(val) is int and val >= 0:
                    if name == self.name.strip():
                        score_updated = True
                        val = max(val, self.score)
                    valid_scores.append({name: val})
        if not score_updated:
            valid_scores.append({self.name.strip(): self.score})

        try:
            with open(self.highscore_filename, "w") as f:
                json.dump(valid_scores, f, indent=4)
        except OSError:
            print(f"[Warning]: could not save {self.highscore_filename}")

    def draw(self) -> None:
        self.background.draw()
        for layer in self.title:
            layer.draw()
        self.score_label.draw()
        self.prompt.draw()
        self.name_label.draw()
        self.hint.draw()

    def key_handler(self, symbol: int) -> View | None:
        if symbol == key.RETURN and self.name.strip():
            self.dump_score()
            return self.menu_view
        if len(self.name) < 10 and (
            (key.A <= symbol <= key.Z)
            or (key._0 <= symbol <= key._9)
            or symbol == key.SPACE
        ):
            self.name += chr(symbol).upper()
        if symbol == key.BACKSPACE:
            self.name = self.name[:-1]
        self.name_label.text = f"{self.name:_<10}"
        return None
