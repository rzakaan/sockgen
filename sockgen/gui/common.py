import tkinter

class Tk():
    def clear_frame(frame: tkinter.Frame) -> None:
        for widget in frame.winfo_children():
            widget.destroy()

    def get_treeview_selection(treeview: tkinter.Treeview):
        selectedId = treeview.selection()[0]
        parentId = treeview.parent(selectedId)
        parent = treeview.item(parentId)
        selected = treeview.item(selectedId)
        return selected, parent
