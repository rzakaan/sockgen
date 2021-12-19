import tkinter as tk
from tkinter.constants import LEFT, RIGHT
import tkinter.ttk as ttk

from message_generator.data.data import *
from message_generator.data.models import *
from message_generator.core.messagexml import *
from message_generator.builder.builder import ProjectBuillder
from message_generator.gui.gtk_main_window import *
from message_generator.gui.tkinter_main_window import *

class TkMainWindow(tk.Tk):   
    def __init__(self):
        super().__init__()
        self.init_ui()  

    def loadValues(self):
        try:
            root = readXML('message.xml')
        except Exception as e:
            exit("Error Xml Parsing")
            
        self.interfaces = readInterfaces(root)
        self.datafields = readDataFields(root)
        self.enumerations = readEnumerations(root)
        self.messageHeader = readMessageHeader(root) 
        self.complextypes = readComplexTypes(root)
        self.messages = readMessages(root)

    def createProject(self):
        bundle = MessageBundle
        bundle.datafields = self.datafields
        bundle.enumerations = self.enumerations
        bundle.complextypes = self.complextypes
        bundle.messageHeader = self.messageHeader
        builder = ProjectBuillder()
        builder.setBundle(bundle)
        builder.run()    

    def init_ui(self):
        self.title("Message Generator")
        self.geometry("500x500")
        self.resizable(False, False)
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.frame = tk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=1)

        self.treeView = ttk.Treeview(self.frame)
        self.treeView.bind('<<TreeviewSelect>>', self.item_selected)
        self.treeView.pack(side=LEFT, fill=tk.BOTH, expand=1)

        self.propertyFrame = tk.Frame(self.frame)        
        self.listProperty = tk.Listbox(self.propertyFrame)
        self.listProperty.pack(side=LEFT, fill=tk.BOTH, expand=1)
        self.propertyFrame.pack(side=RIGHT, fill=tk.BOTH, expand=1)
        
    def item_selected(self, event):
        pass
    def on_closing(self):
        pass