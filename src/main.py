import parser


def main() -> None:
    while True:
        command = input("> ")

        parser.parse(command.lower().strip())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
