import os
from sockgen.data.models import *
from sockgen.core.messagecore import *
from sockgen.builder.settings import BuilderSettings as Set
from sockgen.builder.java.common import *
from sockgen.builder.java.setter_getter import *
from sockgen.builder.java.constructor import *

def createMessage(message: MessageXML, bundle: MessageBundle) -> bool:
    if Set.DEBUG: print(message)
    
    fileName = "{}.{}".format(message.name, Set.fileExtension)
    filePath = os.path.join(os.path.curdir, Set.outputDir, Set.MessageSettings.outputDir, fileName)
    extends = "extends Message" if True else ""
    
    f = open(filePath, 'w')

    # comments
    if Set.commentAdd:
        fileComment(f)

    # imports
    print("package {};".format(Set.MessageSettings.outputDir), file=f)
    print("", file=f)
    print("import {}.*;\n".format(Set.EnumerationSettings.outputDir), file=f)
        
    # class header
    print("class {} {} {{".format(message.name, extends), file=f)

    # create static & final variables
    print(Set.tabstop * " " + "public static final messageId = {}".format(message.mid), file=f)
    print("", file=f)
    
    # create member variables 
    for recordElement in message.elements:
        if Set.DEBUG: print(recordElement)
        
        functionName = recordElement.name[0].upper() + recordElement.name[1:]
        strDataFormatType = getDataFormatType(recordElement, bundle)
        
        print(Set.tabstop * " " + "private {} {};".format(strDataFormatType, recordElement.name), file=f)
    
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