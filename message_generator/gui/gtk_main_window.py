import os

try:
    import gi
    gi.require_version('Gtk', '3.0') 
    from gi.repository import GLib, Gio, Gtk
except Exception as e:
    exit("Error importin gtk")

class GtkMainWindow():
    # Constants
    UI_DIR="./message_generator/gui/"
    

    def __init__(self):
        self.mylist = [("Riza", 17, "Software Engineer"),
            ("Kaan", 28, "Computer Engineer")]

        self.list_store = Gtk.ListStore(str, int, str)

        super().__init__()
        self.init_ui()
        Gtk.main()

    def init_ui(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.join(self.UI_DIR, "gui.glade"))        
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("Main")
        self.window.connect("delete-event", self.on_window_destroy)
        self.window.show_all()

        self.button = self.builder.get_object("buttonAdd")
        self.treeView = self.builder.get_object("treeView")
        self.treeView.set_model(self.list_store)
    
    def init_values(self):
        for i in self.mylist:
            self.list_store.append(list(i))

        for i, title in enumerate(["Name", "Age", "Job"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(title, renderer, text=i)
            self.treeView.append_column(column)

    def on_buttonAdd_clicked(self, widget):
        pass

    def on_window_destroy(self, widget, param):
        Gtk.main_quit()