from message_generator.data.models import *
from message_generator.builder.java.record import *
from message_generator.builder.java.message import *
from message_generator.builder.java.enum import *

class ProjectBuillder:
    def __init__(self) -> None:
        pass

    def setBundle(self, bundle):
        self.bundle = bundle

    def run(self):
        createRecord(self.bundle.complextypes[1], self.bundle)
        createMessage(self.bundle.messages[1], self.bundle)
        for e in self.bundle.enumerations:
            createEnumeration(e)