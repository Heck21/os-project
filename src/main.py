from pathlib import Path

from parser import parse


def prompt() -> str:
    """Generates shortened path to current directory that is shown at prompt."""

    full_path = Path.cwd().parts

    if len(full_path) == 1:
        return f"{full_path[0]}"
    else:
        return f"{full_path[0]}../{full_path[-1]}"


def main() -> None:
    while True:
        user_input = input(f"{prompt()} > ")

        parse(user_input.strip())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
