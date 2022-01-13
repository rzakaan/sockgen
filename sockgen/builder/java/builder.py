from sockgen.builder.settings import BuilderSettings as Set
from sockgen.data.models import *
from sockgen.builder.java.record import *
from sockgen.builder.java.message import *
from sockgen.builder.java.enum import *

import os
class JavaBuilder():
    def setBundle(self, bundle: ProjectBundle):
        self.bundle = bundle
        
        # generete common directory
        try:
            os.makedirs(os.path.join(os.path.curdir, Set.outputDir, Set.MessageSettings.outputDir))
            os.makedirs(os.path.join(os.path.curdir, Set.outputDir, Set.EnumerationSettings.outputDir))
        except OSError as error:
            print("Error: {}".format(error))

    def build(self):
        if self.bundle == None:
            return
        
        for e in self.bundle.messageBundle.enumerations:
            createEnumeration(e)

        for m in self.bundle.messageBundle.messages:
            createMessage(m, self.bundle.messageBundle)
