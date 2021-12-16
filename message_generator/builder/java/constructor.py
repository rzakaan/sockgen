from message_generator.data.models import *
from message_generator.core.messagecore import *

def createConstructor(constructorName, recordElements, bundle, file):
    print(Conf.tabstop * " " + "public {}() {{".format(constructorName), file=file)
    print(Conf.tabstop * " " + "}\n", file=file)
    
    constructorParameters = ''
    constructorBody = ''
    strDataFormatType = ''
    
    for element in recordElements[:-1]:
        strDataFormatType = getDataFormatType(element, bundle)
        constructorParameters += "{} {}, ".format(strDataFormatType, element.name)
        constructorBody += Conf.tabstop * 2 * Conf.tab + "this.{} = {};\n".format(element.name, element.name)
    
    # for last item
    lastElement = recordElements[-1]
    strDataFormatType = getDataFormatType(lastElement, bundle)
    constructorParameters += "{} {}".format(strDataFormatType, lastElement.name)
    constructorBody += Conf.tabstop * 2 * Conf.tab + "this.{} = {};".format(lastElement.name, lastElement.name)
    
    print(Conf.tabstop * " " + "public {} ({}) {{".format(constructorName, constructorParameters), file=file)
    print(constructorBody, file=file)
    print(Conf.tabstop * " " + "}", file=file)