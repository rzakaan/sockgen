import os
from datetime import date
from message_generator.builder.settings import BuilderSettings as Set

def newline(file):
    print('', file=file)

def fileComment(file):
    today=date.today()
    who=os.popen("whoami").read().strip()    
    
    print("/*", file=file)
    print(Set.tabstop * Set.tab + "@date {}".format(today), file=file)
    print(Set.tabstop * Set.tab + "@author {}".format(who), file=file)
    print(Set.tabstop * Set.tab + "@file {}".format(os.path.basename(file.name)), file=file)
    print("*/", file=file)