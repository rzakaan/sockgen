import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter.constants import LEFT, RIGHT
from tkinter import filedialog
from PIL import Image, ImageTk

from message_generator.data.settings import Settings
from message_generator.data.enum import *
from message_generator.data.models import *
from message_generator.core.messagexml import *
from message_generator.builder.project import ProjectBuillder
from message_generator.gui.gtk_main_window import *
from message_generator.gui.tkinter_main_window import *

class TkMainWindow(tk.Tk):
    PADX=5
    PADY=5
    ICON_DIR="./message_generator/icons/"
    TAGS = ['interfaces', 'datafields', 'enumerations', 'complex', 'messages']
    
    # Interface Properties
    BIT_ORDER = ['Intel', 'Motorola']
    BYTE_ORDER = [ 'LittleEndian', 'BigEndian' ]
    INTERFACE_TYPE = ['TCP_SERVER', 'TCP_CLIENT', 'UDP_SERVER', 'UDP_CLIENT', 'UDP_BROADCAST', 'UDP_MULTICAST', 'UDP_UNICAST', 'SERIAL', 'FILE']

    # Datafield Properties
    DATA_FORMAT_TYPE = ['BNR', 'IEEE754']
    DATA_TYPE = ['INT', 'UINT', 'FLOAT', 'STRING', 'BOOLEAN']

    LANGUAGES = ['JAVA', 'CPP', 'CSHARP', 'PYTHON', 'JAVASCRIPT']

    def __init__(self):
        super().__init__()

        # Interface 
        self.textInterfaceName = StringVar()
        self.textBitOrder = StringVar()
        self.textInByteOrder = StringVar()
        self.textOutByteOrder = StringVar()
        self.textInterfaceType = StringVar()
        self.textInterfaceSettings = StringVar()
        self.textInterfaceDescription = StringVar()

        # Datafield
        self.textDatafieldName = StringVar()
        self.textDataType = StringVar()
        self.textDataFormatType = StringVar()
        self.textDataFieldMinValue = StringVar()
        self.textDataFieldMaxValue = StringVar()
        self.textDataFieldSize = StringVar()
        self.textDataFieldResolution = StringVar()
        self.textDataFieldDescription = StringVar()

        # Enumeration
        self.textEnumName = StringVar()
        self.textEnumSize = StringVar()
        self.textEnumMinValue = StringVar()
        self.textEnumMaxValue = StringVar()
        self.textEnumDataFormatType = StringVar()
        self.textEnumDescription = StringVar()

        # General
        self.textStatusBar = StringVar()

        self.loadValues()
        self.init_ui()  
        self.log("Ready")
        self.createProject()

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
        self.log("Creating Project")
        
        mbundle = MessageBundle
        mbundle.datafields = self.datafields
        mbundle.enumerations = self.enumerations
        mbundle.complextypes = self.complextypes
        mbundle.messageHeader = self.messageHeader
        mbundle.messages = self.messages
        mbundle.interfaces = self.interfaces

        bundle = ProjectBundle()
        bundle.interfaces = self.interfaces
        bundle.messageBundle = mbundle

        builder = ProjectBuillder()
        builder.setLanguage(Language.JAVA)
        builder.setBundle(bundle)
        builder.build()    

    def init_ui(self):
        #
        # Window Settings
        #
        width=1000
        height=700
        self.title("Message Generator")
        self.geometry(str(width)+"x"+str(height))
        self.minsize(width=width, height=height)
        self.resizable(True, True)
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure('Treeview', rowheight=24)
        self.style.map("Treeview", background=[('selected', 'green')])
        self.style.layout('nodotbox.Treeview.Item', 
            [('Treeitem.padding',
            {'children': [('Treeitem.indicator', {'side': 'left', 'sticky': ''}),
                ('Treeitem.image', {'side': 'left', 'sticky': ''}),
                ('Treeitem.text', {'side': 'left', 'sticky': ''})],
            'sticky': 'nswe'})])
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
        menuBar.add_cascade(label="Edit", menu=editMenu)
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
        # Context Menu
        #
        self.contextMenu = Menu(self.main, tearoff = 0)
        self.contextMenu.add_command(label ="Add Node", command=self.onAddNodeContextMenuClick)
        self.contextMenu.add_command(label ="Remove Node", command=self.onRemoveNodeContextMenuClick)
        self.contextMenu.add_command(label ="Rename", command=self.onRenameNodeContextMenuClick)

        #
        # Status Panel
        #
        self.statusbar = tk.Label(self.main, relief=tk.SUNKEN, anchor=tk.W, textvariable=self.textStatusBar)

        #
        # Node Panel
        #
        self.tree = ttk.Treeview(self.main, style='nodotbox.Treeview')
        self.tree.bind('<<TreeviewSelect>>', self.treeViewItemSelected)
        self.tree.bind("<Button-3>", self.do_popup)
        self.tree.heading('#0', text='Nodes', anchor='w')

        root_node=''
        self.node_interfaces = self.tree.insert(root_node, 'end', text='interfaces', open=True, image=self.iconAddNode, tags=('parent'))
        self.node_datafields = self.tree.insert(root_node, 'end', text='datafields', open=True, image=self.iconAddNode, tags=('parent'))
        self.node_enumerations = self.tree.insert(root_node, 'end', text='enumerations', open=True, image=self.iconAddNode, tags=('parent'))
        self.node_complex = self.tree.insert(root_node, 'end', text='complex', open=True, image=self.iconAddNode, tags=('parent'))
        self.node_messages = self.tree.insert(root_node, 'end', text='messages', open=True, image=self.iconAddNode, tags=('parent'))

        # to load interfaces
        for i in self.interfaces:
            self.tree.insert(self.node_interfaces, 'end', text=i.name, tags=('child'))

        # to load datafields
        for i in self.datafields:
            self.tree.insert(self.node_datafields, 'end', text=i.name, tags=('child'))

        # to load enumerations
        for i in self.enumerations:
            self.tree.insert(self.node_enumerations, 'end', text=i.name, tags=('child'))
        
        # to load complex
        for i in self.complextypes:
            self.tree.insert(self.node_complex, 'end', text=i.name, tags=('child'))

        # to load messages
        for i in self.messages:
            self.tree.insert(self.node_messages, 'end', text=i.name, tags=('child'))

        self.propertyFrame = tk.LabelFrame(self.main, text="Properties", height=300)
        self.propertyTable = tk.Frame(self.propertyFrame)
        self.propertyTable.pack(fill=tk.BOTH, padx=self.PADX, pady=self.PADY)        

        #
        # Configuration Panel
        #
        self.textLanguages = StringVar()
        self.confFrame = tk.LabelFrame(self.main, text="Configurations")
        self.cmbLanguages = ttk.Combobox(self.confFrame, values=[i for i in self.LANGUAGES], textvariable=self.textLanguages, state="readonly")
        self.cmbLanguages.pack(padx=self.PADX, pady=self.PADY)

        #
        # Byte Panel
        #
        self.byteFrame = tk.Frame(self.main)
        columns = ('Address', '7', '6', 5, '4', '3', '2', '1', '0')
        self.byteTree = ttk.Treeview(self.byteFrame, columns=columns, show='headings')
        #self.byteTree.bind('<<TreeviewSelect>>', self.byteTreeViewItemSelected)
        self.byteTree.heading('Address', text='Address', anchor='w')        
        self.byteTree.heading('7', text='7', anchor='w')
        self.byteTree.heading('6', text='6', anchor='w')
        self.byteTree.heading('5', text='5', anchor='w')
        self.byteTree.heading('4', text='4', anchor='w')
        self.byteTree.heading('3', text='3', anchor='w')
        self.byteTree.heading('2', text='2', anchor='w')
        self.byteTree.heading('1', text='1', anchor='w')
        self.byteTree.heading('0', text='0', anchor='w')

        self.byteTree.column('Address', stretch=NO, width=55)
        self.byteTree.column('7', stretch=NO, width=25)
        self.byteTree.column('6', stretch=NO, width=25)
        self.byteTree.column('5', stretch=NO, width=25)
        self.byteTree.column('4', stretch=NO, width=25)
        self.byteTree.column('3', stretch=NO, width=25)
        self.byteTree.column('2', stretch=NO, width=25)
        self.byteTree.column('1', stretch=NO, width=25)
        self.byteTree.column('0', stretch=NO, width=25)
        self.byteTree.pack(fill=tk.BOTH, expand=1)

        # Example Data        
        self.byteTree.insert('', 'end', text="0x01", values=('0x01', 0, 0, 0, 0, 0, 0, 0, 0))
        self.byteTree.insert('', 'end', text="0x02", values=('0x02', 0, 0, 0, 0, 0, 0, 0, 0))

        #
        # Window Pack
        #
        self.statusbar.pack(side=BOTTOM, fill=tk.X)
        self.tree.pack(side=LEFT, fill=tk.BOTH, expand=1)
        self.propertyFrame.pack(side=LEFT, fill=tk.BOTH, padx=self.PADX)
        self.confFrame.pack(side=RIGHT, fill=tk.BOTH, expand=1, padx=self.PADX)
        self.byteFrame.pack(side=RIGHT, fill=tk.BOTH, expand=1, padx=self.PADX)

    def loadByteCodes(self, bytecodes):
        self.byteTree.delete(*self.byteTree.get_children())
        for i in bytecodes:
            self.byteTree.insert('', 'end', text=i.address, values=(i.byte7, i.byte6, i.byte5, i.byte4, i.byte3, i.byte2, i.byte1, i.byte0))
    #
    # Context Menu Callbacks
    #
    def do_popup(self, event):
        try:
            self.contextMenu.tk_popup(event.x_root, event.y_root)
        finally:
            self.grab_release()
    
    def onAddNodeContextMenuClick(self):
        parent, current = self.getTreeViewSelection()
    
    def onRemoveNodeContextMenuClick(self):
        parent, current = self.getTreeViewSelection()
    
    def onRenameNodeContextMenuClick(self):
        parent, current = self.getTreeViewSelection()

    #
    # Menu Functions
    #
    def onNewFileMenuClick(self):
        pass

    def onOpenFileMenuClick(self):
        filepath = filedialog.askopenfilename(initialdir=os.path.curdir)
        Settings().configFile = filepath
        self.log("Loading config file: %s" % filepath)

    def onSaveFileMenuClick(self):
        result = filedialog.asksaveasfile()

    def onSaveAsFileMenuClick(self):
        result = filedialog.asksaveasfile()

    def onExportFileMenuClick(self):
        pass

    def onValidateEditMenuClick(self):
        pass

    def onHelpMenuClick(self):
        pass

    def onAboutHelpMenuClick(self):
        pass

    #
    # Gui Functions
    #
    def log(self, message, logtype: LogType = LogType.INFO):
        if LogType.ERROR == logtype:
            self.statusbar.config(font=('Arial 10 bold'))
            self.statusbar.config(fg="white")
            self.statusbar.config(bg="red")
        elif LogType.WARNING == logtype:
            self.statusbar.config(bg="yellow")
        self.textStatusBar.set(message)

    def getTreeViewSelection(self):
        curId = self.tree.selection()[0]
        parentId = self.tree.parent(curId)
        parent = self.tree.item(parentId)
        current = self.tree.item(curId)
        return parent, current

    def treeViewItemSelected(self, event):
        parent, current = self.getTreeViewSelection()

        if "parent" in current['tags']:
            return

        self.clearFrame(self.propertyTable)

        if parent['text'] == 'interfaces':
            interface = self.findNode(current['text'], self.interfaces)
            self.loadInterfaceComponents()
            self.loadInterfaceData(interface)

        elif parent['text'] == 'datafields':
            enum = self.findNode(current['text'], self.datafields)
            self.loadDatafieldComponents()
            self.loadDatafieldData(enum)

        elif parent['text'] == 'enumerations':
            enum = self.findNode(current['text'], self.enumerations)
            self.loadEnumerationComponents()
            self.loadEnumerationData(enum)

        elif parent['text'] == 'complex':
            self.loadComplexTypeComponents()
        elif parent['text'] == 'messages':
            self.loadMessageComponents()
        else:
            print('Unknown Selected')

    def clearFrame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def findNode(self, name, array):
        for i in array:
            if name == i.name:
                return i
        return None

    def loadInterfaceData(self, interface):
        self.textInterfaceName.set(interface.name)
        self.textBitOrder.set(interface.bitOrder)
        self.textInByteOrder.set(interface.inByteOrder)
        self.textOutByteOrder.set(interface.outByteOrder)
        self.textInterfaceType.set(interface.interfaceType)
        self.textInterfaceSettings.set(interface.interfaceSettings)
        self.textInterfaceDescription.set(interface.description)

    def loadDatafieldData(self, datafield):
        self.textDatafieldName.set(datafield.name)
        self.textDataType.set(datafield.dataType)
        self.textDataFormatType.set(datafield.dataFormatType)
        self.textDataFieldMinValue.set(datafield.minValue)
        self.textDataFieldMaxValue.set(datafield.maxValue)
        self.textDataFieldSize.set(datafield.size)
        self.textDataFieldResolution.set(datafield.description)
        self.textInterfaceDescription.set(datafield.description)

    def loadEnumerationData(self, enum):
        self.textEnumName.set(enum.name)
        self.textEnumSize.set(enum.size)
        self.textEnumMinValue.set(enum.minValue)
        self.textEnumMaxValue.set(enum.maxValue)
        self.textEnumDataFormatType.set(enum.dataFormatType)
        self.textEnumDescription.set(enum.description)

    def loadInterfaceComponents(self):
        lblInterfaceName = Label(self.propertyTable, text="Interface Name")
        lblBitOrder = Label(self.propertyTable, text="Bit Order")
        lblInByteOrder = Label(self.propertyTable, text="In Byte Order")
        lblOutByteOrder = Label(self.propertyTable, text="Out Byte Order")
        lblInterfaceType = Label(self.propertyTable, text="Interface Type")
        lblInterfaceSettings = Label(self.propertyTable, text="Interface Settings")
        lblInterfaceDescription = Label(self.propertyTable, text="Interface Description")

        self.entryInterfaceName = Entry(self.propertyTable, textvariable=self.textInterfaceName)
        self.cmbBitOrder = ttk.Combobox(self.propertyTable, values=[i for i in self.BIT_ORDER], textvariable=self.textBitOrder, state="readonly")
        self.cmbInByteOrder = ttk.Combobox(self.propertyTable, values=[i for i in self.BYTE_ORDER], textvariable=self.textInByteOrder, state="readonly")
        self.cmbOutByteOrder = ttk.Combobox(self.propertyTable, values=[i for i in self.BYTE_ORDER], textvariable=self.textOutByteOrder, state="readonly")
        self.cmbInterfaceType = ttk.Combobox(self.propertyTable, values=[i for i in self.INTERFACE_TYPE], textvariable=self.textInterfaceType, state="readonly")
        self.cmbInterfaceSettings = Entry(self.propertyTable, textvariable=self.textInterfaceSettings)
        self.entryInterfaceDescription = Entry(self.propertyTable, textvariable=self.textInterfaceDescription)
        
        # property labels
        lblInterfaceName.grid(row=0, column=0, padx=self.PADX, pady=self.PADY)
        lblBitOrder.grid(row=1, column=0, padx=self.PADX, pady=self.PADY)
        lblInByteOrder.grid(row=2, column=0, padx=self.PADX, pady=self.PADY)
        lblOutByteOrder.grid(row=3, column=0, padx=self.PADX, pady=self.PADY)
        lblInterfaceType.grid(row=4, column=0, padx=self.PADX, pady=self.PADY)
        lblInterfaceSettings.grid(row=5, column=0, padx=self.PADX, pady=self.PADY)
        lblInterfaceDescription.grid(row=6, column=0, padx=self.PADX, pady=self.PADY)

        # property components
        COL=1
        self.entryInterfaceName.grid(row=0, column=COL, sticky="W")
        self.cmbBitOrder.grid(row=1, column=COL, sticky="W")
        self.cmbInByteOrder.grid(row=2, column=COL, sticky="W")
        self.cmbOutByteOrder.grid(row=3, column=COL, sticky="W")
        self.cmbInterfaceType.grid(row=4, column=COL, sticky="W")
        self.cmbInterfaceSettings.grid(row=5, column=COL, sticky="W")
        self.entryInterfaceDescription.grid(row=6, column=COL, sticky="W")
    
    def loadDatafieldComponents(self):
        lblName = Label(self.propertyTable, text="Name")
        lblDataType = Label(self.propertyTable, text="Data Type")
        lblDataFormatType = Label(self.propertyTable, text="Data Format Type")
        lblMinVallue = Label(self.propertyTable, text="Min Value")
        lblMaxValue = Label(self.propertyTable, text="Max Value")
        lblSize = Label(self.propertyTable, text="Size")
        lblResolution = Label(self.propertyTable, text="Resolution")
        lblDescription = Label(self.propertyTable, text="Description")

        entryName = Entry(self.propertyTable, textvariable=self.textDatafieldName)
        cmbDataType = ttk.Combobox(self.propertyTable, values=[i for i in self.DATA_TYPE], textvariable=self.textDataType, state="readonly")
        cmbDataFormatType = ttk.Combobox(self.propertyTable, values=[i for i in self.DATA_FORMAT_TYPE], textvariable=self.textDataFormatType, state="readonly")
        entryMinValue = Entry(self.propertyTable, textvariable=self.textDataFieldMinValue)
        entryMaxValue = Entry(self.propertyTable, textvariable=self.textDataFieldMaxValue)
        entrySize = Entry(self.propertyTable, textvariable=self.textDataFieldSize)
        entryResolution = Entry(self.propertyTable, textvariable=self.textDataFieldResolution)
        entryDescription = Entry(self.propertyTable, textvariable=self.textDataFieldDescription)        
        
        # property labels
        lblName.grid(row=0, column=0, padx=self.PADX, pady=self.PADY)
        lblDataType.grid(row=1, column=0, padx=self.PADX, pady=self.PADY)
        lblDataFormatType.grid(row=2, column=0, padx=self.PADX, pady=self.PADY)
        lblMinVallue.grid(row=3, column=0, padx=self.PADX, pady=self.PADY)
        lblMaxValue.grid(row=4, column=0, padx=self.PADX, pady=self.PADY)
        lblSize.grid(row=5, column=0, padx=self.PADX, pady=self.PADY)
        lblResolution.grid(row=6, column=0, padx=self.PADX, pady=self.PADY)
        lblDescription.grid(row=7, column=0, padx=self.PADX, pady=self.PADY)
        
        # property components
        entryName.grid(row=0, column=1, sticky="W")
        cmbDataType.grid(row=1, column=1, sticky="W")
        cmbDataFormatType.grid(row=2, column=1, sticky="W")
        entryMinValue.grid(row=3, column=1, sticky="W")
        entryMaxValue.grid(row=4, column=1, sticky="W")
        entrySize.grid(row=5, column=1, sticky="W")
        entryResolution.grid(row=6, column=1, sticky="W")
        entryDescription.grid(row=7, column=1, sticky="W")  

    def loadEnumerationComponents(self):
        lblName = Label(self.propertyTable, text="Name")
        lblDataFormatType = Label(self.propertyTable, text="Data Format Type")
        lblMinVallue = Label(self.propertyTable, text="Min Value")
        lblMaxValue = Label(self.propertyTable, text="Max Value")
        lblSize = Label(self.propertyTable, text="Size")
        lblDescription = Label(self.propertyTable, text="Description")

        entryName = Entry(self.propertyTable, textvariable=self.textEnumName)
        cmbDataFormatType = ttk.Combobox(self.propertyTable, values=[i for i in self.DATA_FORMAT_TYPE], textvariable=self.textEnumDataFormatType, state="readonly")
        entryMinValue = Entry(self.propertyTable, textvariable=self.textEnumMinValue)
        entryMaxValue = Entry(self.propertyTable, textvariable=self.textEnumMaxValue)
        entrySize = Entry(self.propertyTable, textvariable=self.textEnumSize)
        entryDescription = Entry(self.propertyTable, textvariable=self.textEnumDescription)
        
        # property labels
        lblName.grid(row=0, column=0, padx=self.PADX, pady=self.PADY)
        lblDataFormatType.grid(row=2, column=0, padx=self.PADX, pady=self.PADY)
        lblMinVallue.grid(row=3, column=0, padx=self.PADX, pady=self.PADY)
        lblMaxValue.grid(row=4, column=0, padx=self.PADX, pady=self.PADY)
        lblSize.grid(row=5, column=0, padx=self.PADX, pady=self.PADY)
        lblDescription.grid(row=7, column=0, padx=self.PADX, pady=self.PADY)
        
        # property components
        entryName.grid(row=0, column=1, sticky="W")
        cmbDataFormatType.grid(row=2, column=1, sticky="W")
        entryMinValue.grid(row=3, column=1, sticky="W")
        entryMaxValue.grid(row=4, column=1, sticky="W")
        entrySize.grid(row=5, column=1, sticky="W")
        entryDescription.grid(row=7, column=1, sticky="W")  

    def loadComplexTypeComponents(self):
        pass
        
    def on_closing(self):
        pass