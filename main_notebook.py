import sys
import tkinter as tk

import tkinter.ttk as ttk
from utility import debugger, Logger
from notebook import Notebook
from setup_forms import *


class _notebook_base(Notebook):

    def __init__(self, master, names=None, height=700, width=1000):
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug("enter constructor")
        super().__init__(master, height=height, width=width)

        self.names = names
        if not names is None:
            for name in self.names:
                self.add_tab(name)

        self.form_class = []

    @debugger
    def get_name(self, index):
        return self.names[index]

    @debugger
    def get_index(self, name):
        for index, item in enumerate(self.names):
            if item == name:
                return index

        return None

    @debugger
    def get_form_class(self, index):
        return self.form_class[index]

    @debugger
    def set_form(self, index, form_class, *args, **kargs):
        idx = 0
        if type(index) == type(''):
            idx = self.get_name()
        elif type(index) == type(0):
            idx = index

        self.form_class.append(form_class(self.get_frame(idx), *args, **kargs))
        return self.form_class[-1]

class MainNotebook(_notebook_base):

    HOME_FRAME = 0
    SALES_FRAME = 1
    PURCHASE_FRAME = 2
    REPORTS_FRAME = 3
    SETUP_FRAME = 4

    def __init__(self, master):
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)
        super().__init__(master)

        self.add_tab('Home')
        self.add_tab('Sales')
        self.add_tab('Purchase')
        self.add_tab('Reports')
        self.add_tab('Setup')

class SetupNotebook(_notebook_base):

    BUSINESS_FRAME = 0
    CUSTOMERS_FRAME = 1
    VENDORS_FRAME = 2
    ACCOUNTS_FRAME = 3
    INVENTORY_FRAME = 4
    SALES_FRAME = 5
    PURCHASE_FRAME = 6
    IMPORT_FRAME = 7

    def __init__(self, master):
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)
        super().__init__(master, ['Business', 'Customers', 'Vendors', 'Accounts',
                                  'Inventory', 'Sales', 'Purchase', 'Import'])

        SetupBusinessForm(self)
        SetupCustomersForm(self)
        SetupVendorsForm(self)
        SetupAccountsForm(self)
        SetupInventoryForm(self)
        SetupSalesForm(self)
        SetupPurchaseForm(self)
