
import sys

import tkinter as tk
import tkinter.ttk as ttk
from utility import Logger, debugger
from database import Database
from forms import Form

class SetupBusinessForm(Form):
    '''
    Create the form for the Business tab under Setup.
    '''

    def __init__(self, notebook):
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)
        super().__init__(notebook, notebook.BUSINESS_FRAME, 'Business')

        self.add_title('Business Setup Form')
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

class SetupCustomersForm(Form):

    def __init__(self, notebook):
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)
        super().__init__(notebook, notebook.CUSTOMERS_FRAME, 'Customer')

        self.add_title('Customers Setup Form')
        self.add_dynamic_label('Date', 'date_created', width=20)
        self.add_entry('Name', 'name', str)
        self.add_entry('Address1', 'address1', str)
        self.add_entry('Address2', 'address2', str)

        self.add_entry('City', 'city', str, inc_row=False, span=1, width=20)
        self.add_entry('State', 'state', str, width=20, span=1)

        self.add_entry('Zip Code', 'zip', str, width=20, span=1, inc_row=False)
        self.add_combo('Country', 'Country', 'country_ID', width=20)

        self.add_entry('Email', 'email_address', str, width=20, span=1, inc_row=False)
        self.add_combo('Email Status', 'EmailStatus', 'email_status_ID', width=20)

        self.add_entry('Phone', 'phone_number', str, width=20, span=1, inc_row=False)
        self.add_combo('Phone Status', 'PhoneStatus', 'phone_status_ID', width=20)

        self.add_entry('Web Site', 'web_site', str, width=20, inc_row=False)
        self.add_combo('Class', 'ContactClass', 'class_ID', width=20)

        self.add_entry('Description', 'description', str)

        self.add_text('Notes', 'notes', height=10)

        self.add_button('Prev')
        self.add_button('Next')
        self.add_button('Select')
        self.add_button('New')
        self.add_button('Save')
        self.add_button('Delete')

class SetupVendorsForm(Form):

    def __init__(self, notebook):
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)
        super().__init__(notebook, notebook.VENDORS_FRAME, 'Vendor')

        self.add_title('Vendors Setup Form')
        self.add_dynamic_label('Date', 'date_created', width=20)
        self.add_entry('Name', 'name', str)
        self.add_entry('Contact', 'contact_name', str)
        self.add_entry('Description', 'description', str)

        self.add_entry('Email', 'email_address', str, width=20, span=1, inc_row=False)
        self.add_combo('Email Status', 'EmailStatus', 'email_status_ID', width=20)

        self.add_entry('Phone', 'phone_number', str, width=20, span=1, inc_row=False)
        self.add_combo('Phone Status', 'PhoneStatus', 'phone_status_ID', width=20)

        self.add_entry('Web Site', 'web_site', str, width=20, inc_row=False)
        self.add_combo('Class', 'ContactClass', 'type_ID', width=20)

        self.add_text('Notes', 'notes', height=10)

        self.add_button('Prev')
        self.add_button('Next')
        self.add_button('Select')
        self.add_button('New')
        self.add_button('Save')
        self.add_button('Delete')

class SetupAccountsForm(Form):

    def __init__(self, notebook):
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)
        super().__init__(notebook, notebook.ACCOUNTS_FRAME, 'Account')

        self.add_title('Accounts Setup Form')
        self.add_entry('Name', 'name', str, width=20)
        self.add_entry('Number', 'number', str, width=20)
        self.add_combo('Type', 'AccountTypes', 'type_ID', width=20)
        self.add_entry('Total', 'total', float, width=20)
        self.add_entry('Description', 'description', str)
        self.add_text('Notes', 'notes', height=10)

        self.add_button('Prev')
        self.add_button('Next')
        self.add_button('Select')
        self.add_button('New')
        self.add_button('Save')
        self.add_button('Delete')

class SetupInventoryForm(Form):

    def __init__(self, notebook):
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)
        super().__init__(notebook, notebook.INVENTORY_FRAME, 'InventoryItem')

        self.add_title('Inventory Setup Form')
        self.add_entry('Name', 'name', str, width=20)
        self.add_entry('Stock Num', 'stock_num', int, width=20)
        self.add_entry('Stock', 'num_stock', int, width=20)
        self.add_entry('Retail', 'retail', float, width=20)
        self.add_entry('Wholesale', 'wholesale', float, width=20)
        self.add_entry('Description', 'description', str)
        self.add_text('Notes', 'notes', height=10)

        self.add_button('Prev')
        self.add_button('Next')
        self.add_button('Select')
        self.add_button('New')
        self.add_button('Save')
        self.add_button('Delete')

class supplimental_form(Form):

    INDIRECT_LABEL = Form.CUSTOM+1
    COMMIT_BTN = Form.CUSTOM+2

    def __init__(self, notebook, index, table):
        super().__init__(notebook, index, table)

    @debugger
    def add_indirect_label(self, name, local_col, table, indir_col, inc_row=True, **kwargs):
        '''
        This is stored as an ID in the database. This widget supports getting that ID and converting
        it into the table entry that it represents.

        name = The display name
        local_col = The column where the ID is stored.
        table = The table to find the displayed value in.
        indir_col = The column in the forign table where the value is.
        '''
        lab = tk.Label(self.ctl_frame, text=name+':')

        value = tk.StringVar(self.ctl_frame)
        val = tk.Label(self.ctl_frame, textvariable=value, **kwargs)

        lab.grid(row=self.row, column=self.col, padx=self.padx, pady=self.pady, sticky=tk.E)
        self.col += 1
        val.grid(row=self.row, column=self.col, padx=self.padx, pady=self.pady, sticky=tk.W)

        if inc_row:
            self.row += 1
            self.col = 0
        else:
            self.col += 1

        def getter():
            pass

        def setter(s):
            # The 's' parameter is what is read from the data base, which will be an int.
            val = self.data.get_single_value(table, indir_col, s)
            value.set(str(val))

        def clear(self):
            pass

        self.controls[name] = {'column': local_col,
                               'table': table,
                               'ind_col': indir_col,
                               'obj':lab,
                               'get':getter,
                               'set':lambda s: setter(s),
                               'clear':clear,
                               'kind':self.INDIRECT_LABEL}

    @debugger
    def add_commit_btn(self):
        '''
        This is a special button that controls the "commit" field in the record. If the 'committed' column
        is not zero, then the button is disabled. When the button is pressed, then the 'committed' column
        is updated to be 1 and the button is disabled. The button cannot be enabled without changing the
        column in the database.

        This control depends on having the fields in the database having the names that are hard-coded
        into it.
        '''
        btn = tk.Button(self.btn_frame, text='Commit', command=self.commit_btn, width=self.btn_width)
        btn.pack(padx=self.btn_padx, pady=self.btn_pady, side=tk.TOP)
        self.btn_col += 1

        def getter():
            pass

        def setter(s):
            # The 's' parameter is what is read from the data base, which will be an int.
            val = self.data.get_single_value(self.table, 'committed', s)
            if val:
                btn.configure(state='disabled')

        def clear(self):
            pass

        self.controls['Commit'] = {'column': 'committed',
                               'obj':btn,
                               'get':getter,
                               'set':lambda s: setter(s),
                               'clear':clear,
                               'kind':self.COMMIT_BTN}

    @debugger
    def commit_btn(self):
        '''
        This is the commit button callback.
        '''
        self.logger.debug('Commit btn')
        self.controls['Commit']['obj'].configure(state='disabled')
        self.data.set_single_value(self.table, 'committed', self.row_list[self.row_index], 1)
        self.data.commit()

    @debugger
    def add_products_widget(self):
        '''
        This is a compound widget that lists the products that are currently instantiated for the
        sales field. This is stored using a "one to many" connector table. The products listed
        must already exist in the database.
        '''
        sale_id = self.row_list[self.row_index]
        print("sale ID= ", sale_id)
        lab = tk.Label(self.ctl_frame, text='Products:')
        wid = ProductWidget(self.ctl_frame, sale_id, bd=1, relief=tk.RIDGE)

        lab.grid(row=self.row, column=self.col, padx=self.padx, pady=self.pady, sticky=tk.E)
        self.col += 1
        wid.grid(row=self.row, column=self.col, padx=self.padx, pady=self.pady, sticky=tk.W)
        self.row += 1
        self.col = 0

        def getter(self):
            return wid.get()

        def setter(self, val=None):
            wid.populate()

        def clear(self):
            pass

        self.controls['Products'] = {'column': '',
                               'obj':wid,
                               'get':getter,
                               'set':lambda s: setter(s),
                               'clear':clear,
                               'kind':self.CUSTOM}

class ProductLine(tk.Frame):

    def __init__(self, owner, idx, prod_idx, quan, **kargs):
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)
        super().__init__(owner, **kargs)

        self.data = Database.get_instance()

        tk.Label(self, text=str(idx)).grid(row=0, column=0)
        self.spin_value = tk.StringVar(self)
        self.spin = tk.Spinbox(self, from_=1, to=99, width=3, textvariable=self.spin_value)
        self.combo = ttk.Combobox(self, width=50, state='readonly')
        self.spin.grid(row=0, column=1, padx=5, pady=5)
        self.combo.grid(row=0, column=2, padx=5, pady=5)

        self.populate()
        self.set({'quan':quan, 'value':prod_idx})


    @debugger
    def get(self):
        '''
        Returns a dict with the data in it.
        '''
        return {'quan': int(self.spin_value.get()), 'value': self.combo.current()+1}

    @debugger
    def set(self, data):
        '''
        Accepts a dict with the data in it.
        '''
        self.spin_value.set(str(data['quan']))
        self.combo.current(str(data['value']-1))

    @debugger
    def clear(self):
        self.spin_value.set(str(1))
        self.combo.current(str(-1))

    @debugger
    def populate(self):
        '''
        Populate the combo box with the list of products.
        '''
        lst = self.data.populate_list('InventoryItem', 'name')
        self.combo['values'] = lst

class ProductWidget(tk.Frame):

    def __init__(self, owner, sale_id, **kargs):
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)
        super().__init__(owner, **kargs)

        self.data = Database.get_instance()
        self.sale_id = sale_id
        self.product_list = []
        self.line_widgets = []

        self.btn_frame = tk.Frame(self)
        self.ctl_frame = tk.Frame(self)
        self.btn_frame.pack(side='bottom')
        self.ctl_frame.pack(side='top')

        self.add_btn = tk.Button(self.btn_frame, text='Add', width=8)
        self.sav_btn = tk.Button(self.btn_frame, text='Save', width=8)
        self.rst_btn = tk.Button(self.btn_frame, text='Reset', width=8)
        self.add_btn.pack(side='left')
        self.sav_btn.pack(side='left')
        self.rst_btn.pack(side='left')

        self.populate()

    @debugger
    def populate(self):
        '''
        Read all of the product IDs defined in the database, and place them in the widget.
        '''
        self.products_list = self.data.get_row_list_by_col('ProductList', 'sale_record_ID', self.sale_id)
        if not self.products_list is None:
            # add product line items
            #self.logger.debug("products list = %s"%(str(self.products_list)))
            for idx, item in enumerate(self.products_list):
                line = ProductLine(self.ctl_frame, idx+1, item['inventory_ID'], item['quantity'])
                line.grid(row=idx, column=0)
                self.line_widgets.append(line)
        else:
            # no products, just add a single line
            self.logger.debug("products list = no products associated with sale")
            line = ProductLine(self.ctl_frame, 1, 1, 1)
            line.grid(row=0, column=0)
            del self.line_widgets # destroy the list
            self.line_widgets = []

    @debugger
    def get(self):
        '''
        Return the contents of the widget as an array of dictionaries.
        '''
        retv = []
        for item in self.line_widgets:
            retv.append(item.get())

    @debugger
    def set(self):
        self.populate()

    @debugger
    def clear(self):
        pass

class SetupSalesForm(supplimental_form):

    def __init__(self, notebook):
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)
        super().__init__(notebook, notebook.SALES_FRAME, 'SaleRecord')

        self.add_title('Sales Setup Form')
        self.add_indirect_label('Customer', 'customer_ID', 'Customer', 'name')
        self.add_dynamic_label('Gross', 'gross', width=20)
        self.add_dynamic_label('Fees', 'fees', width=20)
        self.add_dynamic_label('Shipping', 'shipping', width=20)
        self.add_combo('Status', 'SaleStatus', 'status_ID', width=20)
        # TODO make the products widget and add it here
        self.add_products_widget()
        self.add_text('Notes', 'notes', height=10)

        self.add_button('Prev')
        self.add_button('Next')
        self.add_button('Save')
        self.add_button('Delete')
        self.add_commit_btn()
        # TODO override the load and save forms to support products widget

class SetupPurchaseForm(supplimental_form):

    def __init__(self, notebook):
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)
        super().__init__(notebook, notebook.PURCHASE_FRAME, 'PurchaseRecord')

        self.add_title('Purchase Setup Form')
        self.add_indirect_label('Vendor', 'vendor_ID', 'Vendor', 'name')
        self.add_dynamic_label('Gross', 'gross', width=20)
        self.add_dynamic_label('Tax', 'tax', width=20)
        self.add_dynamic_label('Shipping', 'shipping', width=20)
        self.add_combo('Purchase Type', 'PurchaseType', 'type_ID', inc_row=False, width=20)
        self.add_combo('Purchase Status', 'PurchaseStatus', 'status_ID', width=20)
        self.add_text('Notes', 'notes', height=10)

        self.add_button('Prev')
        self.add_button('Next')
        self.add_button('Save')
        self.add_button('Delete')
        self.add_commit_btn()
