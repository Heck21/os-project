from pathlib import Path

import parser


def prompt():
    full_path = Path.cwd().parts

    if len(full_path) == 1:
        return f"{full_path[0]}"
    else:
        return f"{full_path[0]}../{full_path[-1]}"


def main() -> None:
    while True:
        command = input(f"{prompt()} > ")

        parser.parse(command.strip())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
