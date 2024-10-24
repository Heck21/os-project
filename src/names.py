from enum import Enum
from typing import Mapping


class Names(Mapping):
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


class Symbols(Mapping):
    OVERWRITE_REDIRECT = ">"
    APPEND_REDIRECT = ">>"
