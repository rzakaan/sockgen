import os
from datetime import date

from message_generator.data.models import *
from message_generator.core.messagecore import *
from message_generator.builder.java.common import *
from message_generator.builder.java.setter_getter import *
from message_generator.builder.java.constructor import *

def createMessage(message: MessageXML, bundle: MessageBundle) -> bool:
    if Conf.DEBUG: print(message)
    
    today=date.today()
    who=os.popen("whoami").read().strip()
    fileName = "{}.{}".format(message.name, Conf.fileExtension)
    extends = "extends Message" if True else ""
    isComment = False
    
    f = open(fileName, 'w')
    
    # comments
    if isComment:
        print("/*", file=f)
        print(Conf.tabstop * Conf.tab + "@date {}".format(today), file=f)
        print(Conf.tabstop * Conf.tab + "@author {}".format(who), file=f)
        print(Conf.tabstop * Conf.tab + "@file {}".format(fileName), file=f)
        print("*/", file=f)

    # imports
    print("package msg;", file=f)
    print("", file=f)
    print("import enumerations.*;\n", file=f)
        
    # class header
    print("class {} {} {{".format(message.name, extends), file=f)

    # create static & final variables
    print(Conf.tabstop * " " + "public static final messageId = {}".format(message.mid), file=f)
    print("", file=f)
    
    getterAndSetter = ""
    
    # create member variables 
    for recordElement in message.elements:
        if Conf.DEBUG: print(recordElement)
        
        functionName = recordElement.name[0].upper() + recordElement.name[1:]
        strDataFormatType = getDataFormatType(recordElement, bundle)
        
        print(Conf.tabstop * " " + "private {} {};".format(strDataFormatType, recordElement.name), file=f)
    
    # create setter & getter
    for e in message.elements:
        createSetterGetter(e, bundle, f)
    
    newline(f)
    
    # create constructor
    createConstructor(message.name, message.elements, bundle, f);

    # bracket end of class 
    print("}", file=f) 
    
    f.close()
    return True