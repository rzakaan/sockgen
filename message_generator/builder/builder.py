from enum import Enum
from message_generator.data.models import *
from message_generator.builder.java.record import *
from message_generator.builder.java.message import *
from message_generator.builder.java.enum import *

class Language(Enum):
    JAVA = 1
    CPP = 2
    PYTHON = 3

class ProjectBuillder:
    def __init__(self) -> None:
        pass

    def setLanguage(self, language: Language) -> None:
        self.language = language

    def setBundle(self, bundle: ProjectBundle) -> None:
        self.bundle = bundle

    def run(self):
        if self.language == Language.JAVA:
            self.java()
        elif self.language == Language.CPP:
            self.cpp()
        elif self.language == Language.PYTHON:
            self.python()

    def java(self):
        for e in self.bundle.enumerations:
            createEnumeration(e)

        for m in self.bundle.messages:
            createMessage(m, self.bundle)

    def cpp(self):
        pass

    def python(self):
        pass
