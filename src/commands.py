import subprocess
import sys
import os

from pathlib import Path


def cf(target: list[str]):
    try:
        subprocess.run(["touch", *target], check=True)
    except subprocess.CalledProcessError as e:
        print("Error")


def df(target: list[str]):
    try:
        subprocess.run(["rm", "-iv", *target], check=True)
    except subprocess.CalledProcessError as e:
        print("Error")


def rf(target: list[str]):
    try:
        subprocess.run(["mv", "-iv", *target], check=True)
    except subprocess.CalledProcessError as e:
        print("Error")


def md(target: list[str]):
    try:
        subprocess.run(["mkdir", "-v", *target], check=True)
    except subprocess.CalledProcessError as e:
        print("Error")


def dd(target: list[str]):
    try:
        subprocess.run(["rm", "-Ivr", *target], check=True)
    except subprocess.CalledProcessError as e:
        print("Error")


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
        print("Error")


def ls(target: list[str]):
    try:
        subprocess.run(["ls", "-la", *target], check=True)
    except subprocess.CalledProcessError as e:
        print("Error")


def help():
    print("Generic Help Message")


def exit():
    print("Exiting...")
    sys.exit(0)
