import shlex
from names import Names
import commands


def parse(full_command: str):
    args = shlex.split(full_command)
    command = args.pop(0)

    match (command):
        case Names.CREATE_FILE.value:
            commands.cf(args)
        case Names.DELETE_FILE.value:
            commands.df(args)
        case Names.RENAME_FILE.value:
            commands.rf(args)
        case Names.MAKE_DIRECTORY.value:
            commands.md(args)
        case Names.DELETE_DIRECTORY.value:
            commands.dd(args)
        case Names.CHANGE_DIRECTORY.value:
            commands.cd(args)
        case Names.MODIFY_PERMISSIONS.value:
            commands.mod(args)
        case Names.LIST_FILES.value:
            commands.ls(args)
        case Names.HELP.value:
            commands.help()
        case Names.EXIT.value:
            commands.exit()
        case _:
            print("Unknown Command.")
