#!/usr/bin/python

import argparse

from sockgen.gui.gtk_main_window import *
from sockgen.gui.tkinter_main_window import *

if __name__ == '__main__':  
    parser = argparse.ArgumentParser(description='Generate a message from a XML file.')
    parser.add_argument('--gui', type=str, help='graphical interface')
    parser.add_argument('--generate', help='generate project')
    parser.add_argument('--output', type=str, help='file to generate')
    args = parser.parse_args()

    try:
        if args.gui == "gtk":
            main_window = GtkMainWindow()
        else:
            # gui 'tk'
            main_window = TkMainWindow()
            main_window.mainloop()
    except KeyboardInterrupt:
      print('An exception occurred')
      exit(1)