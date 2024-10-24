import subprocess
import sys
import os

from pathlib import Path


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
    if redirect:
        file = Path(str(file))
        mode = str(mode)

        try:
            with open(file, mode) as f:
                subprocess.run(["ls", "-la", *target], stdout=f, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Error: {e}")
    else:
        try:
            subprocess.run(["ls", "-la", *target], check=True)
        except subprocess.CalledProcessError as e:
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
