import subprocess
import sys
import os

from pathlib import Path

ORIGINAL_VARS = {x for x in os.environ.keys()}


def cf(target: list[str]):
    try:
        subprocess.run(["touch", *target], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def df(target: list[str]):
    try:
        subprocess.run(["rm", "-iv", *target], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def rf(target: list[str]):
    try:
        subprocess.run(["mv", "-iv", *target], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def md(target: list[str]):
    try:
        subprocess.run(["mkdir", "-v", *target], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def dd(target: list[str]):
    try:
        subprocess.run(["rm", "-Ivr", *target], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def cd(target: list[str]):
    try:
        new_path = Path(*target).resolve()
        os.chdir(new_path)
    except Exception as e:
        print(f"Error: {e}")


def mod(target: list[str]):
    try:
        subprocess.run(["chmod", *target], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def ls(target: list[str], redirect=False, file=None, mode=None):
    try:
        if redirect:
            file = Path(str(file))
            mode = str(mode)

            with open(file, mode) as f:
                subprocess.run(["ls", "-la", *target], stdout=f, check=True)
        else:
            subprocess.run(["ls", "-la", *target], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error: {e}")


def set(target: list[str]):
    var, value = target[0].split("=")
    var = var.strip()
    value = value.strip()

    try:
        os.environ[var] = value
    except Exception as e:
        print(f"Error: {e}")


def unset(target: list[str]):
    var = target[0].strip()

    try:
        if var in ORIGINAL_VARS:
            raise ValueError("Cannot unset important variables")
        else:
            del os.environ[var]
    except Exception as e:
        print(f"Error: {e}")


def write_env(output):
    for key, value in os.environ.items():
        if key not in ORIGINAL_VARS:
            output(f"{key}={value}")


def env(redirect=False, file=None, mode=None):
    if redirect:
        file = Path(str(file))
        mode = str(mode)

        try:
            with open(file, mode) as f:
                write_env(lambda line: f.write(f"{line}\n"))
        except FileNotFoundError as e:
            print(f"Error: {e}")
    else:
        write_env(print)


def expand(args: list[str]):
    return [
        os.environ.get(arg.removeprefix("$"), "") if arg.startswith("$") else arg
        for arg in args
    ]


def echo(target: list[str], redirect=False, file=None, mode=None):
    vars = expand(target)

    try:
        if redirect:
            file = Path(str(file))
            mode = str(mode)

            with open(file, mode) as f:
                subprocess.run(["echo", *vars], stdout=f, check=True)
        else:
            subprocess.run(["echo", *vars], check=True)
    except (subprocess.CalledProcessError, KeyError) as e:
        print(f"Error: {e}")


def help(redirect=False, file=None, mode=None):
    help_message = "Generic Help Message"

    if redirect:
        file = Path(str(file))
        mode = str(mode)

        try:
            with open(file, mode) as f:
                f.write(help_message)
        except FileNotFoundError as e:
            print(f"Error: {e}")
    else:
        print(help_message)


def exit():
    print("Exiting...")
    sys.exit(0)
