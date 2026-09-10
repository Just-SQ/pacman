from typing import Any
import json


class Parser:
    DEFAULT_CONFIG: dict[str, Any] = {
  "highscore_filename": "top_scores.txt",
  "level": (20, 20),
  "lives": 3,
  "points_per_pacgum": 5,
  "points_per_super_pacgum": 100,
  "points_per_ghost": 500
}
    BOUNDS: dict[str, tuple[int, int]] = {
    "lives": (1, 99),
    "points_per_pacgum": (1, 100000),
    "points_per_super_pacgum": (1, 100000),
    "points_per_ghost": (1, 100000),
    "level": (10, 50) 
}

    def __init__(self, path: str) -> None:
        self.path: str = path

    def parse(self) -> dict[str, Any]:
        string: str = ''
        with open(self.path) as f:
            for line in f:
                if not line.strip().startswith('#'):
                    string += line
                else:
                    string += '\n'
        loaded_str: Any = json.loads(string)
        return self._validate(loaded_str)

    def _validate(self, loaded_str: Any) -> dict[str, Any]:
        result: Any = loaded_str
        int_keys: set[str] = {
            "lives",
            "points_per_pacgum",
            "points_per_super_pacgum",
            "points_per_ghost"
        }
        if not isinstance(result, dict):
            raise ValueError("top level must be a JSON object")
        unknown: set[Any] = set(result) - set(self.DEFAULT_CONFIG)
        for key in unknown:
            print(f"Warning: unknown key '{key}' ignored")
        for key in self.DEFAULT_CONFIG:
            if key not in result:
                result[key] = self.DEFAULT_CONFIG[key]
                print(f"Warning: '{key}' is missing, using {result[key]}")
            elif key in int_keys:
                self._validate_int_keys(result, key)
            elif key == "level":
                self._validate_level(result, key)
            elif key == "highscore_filename":
                if not isinstance(result[key], str):
                    result[key] = self.DEFAULT_CONFIG[key]
                    print(f"Warning: '{key}' must be text, using 'top_scores.txt'")
        return result

    def _validate_int_keys(self, result, key) -> None:
        low, high = self.BOUNDS[key]
        try:
            if isinstance(result[key], bool):
                raise ValueError()
            result[key] = int(result[key])
            if result[key] < low or result[key] > high:
                raise ValueError()
        except (ValueError, TypeError):
            result[key] = self.DEFAULT_CONFIG[key]
            print(f"Warning: {key} must be an integer between {low} and {high}, using {result[key]}")

    def _validate_level(self, result, key) -> None:
        low, high = self.BOUNDS[key]
        try:
            if len(result[key]) != 2:
                raise ValueError()
            result[key][0] = int(result[key][0])
            result[key][1] = int(result[key][1])
            if not self._level_inbound(result, key, low, high):
                raise ValueError()
        except Exception:
            result[key] = self.DEFAULT_CONFIG[key]
            print(f"Warning: {key} must be [width, height] each one between {low} and {high}, using {result[key]}")

    def _level_inbound(self, result, key, low, high) -> bool:
        return low <= result[key][0] <= high and low <= result[key][1] <= high
