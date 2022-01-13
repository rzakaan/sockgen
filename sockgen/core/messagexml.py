import xml.etree.ElementTree as ET

from message_generator.data.models import *
from message_generator.core.messagexml import *

# ./genre/decade/movie/[year='1992']
# ./genre/decade/movie/format/[@multiple='Yes']

# ==============================================================================
#                               UTILS
# ==============================================================================

def isAttribExists(node, attrib):
    if attrib in node.attrib:
        return True
    else:
        return False

def getAttrib(node, attrib):
    if isAttribExists(node, attrib):
        return node.attrib[attrib]
    return ""

# ==============================================================================
#                               CORE
# ==============================================================================

def readXML(fileName):
    tree = ET.parse(fileName)
    return tree.getroot()
    
    
def readInterfaces(node) -> list[InterfaceXML]:
    """
    This function is for reading interface for communicating
    
    :param node
    :type node: ElementTree
    :return interfaces: list
    """
    
    root = node.find('interfaces')
    searched = root.findall('interface')
    item_list = []
    for i in searched:
        # set interface attributes
        item = InterfaceXML()
        item.name = getAttrib(i,'name')
        item.bitOrder = getAttrib(i, 'bitOrder')
        item.inByteOrder = getAttrib(i, 'inByteOrder')
        item.outByteOrder = getAttrib(i, 'outByteOrder')
        item.settings = getAttrib(i, 'settings')
        item.type = getAttrib(i, 'type')
        item.mode = getAttrib(i, 'mode')
        item.description = getAttrib(i, 'description')
        item_list.append(item)
        
        # set packets
        packets = i.findall('packet')
        for p in packets:
            pack = InterfacePacketXML()
            pack.name = getAttrib(p, 'name')
            pack.rx = getAttrib(p, 'rx')
            pack.tx = getAttrib(p, 'tx')
            item.packets.append(pack)
        
    return item_list


def readDataFields(node):
    root = node.find('datafields')
    searched = root.findall('data')
    item_list = []
    for i in searched:
        # set datafield attributes
        item = DataFieldXML()
        item.name = getAttrib(i,'name')
        item.size = int(getAttrib(i, 'size'))
        item.minValue = getAttrib(i, 'minValue')
        item.maxValue = getAttrib(i, 'maxValue')
        item.dataType = getAttrib(i, 'dataType')
        item.dataFormatType = getAttrib(i, 'dataFormatType')
        item.resolution = getAttrib(i, 'resolution')
        item.description = getAttrib(i, 'description')
        item_list.append(item)
        
    return item_list


def readEnumerations(node):
    root = node.find('enumerations')
    searched = root.findall('enum')
    item_list = []
    for i in searched:
        # set datafield attributes
        item = EnumXML()
        item.name = getAttrib(i,'name')
        item.size = getAttrib(i, 'size')
        item.minValue = getAttrib(i, 'minValue')
        item.maxValue = getAttrib(i, 'maxValue')
        item.dataFormatType = getAttrib(i, 'dataFormatType')
        item.description = getAttrib(i, 'description')
        item_list.append(item)
        
        values = i.findall('value')
        for val in values:
            v = EnumValueXML()
            v.enumName = getAttrib(val, 'enumName')
            v.enumValue = getAttrib(val, 'enumValue')
            v.description = getAttrib(val, 'description')
            item.values.append(v)
        
    return item_list
    

def readComplexTypes(node):
    root = node.find('complex')
    searched = root.findall('record')
    record_list = []
    
    for i in searched:
        record = RecordXML()
        record.name = getAttrib(i, 'name')
        record_list.append(record)
        
        elements = i.findall('element')
        for e in elements:
            item = RecordElementXML()
            item.name = getAttrib(e,'name')
            item.value = getAttrib(e, 'value')
            item.dataTypeName = getAttrib(e, 'dataTypeName')
            item.recordElementType = getAttrib(e, 'recordElementType')
            item.fieldType = getAttrib(e, 'fieldType')
            record.elements.append(item)
        
    
    return record_list


def readMessageHeader(node):
    root = node.find('complex')
    searched = root.findall('record')
    header = MessageHeaderXML()
    
    for i in searched:
        if getAttrib(i, 'recordType') == 'messageHeader':
            for e in i.findall('element'):
                item = RecordElementXML()
                item.name = getAttrib(e,'name')
                item.dataTypeName = getAttrib(e, 'dataTypeName')
                item.recordElementType = getAttrib(e, 'recordElementType')
                item.fieldType = getAttrib(e, 'fieldType')
                header.records.append(item)
        
    return header


def readMessages(node):
    root = node.find('messages')
    searched = root.findall('message')
    messages = []
    
    for i in searched:
        m = MessageXML()
        m.mid = getAttrib(i,'mid')
        m.name = getAttrib(i,'name')
        messages.append(m)
        for e in i.findall('element'):
            item = RecordElementXML()
            item.name = getAttrib(e,'name')
            item.dataTypeName = getAttrib(e, 'dataTypeName')
            item.recordElementType = getAttrib(e, 'recordElementType')
            item.fieldType = getAttrib(e, 'fieldType')
            m.elements.append(item)
        
    return messages