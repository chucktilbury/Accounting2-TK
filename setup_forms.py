
import sys

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror, showinfo, askyesno
from utility import Logger, debugger
from database import Database
from forms import Form
from custom_widgets import *
from importer import ImportPayPal


class supplimental_form(Form):


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
            return self.data.get_single_value(self.table, local_col, self.row_list[self.row_index])


        def setter(row_id):
            # The 's' parameter is what is read from the data base, which will be an int.
            val = self.data.get_single_value(table, indir_col, row_id)
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
        #btn.pack(padx=self.btn_padx, pady=self.btn_pady, side=tk.TOP)
        btn.grid(row = self.btn_row, column=0, padx=self.btn_padx, pady=self.btn_pady)
        self.btn_row += 1

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
        if len(self.row_list) > 0:
            sale_id = self.row_list[self.row_index]
        else:
            sale_id = -1

        print("sale ID= ", sale_id)
        lab = tk.Label(self.ctl_frame, text='Products:')
        wid = ProductWidget(self.ctl_frame, sale_id, bd=1, relief=tk.RIDGE)

        lab.grid(row=self.row, column=self.col, padx=self.padx, pady=self.pady, sticky=tk.E)
        self.col += 1
        wid.grid(row=self.row, column=self.col, padx=self.padx, pady=self.pady, sticky=tk.W)
        self.row += 1
        self.col = 0

        def getter():
            return wid.get()

        def setter(sale_id):
            wid.set(sale_id)

        def clear():
            pass

        self.controls['Products'] = {'column': None,
                               'obj':wid,
                               'get':getter,
                               'set':lambda s: setter(s),
                               'clear':clear,
                               'kind':self.PRODUCT}

    @debugger
    def add_dir_browser(self, **kw):
        '''
        Add a file system browser widget to the form.
        '''
        lab = tk.Label(self.ctl_frame, text='Select File:')
        wid = DirectoryBrowser(self.ctl_frame, **kw)

        lab.grid(row=self.row, column=self.col, padx=self.padx, pady=self.pady, sticky=tk.E)
        self.col += 1
        wid.grid(row=self.row, column=self.col, padx=self.padx, pady=self.pady, sticky=tk.W)
        self.row += 1
        self.col = 0

        def getter():
            return wid.file_name

        def setter():
            pass #wid.set(sale_id)

        def clear():
            pass

        self.controls['dir_browser'] = {'column': None,
                               'obj':wid,
                               'get':getter,
                               'set':setter,
                               'clear':clear,
                               'kind':self.DIR_BROWSER}

    @debugger
    def add_import_btn(self):
        '''
        '''
        btn = tk.Button(self.btn_frame, text='Import', command=self.import_btn, width=self.btn_width)
        #btn.pack(padx=self.btn_padx, pady=self.btn_pady, side=tk.TOP)
        btn.grid(row = self.btn_row, column=0, padx=self.btn_padx, pady=self.btn_pady)
        self.btn_row += 1

        def getter():
            pass

        def setter():
            pass

        def clear():
            pass

        self.controls['Commit'] = {'column': 'committed',
                               'obj':btn,
                               'get':getter,
                               'set':setter,
                               'clear':clear,
                               'kind':self.IMPORT_BTN}

    @debugger
    def import_btn(self):
        '''
        This is the import button callback.
        '''
        self.logger.debug('Import btn')
        fname = self.controls['dir_browser']['get']()
        if fname == '':
            showerror('Error', 'Please select a file instead of a directory')
        elif askyesno('Confirm Import', 'You are importing the file\n%s\nConfirm?'%(fname)):
            self.logger.debug('Importing file: %s'%(fname))
            importer = ImportPayPal(fname)
            importer.import_all()


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

    @debugger
    def save_callback(self):
        self.logger.debug('supplimental form save callback')
        if askyesno('Save record?', 'Are you sure you want to save this?'):
            self.commit_form()
            self.controls['Products']['obj'].save_btn()
            self.data.commit()

    @debugger
    def delete_callback(self):
        self.logger.debug('supplimental form delete callback')
        if askyesno('Delete record?', 'Are you sure you want to delete this?'):
            self.data.delete_row(self.table, self.row_list[self.row_index])
            self.data.delete_where('ProductList', 'sale_record_ID=%d'%(self.controls['Products']['obj'].sale_id))
            self.row_list = self.data.get_id_list(self.table)
            self.load_form()
            self.data.commit()

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

class SetupImportForm(supplimental_form):

    def __init__(self, notebook):
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)
        super().__init__(notebook, notebook.IMPORT_FRAME, 'RawImport')

        self.add_title('Import Setup Form')
        self.add_dir_browser()
        self.add_import_btn()
