from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import LEFT, RIGHT
from PIL import Image, ImageTk

from message_generator.data.data import *
from message_generator.data.models import *
from message_generator.core.messagexml import *
from message_generator.builder.builder import ProjectBuillder
from message_generator.gui.gtk_main_window import *
from message_generator.gui.tkinter_main_window import *

class TkMainWindow(tk.Tk):
    ICON_DIR="./message_generator/icons/"

    def __init__(self):
        super().__init__()
        self.loadValues()
        self.init_ui()  

    def loadValues(self):
        try:
            root = readXML('config/message.xml')
        except Exception as e:
            print(e)
            exit(1)
            return False
            
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
        #
        # Window Settings
        #
        self.title("Message Generator")
        self.geometry("500x500")
        self.resizable(True, True)
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure('Treeview', rowheight=24)
        
        #
        # Menu Bar
        #
        menuBar = Menu(self)
        fileMenu = Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="New", command=self.onNewFileMenuClick)
        fileMenu.add_command(label="Open", command=self.onOpenFileMenuClick)
        fileMenu.add_command(label="Save", command=self.onSaveFileMenuClick)
        fileMenu.add_command(label="Save As", command=self.onSaveAsFileMenuClick)
        fileMenu.add_separator()
        fileMenu.add_command(label="Export", command=self.onExportFileMenuClick)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.quit)
        
        editMenu = Menu(menuBar, tearoff=0)
        editMenu.add_command(label="Validate", command=self.onValidateEditMenuClick)

        helpMenu = Menu(menuBar, tearoff=0)
        helpMenu.add_command(label="Help Index", command=self.onHelpMenuClick)
        helpMenu.add_command(label="About...", command=self.onAboutHelpMenuClick)

        menuBar.add_cascade(label="File", menu=fileMenu)
        menuBar.add_cascade(label="Edit", menu=helpMenu)
        menuBar.add_cascade(label="Help", menu=helpMenu)
        self.config(menu=menuBar)

        #
        # Icons
        #
        iconSize=(20, 20)
        iconAddNodePath = os.path.join(self.ICON_DIR, 'add-node-48.png')
        self.iconAddNode = ImageTk.PhotoImage(Image.open(iconAddNodePath).resize(iconSize))

        #
        # Main Frame
        #
        self.main = tk.Frame(self)
        self.main.pack(fill=tk.BOTH, expand=1)

        #
        # Left Panel TreeView
        #
        self.tree = ttk.Treeview(self.main)
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)
        self.tree.heading('#0', text='Nodes', anchor='w')

        root_node=''
        self.node_interfaces = self.tree.insert(root_node, 'end', text='interfaces', open=True, image=self.iconAddNode)
        self.node_datafields = self.tree.insert(root_node, 'end', text='datafields', open=True, image=self.iconAddNode)
        self.node_enumerations = self.tree.insert(root_node, 'end', text='enumerations', open=True, image=self.iconAddNode)
        self.node_complex = self.tree.insert(root_node, 'end', text='complex', open=True, image=self.iconAddNode)
        self.node_messages = self.tree.insert(root_node, 'end', text='messages', open=True, image=self.iconAddNode)

        # to load interfaces
        for i in self.interfaces:
            self.tree.insert(self.node_interfaces, 'end', text=i.name, open=True)

        # to load datafields
        for i in self.datafields:
            self.tree.insert(self.node_datafields, 'end', text=i.name, open=True)

        # to load enumerations
        for i in self.enumerations:
            self.tree.insert(self.node_enumerations, 'end', text=i.name, open=True)
        
        # to load complex
        for i in self.complextypes:
            self.tree.insert(self.node_complex, 'end', text=i.name, open=True)

        # to load messages
        for i in self.messages:
            self.tree.insert(self.node_messages, 'end', text=i.name, open=True)
        
        self.tree.pack(side=LEFT, fill=tk.BOTH, expand=1)

        #
        # Propety Panel
        #    
        self.propertyFrame = tk.Frame(self.main)
        self.propertyTable = tk.Frame(self.propertyFrame)
        lbl1 = Label(self.propertyTable, text="Record Element")
        lbl2 = Label(self.propertyTable, text="Field Type")
        lbl3 = Label(self.propertyTable, text="Min Value")
        lbl4 = Label(self.propertyTable, text="Max Value")
        cmb1 = ttk.Combobox(self.propertyTable, values=[i.name for i in self.datafields])
        cmb2 = ttk.Combobox(self.propertyTable, values=[i.dataFormatType for i in self.datafields])
        entry1 = Entry(self.propertyTable)
        entry2 = Entry(self.propertyTable)
        
        # property labels
        lbl1.grid(row=0, column=0)
        lbl2.grid(row=1, column=0)
        lbl3.grid(row=2, column=0)
        lbl4.grid(row=3, column=0)
        # property components
        cmb1.grid(row=0, column=1)
        cmb2.grid(row=1, column=1)
        entry1.grid(row=2, column=1)
        entry2.grid(row=3, column=1)
        self.propertyTable.pack(fill=tk.BOTH, expand=1)
        self.propertyFrame.pack(side=RIGHT, fill=tk.BOTH, expand=1)

    #
    # Menu Functions
    #
    def onNewFileMenuClick(self):
        pass

    def onOpenFileMenuClick(self):
        pass

    def onSaveFileMenuClick(self):
        pass

    def onSaveAsFileMenuClick(self):
        pass

    def onExportFileMenuClick(self):
        pass

    def onValidateEditMenuClick(self):
        pass

    def onHelpMenuClick(self):
        pass

    def onAboutHelpMenuClick(self):
        pass

    def loadInterfaceComponents(self):
        pass

    #
    # Gui Functions
    #
    def item_selected(self, event):
        pass
    def on_closing(self):
        pass