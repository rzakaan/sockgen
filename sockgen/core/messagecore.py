from message_generator.data.models import *

def getRecordElement(record_list, dataTypeName: str):
    for field in record_list:
        if field.name == dataTypeName:
            return field
    return None

def getDataFormatType(element, bundle : MessageBundle) -> str:
    strDataFormatType = ''
    if 'datafield' == element.recordElementType:
        df = getRecordElement(bundle.datafields, element.dataTypeName)
        if df is None: return ""
        if 'uint' == df.dataType or 'int' == df.dataType:
            if df.size == 8: strDataFormatType = 'byte'
            elif df.size == 16: strDataFormatType = 'short'
            elif df.size == 32: strDataFormatType = 'int'
            elif df.size == 64: strDataFormatType = 'long'
        elif 'float' == df.dataType:
            if df.size == 32: strDataFormatType = 'float'
            elif df.size == 64: strDataFormatType = 'double'
    elif 'enumeration' == element.recordElementType:
        enu = getRecordElement(bundle.enumerations, element.dataTypeName)
        if enu is None: return ""
        strDataFormatType = enu.name
    elif 'record' == element.recordElementType:
        record = getRecordElement(bundle.complextypes, element.dataTypeName)
        strDataFormatType = record.name
        
    return strDataFormatType