from message_generator.data.models import *
from message_generator.core.messagecore import *
from message_generator.builder.java.common import *
from message_generator.builder.java.setter_getter import *
from message_generator.builder.java.constructor import *

def createRecord(record: RecordXML, bundle: MessageBundle) -> bool:
    if Conf.DEBUG: print(record)
    
    fileName = "{}.{}".format(record.name, Conf.fileExtension)
    getterAndSetter = "";
    
    f = open(fileName, 'w')
    
    # imports
    print("package records;", file=f)
    print("", file=f)
    print("import enumerations.*;\n", file=f)
    
    # class header
    print("class {} {{".format(record.name), file=f)
    
    # create member variables 
    for recordElement in record.elements:
        strDataFormatType = ''
        functionName = recordElement.name[0].upper() + recordElement.name[1:]
        
        if 'datafield' == recordElement.recordElementType:
            df = getRecordElement(bundle.datafields, recordElement.dataTypeName)
            if df is None: continue
            
            if 'uint' == df.dataType or 'int' == df.dataType:
                if df.size == 8: strDataFormatType = 'byte'
                elif df.size == 16: strDataFormatType = 'short'
                elif df.size == 32: strDataFormatType = 'int'
                elif df.size == 64: strDataFormatType = 'long'
            elif 'float' == df.dataType:
                if df.size == 32: strDataFormatType = 'float'
                elif df.size == 64: strDataFormatType = 'double'
            
            print(Conf.tabstop * " " + "private {} {};".format(strDataFormatType, recordElement.name), file=f)
            
        elif 'enumeration' == recordElement.recordElementType:
            enu = getRecordElement(bundle.enumerations, recordElement.dataTypeName)
            if enu is None: continue
            strDataFormatType = enu.name
            
            print(Conf.tabstop * Conf.tab + "private {} {};".format(enu.name, recordElement.name), file=f)

        elif 'record' == recordElement.recordElementType:
            strDataFormatType = recordElement.name
            pass
        
        #getterAndSetter += "\n"
        #getterAndSetter += Conf.tabstop * " " + "public void set{}({} value) {{\n".format(functionName, strDataFormatType)
        #getterAndSetter += Conf.tabstop * 2 * " " + "{} = value;\n".format(recordElement.name)
        #getterAndSetter += Conf.tabstop * " " + '}\n'
        
        #getterAndSetter += "\n"
        #getterAndSetter += Conf.tabstop * " " + "public {} get{}() {{\n".format(strDataFormatType, functionName)
        #getterAndSetter += Conf.tabstop * 2 * " " + "return {};\n".format(recordElement.name)
        #getterAndSetter += Conf.tabstop * " " + '}\n'
        
    # create setter & getter
    for e in record.elements:
        createSetterGetter(e, bundle, f)
    
    newline(f)
    
    # create constructor
    createConstructor(record.name, record.elements, bundle, f);
    
    print('}', file=f)
    f.close()
    return True
