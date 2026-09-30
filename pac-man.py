from argparse import ArgumentParser, Namespace
from json import JSONDecodeError

import pyglet

from src import GameWindow
from src.utils import Parser


def main() -> None:
    arg_parse: ArgumentParser = ArgumentParser()
    arg_parse.add_argument("config_file")
    arg: Namespace = arg_parse.parse_args()
    parser: Parser = Parser(arg.config_file)

    _ = GameWindow(parser.parse())
    pyglet.app.run()


if __name__ == "__main__":
    try:
        main()
    except OSError as e:
        print(f"Could not read Config file: {e}")
    except JSONDecodeError as e:
        print(f"Invalid Json: {e.msg}")
        print(f"Line: {e.lineno}")
    except ValueError as e:
        print(e)
