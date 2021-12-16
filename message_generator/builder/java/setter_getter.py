from message_generator.data.models import *
from message_generator.core.messagecore import *

def createSetterGetter(recordElement, bundle, file):
    functionName = recordElement.name[0].upper() + recordElement.name[1:]
    strDataFormatType = getDataFormatType(recordElement, bundle)
    
    # setter
    print("", file=file)
    print(Conf.tabstop * Conf.tab + "public void set{}({} value) {{".format(functionName, strDataFormatType), file=file)
    print(Conf.tabstop * 2 * Conf.tab + "{} = value;".format(recordElement.name), file=file)
    print(Conf.tabstop * Conf.tab + "}", file=file)
        
    # getter
    print("", file=file)
    print(Conf.tabstop * Conf.tab + "public {} get{}(){{".format(strDataFormatType, functionName), file=file)
    print(Conf.tabstop * 2 * Conf.tab + "return {};".format(recordElement.name), file=file)
    print(Conf.tabstop * Conf.tab + "}", file=file)