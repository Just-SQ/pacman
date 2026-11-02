import json
from typing import Any


class Parser:
    DEFAULT_CONFIG: dict[str, Any] = {
        "highscore_filename": "top_scores.txt",
        "level": (10, 10),
        "lives": 10,
        "points_per_pacgum": 10,
        "points_per_super_pacgum": 50,
        "points_per_ghost": 200,
    }
    BOUNDS: dict[str, tuple[int, int]] = {
        "lives": (1, 99),
        "points_per_pacgum": (1, 100000),
        "points_per_super_pacgum": (1, 100000),
        "points_per_ghost": (1, 100000),
        "level": (5, 25),
    }

    def __init__(self, path: str) -> None:
        self.path: str = path

    def parse(self) -> dict[str, Any]:
        string: str = ""
        with open(self.path) as f:
            for line in f:
                if not line.strip().startswith("#"):
                    string += line
                else:
                    string += "\n"
        loaded_str: Any = json.loads(string)
        return self._validate(loaded_str)

    def _validate(self, loaded_str: Any) -> dict[str, Any]:
        result: Any = loaded_str
        if not isinstance(result, dict):
            raise ValueError("top level must be a JSON object")
        unknown: set[Any] = set(result) - set(self.DEFAULT_CONFIG)
        for key in unknown:
            print(f"Warning: unknown key '{key}' ignored")
        for key in self.DEFAULT_CONFIG:
            if key not in result:
                result[key] = self.DEFAULT_CONFIG[key]
                print(f"Warning: '{key}' is missing, using {result[key]}")
            elif key == "level":
                self._validate_level(result, key)
            elif key in self.BOUNDS:
                self._validate_int_keys(result, key)
            elif key == "highscore_filename":
                if not isinstance(result[key], str):
                    result[key] = self.DEFAULT_CONFIG[key]
                    print(
                        f"Warning: '{key}' must be text, "
                        "using 'top_scores.txt'"
                    )
        return result

    def _validate_int_keys(self, result: dict[str, Any], key: str) -> None:
        low, high = self.BOUNDS[key]
        try:
            if isinstance(result[key], bool):
                raise ValueError()
            result[key] = int(result[key])
            if result[key] < low or result[key] > high:
                raise ValueError()
        except ValueError, TypeError:
            result[key] = self.DEFAULT_CONFIG[key]
            print(
                f"Warning: {key} must be an integer "
                f"between {low} and {high}, using {result[key]}"
            )

    def _validate_level(self, result: dict[str, Any], key: str) -> None:
        low, high = self.BOUNDS[key]
        try:
            if len(result[key]) != 2:
                raise ValueError()
            result[key][0] = int(result[key][0])
            result[key][1] = int(result[key][1])
            if not self._level_inbound(result, key, low, high):
                raise ValueError()
            result[key] = tuple(result[key])
        except Exception:
            result[key] = self.DEFAULT_CONFIG[key]
            print(
                f"Warning: {key} must be [width, height] "
                f"each one between {low} and {high}, using {result[key]}"
            )

    def _level_inbound(
        self, result: dict[str, Any], key: str, low: int, high: int
    ) -> Any:
        return low <= result[key][0] <= high and low <= result[key][1] <= high
