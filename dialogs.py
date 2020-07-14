
from tkinter import ttk
import tkinter as tk
import math
from utility import Logger, debugger


# see: https://effbot.org/tkinterbook/tkinter-dialog-windows.htm
class BaseDialog(tk.Toplevel):
    '''
    This class provides common services to simple data dialogs.
    '''

    def __init__(self, parent):# , title = None):

        #init the logger
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug("Base Dialog start constructor")

        tk.Toplevel.__init__(self, parent)
        self.transient(parent)

        self.parent = parent

        self.result = None
        # get a copy of the data_store for the children

        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.grid(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.initial_focus.focus_set()

        #self.wait_window(self)
        self.logger.debug("Base Dialog leave constructor")

    #
    # construction hooks
    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        return self

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons
        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        box.grid()

    #
    # standard button semantics
    @debugger
    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    @debugger
    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks
    def validate(self):
        return True # override

    def apply(self):
        pass # override


class SelectItem(BaseDialog):
    '''
    Create a list of items called 'name' from a table and return the database
    ID of the item in item_id.
    '''

    def __init__(self, master, table, thing=None):

        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug('SelectItem enter constructor')
        self.table = table
        if thing is None:
            self.thing = 'Item'
        else:
            self.thing = thing

        self.item_id = -1
        super().__init__(master)
        self.wait_window(self)
        self.logger.debug('SelectItem leave constructor')

    @debugger
    def body(self, master):
        self.title("Select %s"%(self.thing))
        self.data = Database.get_instance()

        padx = 6
        pady = 2

        frame = tk.Frame(master, bd=1, relief=tk.RIDGE)
        frame.grid(row=0, column=0, padx=4, pady=7)
        tk.Label(frame, text="Select %s"%(self.thing), font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2)

        ######################
        # Populate the combo boxes
        lst = self.data.populate_list(self.table, 'name')
        lst.sort()

        ######################
        # Show the boxes
        tk.Label(frame, text='Name:').grid(row=1, column=0)
        self.cbb = ttk.Combobox(frame, values=lst)
        self.cbb.grid(row=1, column=1, padx=padx, pady=pady)
        try:
            self.cbb.current(0)
        except tk.TclError:
            mb.showerror("TCL ERROR", "No records are available to select for this table.")

    @debugger
    def validate(self):
        # Since the name was selected from the list, there is no need to
        # validate.
        return True

    @debugger
    def apply(self):
        ''' Populate the form with the selected data. '''
        id = self.data.get_id_by_name(self.table, self.cbb.get())
        self.item_id = id

###############################################################################
# Does not use BaseDialog
class helpDialog:

    def __init__(self, parent):
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug("enter constructor")

        self.top = tk.Toplevel(parent)
        self.tx = tk.Text(self.top, height=25, width=80)
        self.sb = tk.Scrollbar(self.top)
        self.sb.pack(side=tk.RIGHT,fill=tk.Y)
        self.tx.pack(side=tk.LEFT)
        self.sb.config(command=self.tx.yview)
        self.tx.config(yscrollcommand=self.sb.set)
        self.tx.insert(tk.END, help_text)
        self.tx.config(state='disabled')

        self.logger.debug("leave constructor")
