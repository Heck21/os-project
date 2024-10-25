import shlex
from names import Names, Symbols
import commands


def parse(full_command: str):
    args = shlex.split(full_command)
    command = args.pop(0).lower()

    redirectable_commands = [
        Names.LIST_FILES,
        Names.SHOW_ALL_ENV,
        Names.DISPLAY,
        Names.HELP,
    ]

    if (
        Symbols.OVERWRITE_REDIRECT in args or Symbols.APPEND_REDIRECT in args
    ) and command in redirectable_commands:
        if Symbols.OVERWRITE_REDIRECT in args:
            mode = "w"
        else:
            mode = "a"

        execute_with_redirect(command, args, mode)
    else:
        execute(command, args)


def execute(command: str, args: list[str], redirect=False, file=None, mode=None):
    match (command):
        case Names.CREATE_FILE:
            commands.cf(args)
        case Names.DELETE_FILE:
            commands.df(args)
        case Names.RENAME_FILE:
            commands.rf(args)
        case Names.MAKE_DIRECTORY:
            commands.md(args)
        case Names.DELETE_DIRECTORY:
            commands.dd(args)
        case Names.CHANGE_DIRECTORY:
            commands.cd(args)
        case Names.MODIFY_PERMISSIONS:
            commands.mod(args)
        case Names.LIST_FILES:
            commands.ls(args, redirect, file, mode)
        case Names.ADD_ENV_VAR:
            commands.set(args)
        case Names.REMOVE_ENV_VAR:
            commands.unset(args)
        case Names.SHOW_ALL_ENV:
            commands.env(redirect, file, mode)
        case Names.DISPLAY:
            commands.echo(args, redirect, file, mode)
        case Names.HELP:
            commands.help(redirect, file, mode)
        case Names.EXIT:
            commands.exit()
        case _:
            print("Unknown Command.")


def execute_with_redirect(command: str, args: list[str], mode: str):
    output_file = args.pop()

    if mode == "w":
        args.remove(Symbols.OVERWRITE_REDIRECT)
    else:
        args.remove(Symbols.APPEND_REDIRECT)

    execute(command, args, redirect=True, file=output_file, mode=mode)
