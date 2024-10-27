class Names:
    CREATE_FILE = "cf"
    DELETE_FILE = "df"
    RENAME_FILE = "rf"
    MAKE_DIRECTORY = "md"
    DELETE_DIRECTORY = "dd"
    CHANGE_DIRECTORY = "cd"
    MODIFY_PERMISSIONS = "mod"
    LIST_FILES = "ls"
    ADD_ENV_VAR = "set"
    SHOW_ALL_ENV = "env"
    DISPLAY = "echo"
    REMOVE_ENV_VAR = "unset"
    HELP = "help"
    EXIT = "exit"


class Symbols:
    OVERWRITE_REDIRECT = ">"
    APPEND_REDIRECT = ">>"


class ShellError(Exception):
    pass
