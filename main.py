#!/usr/bin/env python3
import sys, traceback

import tkinter as tk
import tkinter.ttk as ttk
from utility import Logger, debugger
from main_notebook import *



class MainFrame(tk.Frame):
    '''
    Entry point of application.
    '''

    def __init__(self):
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)

        self.master = tk.Tk()
        self.master.wm_title("Accounting")

        self.main_notebook = MainNotebook(self.master)
        self.setup_nb = self.main_notebook.set_form(self.main_notebook.SETUP_FRAME, SetupNotebook)


        self.main_notebook.show_frame(self.main_notebook.HOME_FRAME)
        self.setup_nb.show_frame(self.setup_nb.SALES_FRAME)

    @debugger
    def main(self):
        try:
            self.logger.debug("start main loop")
            self.master.mainloop()
            self.logger.debug('close database')
            #self.data.close()
            self.logger.debug("end main loop")

        except Exception:
            traceback.print_exception(*sys.exc_info())

if __name__ == "__main__":
    MainFrame().main()

