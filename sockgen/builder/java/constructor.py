from message_generator.data.models import *
from message_generator.core.messagecore import *
from message_generator.builder.settings import BuilderSettings as Set

def createConstructor(constructorName, recordElements, bundle, file):
    print(Set.tabstop * Set.tab + "public {}() {{".format(constructorName), file=file)
    print(Set.tabstop * Set.tab + "}\n", file=file)
    
    constructorParameters = ''
    constructorBody = ''
    strDataFormatType = ''
    
    for element in recordElements[:-1]:
        strDataFormatType = getDataFormatType(element, bundle)
        constructorParameters += "{} {}, ".format(strDataFormatType, element.name)
        constructorBody += Set.tabstop * 2 * Set.tab + "this.{} = {};\n".format(element.name, element.name)
    
    # for last item
    lastElement = recordElements[-1]
    strDataFormatType = getDataFormatType(lastElement, bundle)
    constructorParameters += "{} {}".format(strDataFormatType, lastElement.name)
    constructorBody += Set.tabstop * 2 * Set.tab + "this.{} = {};".format(lastElement.name, lastElement.name)
    
    print(Set.tabstop * Set.tab + "public {} ({}) {{".format(constructorName, constructorParameters), file=file)
    print(constructorBody, file=file)
    print(Set.tabstop * Set.tab + "}", file=file)