from message_generator.data.models import *
from message_generator.core.messagecore import *
from message_generator.builder.settings import BuilderSettings as Set

def createSetterGetter(recordElement: RecordElementXML, bundle, file):
    functionName = recordElement.name[0].upper() + recordElement.name[1:]
    strDataFormatType = getDataFormatType(recordElement, bundle)
    
    # setter
    print("", file=file)
    print(Set.tabstop * Set.tab + "public void set{}({} value) {{".format(functionName, strDataFormatType), file=file)
    print(Set.tabstop * 2 * Set.tab + "{} = value;".format(recordElement.name), file=file)
    print(Set.tabstop * Set.tab + "}", file=file)
        
    # getter
    print("", file=file)
    print(Set.tabstop * Set.tab + "public {} get{}(){{".format(strDataFormatType, functionName), file=file)
    print(Set.tabstop * 2 * Set.tab + "return {};".format(recordElement.name), file=file)
    print(Set.tabstop * Set.tab + "}", file=file)