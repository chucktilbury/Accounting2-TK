

from notebook import NotebookBase
from utility import Logger, debugger
from main_forms import *

class MainNotebook(NotebookBase):

    HOME_FRAME = 0
    SALES_FRAME = 1
    PURCHASE_FRAME = 2
    REPORTS_FRAME = 3
    SETUP_FRAME = 4

    def __init__(self, master):
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)
        super().__init__(master, ['Home', 'Sales', 'Purchase', 'Reports', 'Setup'])

        MainHomeForm(self)
        MainSalesForm(self)
        MainPurchaseForm(self)
        MainReportsForm(self)
        MainSetupForm(self)

        self.show_frame(self.HOME_FRAME)
