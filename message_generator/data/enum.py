from enum import Enum

class Language(Enum):
    NONE = 0
    JAVA = 1
    CPP = 2
    PYTHON = 3

class LogType:
    INFO = 1
    WARNING = 2
    ERROR = 3