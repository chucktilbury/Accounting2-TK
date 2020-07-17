
import sys, os, time
import tkinter as tk
import tkinter.ttk as ttk
from database import Database
from utility import Logger, debugger

class DirectoryBrowser(tk.Frame):

    KB = 1024.0
    MB = KB * KB
    GB = MB * KB

    def __init__(self, master, **kw):
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)

        super().__init__(master, **kw)
        self.grid()
        #self.isapp = isapp
        self.file_name = ''

        demoPanel = tk.Frame(self)
        demoPanel.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.Y)

        self._create_treeview(demoPanel)
        self._populate_root()

    def _create_treeview(self, parent):
        f = ttk.Frame(parent)
        #f.pack(side=TOP, fill=BOTH, expand=Y)
        f.grid()

        # create the tree and scrollbars
        self.dataCols = ('fullpath', 'type', 'date', 'size')
        self.tree = ttk.Treeview(columns=self.dataCols,
                                 displaycolumns=('date', 'size'))

        ysb = ttk.Scrollbar(orient=tk.VERTICAL, command= self.tree.yview)
        xsb = ttk.Scrollbar(orient=tk.HORIZONTAL, command= self.tree.xview)
        self.tree['yscroll'] = ysb.set
        self.tree['xscroll'] = xsb.set

        # setup column headings
        self.tree.heading('#0', text='Directory Structure', anchor=tk.W)
        self.tree.heading('size', text=' File Size ', anchor=tk.W)
        self.tree.heading('date', text=' File Date ', anchor=tk.W)
        self.tree.column('size', stretch=0, width=90)
        self.tree.column('date', stretch=0, width=160)
        self.tree.column('#0', stretch=0, width=400)

        # add tree and scrollbars to frame
        self.tree.grid(in_=f, row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        ysb.grid(in_=f, row=0, column=1, sticky=(tk.N, tk.S))
        xsb.grid(in_=f, row=1, column=0, sticky=(tk.E, tk.W))

        # set frame resizing priorities
        f.rowconfigure(0, weight=1)
        f.columnconfigure(0, weight=1)

        # action to perform when a node is expanded
        self.tree.bind('<<TreeviewOpen>>', self._update_tree)
        self.tree.bind('<<TreeviewSelect>>', self._update_tree)

    def _populate_root(self):
        # use current directory as root node
        self.path = os.getcwd()

        # insert current directory at top of tree
        # 'values' = column values: fullpath, type, size
        #            if a column value is omitted, assumed empty
        parent = self.tree.insert('', tk.END, text=self.path,
                                  values=[self.path, 'directory'])

        # add the files and sub-directories
        self._populate_tree(parent, self.path, os.listdir(self.path))

    def _populate_tree(self, parent, fullpath, children):
        # parent   - id of node acting as parent
        # fullpath - the parent node's full path
        # children - list of files and sub-directories
        #            belonging to the 'parent' node

        for child in children:
            # build child's fullpath
            cpath = os.path.join(fullpath, child).replace('\\', '/')

            if os.path.isdir(cpath):
                # directory - only populate when expanded
                # (see _create_treeview() 'bind')
                cid =self.tree.insert(parent, tk.END, text=child,
                                      values=[cpath, 'directory'])

                # add 'dummy' child to force node as expandable
                self.tree.insert(cid, tk.END, text='dummy')
            else:
                # must be a 'file'
                size = self._format_size(os.stat(cpath).st_size)
                date = time.strftime('%m/%d/%Y %H:%M', time.localtime(os.stat(cpath).st_mtime))
                self.tree.insert(parent, tk.END, text=child,
                                 values=[cpath, 'file', date, size])

    def _format_size(self, size):
        if size >= self.GB:
            return '{:,.1f} GB'.format(size/self.GB)
        if size >= self.MB:
            return '{:,.1f} MB'.format(size/self.MB)
        if size >= self.KB:
            return '{:,.1f} KB'.format(size/self.KB)
        return '{} bytes'.format(size)

    def _update_tree(self, event): #@UnusedVariable
        # user expanded a node - build the related directory
        nodeId = self.tree.focus()      # the id of the expanded node
        if self.tree.parent(nodeId):    # not at root
            x = self.tree.get_children(nodeId)
            if len(x) > 0:
                topChild = x[0]
                self.file_name = ''

                # if the node only has a 'dummy' child, remove it and
                # build new directory; skip if the node is already
                # populated
                if self.tree.item(topChild, option='text') == 'dummy':
                    self.tree.delete(topChild)
                    path = self.tree.set(nodeId, 'fullpath')
                    self._populate_tree(nodeId, path, os.listdir(path))
            else:
                self.file_name = path = self.tree.set(nodeId, 'fullpath')
                self.logger.debug("select file: " + self.file_name)


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
        self.combo.current(str(1))

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

        self.add_btn = tk.Button(self.btn_frame, text='Add', command=self.add_btn, width=8)
        self.sav_btn = tk.Button(self.btn_frame, text='Save', command=self.save_btn, width=8)
        self.rst_btn = tk.Button(self.btn_frame, text='Reset', command=self.reset_btn, width=8)
        self.add_btn.pack(side='left')
        self.sav_btn.pack(side='left')
        self.rst_btn.pack(side='left')

        self.get_prod_list()
        self.populate()

    @debugger
    def get_prod_list(self):

        self.products_list = self.data.get_row_list_by_col('ProductList', 'sale_record_ID', self.sale_id)
        if not self.products_list is None:
            for idx, item in enumerate(self.products_list):
                line = ProductLine(self.ctl_frame, idx+1, item['inventory_ID'], item['quantity'])
                self.line_widgets.append(line)
        else:
            line = ProductLine(self.ctl_frame, 1, 1, 1)
            self.line_widgets.append(line)

    @debugger
    def populate(self):
        '''
        Read all of the product IDs defined in the database, and place them in the widget.
        self.products_list = self.data.get_row_list_by_col('ProductList', 'sale_record_ID', self.sale_id)
        '''
        for idx, item in enumerate(self.line_widgets):
            if item.get()['quan'] > 0:
                item.grid(row=idx, column=0)

    @debugger
    def forget(self):
        for idx, item in enumerate(self.line_widgets):
            item.grid_forget()

    @debugger
    def get(self):
        '''
        Return the contents of the widget as an array of dictionaries.
        '''
        retv = []
        for item in self.line_widgets:
            retv.append(item.get())

    @debugger
    def set(self, sale_id):
        self.sale_id = sale_id
        self.forget()
        del self.line_widgets
        self.line_widgets = []
        self.get_prod_list()
        self.populate()

    @debugger
    def clear(self):
        pass

    @debugger
    def add_btn(self):
        self.forget()
        line = ProductLine(self.ctl_frame, 1, 1, 1)
        self.line_widgets.append(line)
        self.populate()


    @debugger
    def save_btn(self):
        # delete the currently existing records
        self.data.delete_where('ProductList', 'sale_record_ID=%d'%(self.sale_id))
        for item in self.line_widgets:
            val = item.get()
            if val['quan'] > 0:
                self.data.insert_row('ProductList', {'sale_record_ID':self.sale_id,
                                                    'inventory_ID':val['value'],
                                                    'quantity':val['quan']})
        # TODO: If there are 2 or more items with the same inventory ID, add the
        # quantities together instead of saving two database rows.
        self.data.commit()
        self.forget()
        self.populate()

    @debugger
    def reset_btn(self):
        self.forget()
        del self.line_widgets
        self.line_widgets = []
        line = ProductLine(self.ctl_frame, 1, 1, 1)
        self.line_widgets.append(line)
        self.populate()
