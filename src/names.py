from enum import Enum


class Names(Enum):
    CREATE_FILE = "cf"
    DELETE_FILE = "df"
    RENAME_FILE = "rf"
    MAKE_DIRECTORY = "md"
    DELETE_DIRECTORY = "dd"
    CHANGE_DIRECTORY = "cd"
    MODIFY_PERMISSIONS = "mod"
    LIST_FILES = "ls"
    HELP = "help"
    EXIT = "exit"
