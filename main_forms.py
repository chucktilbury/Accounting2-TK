
import sys
import tkinter as tk
import tkinter.ttk as ttk
from utility import Logger, debugger
from forms import Form
from setup_notebook import SetupNotebook

class MainHomeForm(Form):
    '''
    Create the form for the Business tab under Setup.
    '''

    def __init__(self, notebook):
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)
        super().__init__(notebook, notebook.HOME_FRAME, 'Business')

        self.add_title('Home Form')
        self.add_entry('Name', 'name', str)
        self.add_entry('Address1', 'address1', str)
        self.add_entry('Address2', 'address2', str)

        self.add_entry('City', 'city', str, inc_row=False, span=1, width=20)
        self.add_entry('State', 'state', str, width=20, span=1)

        self.add_entry('Zip Code', 'zip', str, width=20, span=1, inc_row=False)
        self.add_entry('Country', 'country', str, width=20, span=1)

        self.add_entry('Email', 'email_address', str, width=20, span=1, inc_row=False)
        self.add_entry('Phone', 'phone_number', str, width=20, span=1)

        self.add_entry('Web Site', 'web_site', str)
        self.add_entry('Description', 'description', str)

        self.add_text('Terms', 'terms')
        self.add_text('Returns', 'returns')
        self.add_text('Warranty', 'warranty')
        self.add_button('Save')

class MainSalesForm(Form):
    '''
    Create the form for the Business tab under Setup.
    '''

    def __init__(self, notebook):
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)
        super().__init__(notebook, notebook.SALES_FRAME, 'Business')

        self.add_title('Sales Form')

class MainPurchaseForm(Form):
    '''
    Create the form for the Business tab under Setup.
    '''

    def __init__(self, notebook):
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)
        super().__init__(notebook, notebook.PURCHASE_FRAME, 'Business')

        self.add_title('Purchases Form')

class MainReportsForm(Form):
    '''
    Create the form for the Business tab under Setup.
    '''

    def __init__(self, notebook):
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)
        super().__init__(notebook, notebook.REPORTS_FRAME, 'Business')

        self.add_title('Reports Form')

class MainSetupForm(Form):
    '''
    Create the form for the Business tab under Setup.
    '''

    def __init__(self, notebook):
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)
        super().__init__(notebook, notebook.SETUP_FRAME, 'Business')

        self.add_notebook(SetupNotebook)
