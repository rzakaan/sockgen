#!/usr/bin/python


import builtins
from message_generator.data.data import *
from message_generator.data.models import *
from message_generator.core.messagexml import *
from message_generator.builder.builder import ProjectBuillder

def createProject():
    try:
        root = readXML('message.xml')
    except Exception as e:
        exit("Error Xml Parsing")
        
    interfaces = readInterfaces(root)
    datafields = readDataFields(root)
    enumerations = readEnumerations(root)
    messageHeader = readMessageHeader(root) 
    complextypes = readComplexTypes(root)
    messages = readMessages(root)
    
    bundle = MessageBundle
    bundle.datafields = datafields
    bundle.enumerations = enumerations
    bundle.complextypes = complextypes
    bundle.messageHeader = messageHeader

    builder = ProjectBuillder()
    builder.setBundle(bundle)
    builder.run()    

import os
if __name__ == '__main__':
    createProject()         