#!/usr/bin/python

import argparse

from message_generator.gui.gtk_main_window import *
from message_generator.gui.tkinter_main_window import *

if __name__ == '__main__':  
    parser = argparse.ArgumentParser(description='Generate a message from a XML file.')
    parser.add_argument('--gui', type=str, help='graphical interface')
    args = parser.parse_args()

    if args.gui == "gtk":
        main_window = GtkMainWindow()
    else:
        # gui 'tk'
        main_window = TkMainWindow()
        main_window.mainloop()