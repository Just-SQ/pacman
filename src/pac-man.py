from argparse import ArgumentParser
from json import JSONDecodeError
from parser import Parser


def main() -> None:
    arg_parse = ArgumentParser()
    arg_parse.add_argument("config_file")
    arg = arg_parse.parse_args()
    parser = Parser(arg.config_file)
    print(parser.parse())


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
