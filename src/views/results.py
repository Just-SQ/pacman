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

        self.background: pyglet.image.AbstractImage = self.image("menu_bg")
        self.title: pyglet.image.AbstractImage = self.image(
            "title_you_win" if victory else "title_game_over"
        )
        self.score_label: pyglet.text.Label = self.text(
            f"SCORE {score}", 624, 640, 24, constants.YELLOW
        )
        self.prompt: pyglet.text.Label = self.text(
            "ENTER YOUR NAME", 615, 520, 18, constants.GREY
        )
        self.name_label: pyglet.text.Label = self.text(
            f"{self.name:_<10}", 614, 440, 36
        )
        self.hint: pyglet.text.Label = self.text(
            "press enter to save", 637, 90, 14, constants.GREY
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
        self.background.blit(0, 0)
        self.title.blit(0, 720)
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
