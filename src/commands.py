import os
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

from utility import ShellError

ORIGINAL_VARS = {x for x in os.environ.keys()}


def cf(args: list[str]) -> None:
    try:
        if len(args) != 1:
            raise ShellError

        subprocess.run(["touch", *args], stderr=subprocess.DEVNULL, check=True)
    except subprocess.CalledProcessError:
        print("cf: Something went wrong")
    except ShellError:
        print("cf: Incorrect syntax. Type 'help' to see correct syntax")


def df(args: list[str]) -> None:
    try:
        if len(args) != 1:
            raise ShellError

        subprocess.run(["rm", "-f", *args], stderr=subprocess.DEVNULL, check=True)
    except subprocess.CalledProcessError:
        print("df: Cannot remove a directory")
    except ShellError:
        print("df: Incorrect syntax. Type 'help' to see correct syntax")


def rf(args: list[str]) -> None:
    try:
        if len(args) != 2:
            raise ShellError("Incorrect syntax. Type 'help' to see correct syntax")

        old, new = args

        old = Path(old).resolve(strict=True)
        new = Path(new).resolve()

        if old.is_dir():
            raise ShellError("Cannot apply command with directory")

        if old == new:
            raise ShellError(f"'{old.name}' and '{new.name}' are the same file")

        subprocess.run(["mv", "-T", old, new], stderr=subprocess.DEVNULL, check=True)
    except subprocess.CalledProcessError:
        print("rf: Cannot apply command with directory")
    except FileNotFoundError:
        print("rf: No such file")
    except ShellError as e:
        print(f"rf: {e}")


def md(args: list[str]) -> None:
    try:
        if len(args) != 1:
            raise ShellError("Incorrect syntax. Type 'help' to see correct syntax")

        new_directory = Path(*args).resolve()

        if new_directory.exists():
            raise ShellError("Directory already exists")

        subprocess.run(["mkdir", *args], stderr=subprocess.DEVNULL, check=True)
    except (subprocess.CalledProcessError, PermissionError):
        print("md: Permission denied")
    except ShellError as e:
        print(f"md: {e}")


def dd(args: list[str]) -> None:
    try:
        if len(args) != 1:
            raise ShellError("Incorrect syntax. Type 'help' to see correct syntax")

        directory = Path(*args).resolve(strict=True)

        if directory.is_file():
            raise ShellError("Cannot remove a file")

        if directory == Path("/"):
            raise PermissionError

        subprocess.run(["rm", "-rf", directory], stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("dd: No such directory")
    except PermissionError:
        print("dd: Permission denied")
    except ShellError as e:
        print(f"dd: {e}")


def cd(args: list[str]) -> None:
    try:
        new_path = Path(*args).resolve()
        os.chdir(new_path)
    except FileNotFoundError:
        print(f"cd: {new_path.name}: No such directory")
    except PermissionError:
        print(f"cd: {new_path.name}: Permission denied")


def changes() -> str:
    subjects = {"u", "g", "o", "a"}
    modifications = {"+", "-"}
    actions = {"r", "w", "x"}

    while True:
        subject = input("Subjects to change (u, g, o, a): ").lower()

        for letter in subject:
            if letter in subjects:
                valid = True

        if valid:
            break
        else:
            print("Invalid entry")

    while True:
        modification = input("Add or remove permissions (+, -): ")

        if modification not in modifications:
            print("Invalid entry")
        else:
            break

    while True:
        action = input("What permissions to change (r, w, x): ").lower()

        for letter in action:
            if letter in actions:
                valid = True

        if valid:
            break
        else:
            print("Invalid entry")

    return f"{subject}{modification}{action}"


def mod(args: list[str]) -> None:
    try:
        if len(args) != 1:
            raise ShellError

        arg = Path(*args).resolve(strict=True)

        change = changes()

        subprocess.run(["chmod", change, arg], check=True)
    except subprocess.CalledProcessError:
        print("mod: Something went wrong")
    except FileNotFoundError:
        print("mod: No such file or directory")
    except ShellError:
        print("mod: Incorrect syntax. Type 'help' to see correct syntax")


def ls(args: list[str], redirect=False, file=None, mode=None) -> None:
    try:
        if len(args) > 1:
            raise ShellError

        directory = Path(*args).resolve(strict=True)

        if redirect:
            file = Path(str(file))
            mode = str(mode)

            with open(file, mode) as f:
                subprocess.run(["ls", "-la", directory], stdout=f, check=True)
        else:
            subprocess.run(["ls", "-la", directory], check=True)
    except subprocess.CalledProcessError:
        print("ls: Permission denied")
    except FileNotFoundError:
        print("ls: No such directory")
    except ShellError:
        print("ls: Incorrect syntax. Type 'help' to see correct syntax")


def set(args: list[str]) -> None:
    try:
        var, value = args[0].split("=")
        var = var.strip()
        value = value.strip()

        if var in ORIGINAL_VARS:
            raise ShellError

        os.environ[var] = value
    except ValueError:
        print("set: Incorrect syntax. Type 'help' to see correct syntax")
    except ShellError:
        print("set: Cannot overwrite important variable")


def unset(args: list[str]) -> None:
    var = args[0].strip()

    try:
        if var in ORIGINAL_VARS:
            raise ShellError

        del os.environ[var]
    except KeyError:
        print("unset: Variable not found")
    except ShellError:
        print("unset: Cannot unset important variable")


def write_env(output) -> None:
    for key, value in os.environ.items():
        if key not in ORIGINAL_VARS:
            output(f"{key}={value}")


def env(redirect=False, file=None, mode=None) -> None:
    if redirect:
        file = Path(str(file))
        mode = str(mode)

        with open(file, mode) as f:
            write_env(lambda line: f.write(f"{line}\n"))
    else:
        write_env(print)


def expand(args: list[str]) -> list[str]:
    return [
        os.environ.get(arg.removeprefix("$"), "") if arg.startswith("$") else arg
        for arg in args
    ]


def echo(args: list[str], redirect=False, file=None, mode=None) -> None:
    vars = expand(args)

    try:
        if redirect:
            file = Path(str(file))
            mode = str(mode)

            with open(file, mode) as f:
                subprocess.run(["echo", *vars], stdout=f, check=True)
        else:
            subprocess.run(["echo", *vars], check=True)
    except subprocess.CalledProcessError:
        print("echo: Something went wrong")


def help(redirect=False, file=None, mode=None) -> None:
    help_message = """
    cwsh, version 1.0.0

    cf <file>                       - Create <file>
    df <file>                       - Delete <file>
    rf <file>                       - Rename <file>
    md <dir>                        - Create <dir>
    dd <dir>                        - Delete <dir>
    cd <dir>                        - Change working directory to <dir>
    mod <file>                      - Change permission of <file>
    ls <dir>                        - List all content in <dir>
    set [<name>=<value>]            - Add environment variable <name> as <value>
    unset <name>                    - Remove environment variable <name>
    env                             - Show all environment variables
    echo [<value> ...]              - Display <value>
    exit                            - Close shell
    """

    if redirect:
        file = Path(str(file))
        mode = str(mode)

        with open(file, mode) as f:
            f.write(dedent(help_message))
    else:
        print(dedent(help_message))


def exit():
    print("Exiting...")
    sys.exit(0)
