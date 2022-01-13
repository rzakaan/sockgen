
from sockgen.builder.java.builder import JavaBuilder
from sockgen.data.enum import *
from sockgen.data.models import *
from sockgen.builder.java.record import *
from sockgen.builder.java.message import *
from sockgen.builder.java.enum import *

class ProjectBuillder:
    def __init__(self) -> None:
        self.language = Language.NONE

    def setLanguage(self, language: Language) -> None:
        self.language = language

    def setBundle(self, bundle: ProjectBundle) -> None:
        self.bundle = bundle

    def build(self):
        if self.language == Language.JAVA:
            self.java()
        elif self.language == Language.CPP:
            self.cpp()
        elif self.language == Language.PYTHON:
            self.python()

    def java(self):
        builder = JavaBuilder()
        builder.setBundle(self.bundle)
        builder.build()

    def cpp(self):
        pass

    def python(self):
        pass
