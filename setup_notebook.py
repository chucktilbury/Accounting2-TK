
from notebook import NotebookBase
from utility import Logger, debugger
from setup_forms import *

class SetupNotebook(NotebookBase):

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
        SetupImportForm(self)

        self.show_frame(self.BUSINESS_FRAME)
