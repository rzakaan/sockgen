class ProjectBundle():
    interfaces = None
    messageBundle = None
    
class MessageBundle():
    datafields = None
    enumerations = None
    complextypes = None
    messageHeader = None
    messages = None

class InterfacePacketXML:
    name='MsgUnknown' 
    rx='false'
    tx='false'
    
class InterfacePacketXML:
    name='MsgUnknown' 
    rx='false'
    tx='false'

class InterfaceXML:
    def __init__(self):
        self.name=''
        self.description=''
        self.bitOrder='' 
        self.inByteOrder='' 
        self.outByteOrder='' 
        self.interfaceSettings='' 
        self.interfaceType='' 
        self.packets=[]
    
    def __str__(self):
        v  ='Interface {}\n'.format(self.name)
        v +='|--> description({})\n'.format(self.description)
        v +='|--> bitOrder({})\n'.format(self.bitOrder)
        v +='|--> inByteOrder({})\n'.format(self.inByteOrder)
        v +='|--> outByteOrder({})\n'.format(self.outByteOrder)
        v +='|--> interfaceSettings({})\n'.format(self.interfaceSettings)
        v +='|--> interfaceType({})\n'.format(self.interfaceType)
        v +='|--> packets({})\n'.format(', '.join([i.name for i in self.packets]))
        return v

class DataFieldXML:
    def __init__(self):
        self.name=''
        self.size=''
        self.description=''
        self.minValue=''
        self.maxValue=''
        self.dataType='' 
        self.dataFormatType='' 
        self.resolution=''
    
    def __str__(self):
        v  ='DataField {}({})\n'.format(self.name, self.size)
        v +='|--> minValue({})\n'.format(self.minValue)
        v +='|--> maxValue({})\n'.format(self.maxValue)
        v +='|--> dataType({})\n'.format(self.dataType)
        v +='|--> dataFormatType({})\n'.format(self.dataFormatType)
        v +='|--> resolution({})\n'.format(self.resolution)
        return v

class EnumXML:
    def __init__(self):
        self.name=''
        self.size=''
        self.description=''
        self.minValue=''
        self.maxValue=''
        self.dataFormatType='' 
        self.values=[]

    def __str__(self):
        v  ='Enumeration {}({})\n'.format(self.name, self.size)
        v +='|--> minValue({})\n'.format(self.minValue)
        v +='|--> maxValue({})\n'.format(self.maxValue)
        v +='|--> dataFormatType({})\n'.format(self.dataFormatType)
        v +='|--> description({})\n'.format(self.description)
        return v

class EnumValueXML:
    def __init__(self):
        self.enumName=''
        self.enumValue=''
        self.description=''

    def __str__(self):
        v  ='|--> {}({})'.format(self.enumName, self.enumValue)
        return v

class RecordXML:
    def __init__(self):    
        self.name=''
        self.elements: RecordElementXML=[]
    
    def __str__(self):
        v  ='Record {}\n'.format(self.name)
        for r in self.elements:
            v += '|--> {}\n'.format(r)
        return v

class RecordElementXML:
    def __init__(self):
        self.name=''
        self.recordElementType='' 
        self.dataTypeName='' 
        self.fieldType='' 

    def __str__(self):
        v  ='RecordElement {}({} -> {})'.format(self.name, self.recordElementType, self.dataTypeName)
        return v

class MessageHeaderXML:
    def __init__(self):
        self.records=[]
    
    def __str__(self):
        v = 'MessageHeader\n'
        for r in self.records:
            v += '|--> {}\n'.format(r)
        
        return v

class MessageXML:
    def __init__(self):
        self.mid=''
        self.name=''
        self.elements=[] 

    def __str__(self):
        v  ='Message {}({})'.format(self.name, self.mid)
        return v