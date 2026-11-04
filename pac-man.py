import os
import sys
from argparse import ArgumentParser, Namespace
from json import JSONDecodeError

import pyglet

from src import GameWindow
from src.utils import Parser


def main() -> None:
    arg_parse: ArgumentParser = ArgumentParser()
    _ = arg_parse.add_argument("config_file")

    if getattr(sys, "frozen", False) and len(sys.argv) == 1:
        sys.argv.append(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "config.json"
            )
        )

    arg: Namespace = arg_parse.parse_args()

    parser: Parser = Parser(os.path.abspath(arg.config_file))

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
    except KeyboardInterrupt, EOFError:
        pass
    except Exception as e:
        print(f"[ERROR]: {e}")
        sys.exit(1)
