
import tkinter as tk
from tkinter.messagebox import showerror, showinfo, askyesno
import tkinter.ttk as ttk
from utility import debugger, Logger
from database import Database

class ScrollableFrame:
    '''
    This is the scrollable frame class that is used by the notebook class. It
    could be used generically, but it was designed for use here.

    The scrolling functionality supports both a scroll bar as well as the
    mouse wheel.
    '''

    def __init__(self, container, height=700, width=800, *args, **kwargs):

        self.logger = Logger(self, level=Logger.INFO)
        self.logger.debug("enter constructor")

        self.canvas = tk.Canvas(container, height=height, width=width)
        self.scrollwindow = tk.Frame(self.canvas)

        self.canvas.create_window((0, 0), window=self.scrollwindow, anchor="nw")
        self.canvas.pack(side="right", fill="both", expand=True)

        scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.configure(yscrollincrement='20')
        scrollbar.pack(side="right", fill="y")

        self.scrollwindow.bind("<Configure>", self.configure_window)
        self.scrollwindow.bind("<Enter>", self.enter_handler)
        self.scrollwindow.bind("<Leave>", self.leave_handler)
        self.scrollwindow.bind('<Button-4>', self.mouse_wheel)
        self.scrollwindow.bind('<Button-5>', self.mouse_wheel)

        self.canvas.focus_set()
        self.logger.debug("leave constructor")

    def get_frame(self):
        ''' Get the master frame for embedded widgets. '''
        #print('here')
        return self.scrollwindow

    # PORTABILITY! This may not be the same on every platform. It works under
    # linux using xfce. Other must be tested. The problem that this solves is
    # that mousewheel events are only routed to the widget that the mouse is
    # pointing to. If the mouse is hovering over a label or something, the
    # canvas never gets the event. Surprisingly, the enter and leave events
    # are both sent when the mousewheel is rolled. I am sure that this is an
    # "unsupported" feature. If the mousewheel stops working, this is where
    # to look for a fix.
    def enter_handler(self, event):
        #print('enter', event.state)
        state = (event.state & 0x1800) >> 11
        direction = 0
        if state == 2:
            direction = 1
        if state == 1:
            direction = -1
        #print(direction)
        self.canvas.yview_scroll(direction, tk.UNITS)

    def leave_handler(self, event):
        #print('leave', event.state)
        pass

    def configure_window(self, event):
        #print('here', self.mark)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def mouse_wheel(self, event):
        direction = 0
        if event.num == 5:
            direction = 1
        if event.num == 4:
            direction = -1
        #print(direction)
        self.canvas.yview_scroll(direction, tk.UNITS)

class Form: #(tk.Frame):
    '''
    Base class for a form. This contains everything needed to display a form and
    associate the elements of a form with a database record. This allows a complete
    form to be added to a notebook panel.

    A single generic driver routine is used to get or set the form with the database.

    The idea is to capture all of the calls to tkinter having to do with the forms.
    '''
    # widgets that may be added. Used internally to identify them.
    TITLE = 0
    ENTRY = 1
    TEXT = 2
    COMBO = 3
    LABEL = 4
    BUTTON = 5
    # used by the supplemental_form class in setup_forms.py
    INDIRECT_LABEL = 6
    COMMIT_BTN = 7
    PRODUCT = 8

    def __init__(self, notebook, index, table, height=700, width=1000, span=4):
        '''
        Create a form object. A form must be associated with exactly one database table. The form
        is filled in with exactly one row from the database table. If the form does not use all
        of the row, that is handled transparently.

        This class contains frames. It is not, itself, a frame.

        notebook = The notebook container
        index = The index of the tab to bind the form to
        table = The database table where the data from the form is located
        height = The height of the form in pixels
        width = the width of the form in pixels
        span = The number of columns in the form
        '''
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug("enter constructor")

        self.notebook = notebook # container for the form.
        self.nb_index = index # index of the tab to bind the form to
        self.table = table # database table to save and retrieve data

        # frame to bind the widgets to
        self.owner = self.notebook.get_frame(self.nb_index)
        # load_form should be over ridden to handle special cases.
        self.notebook.set_callback(self.nb_index, self.load_form)

        # database singleton object
        self.data = Database.get_instance()
        # the rows may not be sequentially numbered.
        self.row_list = self.data.get_id_list(self.table)
        self.row_index = 0

        # dict of dicts that lists all of the controls by name.
        self.controls = {}

        # actual height and width of the form frame.
        self.height = height
        self.width = width
        self.logger.debug("window size = %d, %d"%(self.height, self.width))

        # keep track of the current layout position.
        self.row = 0
        self.col = 0
        self.btn_col = 0
        self.btn_width = 10
        self.padx = 5
        self.pady = 5
        self.btn_padx = 1
        self.btn_pady = 1
        self.span = span # number of columns for controls
        self.ctrl_width = 60 # default control width in chars
        self.text_height = 20 # default text height

        # create the frames
        fr = tk.Frame(self.owner)
        #self.ctl_frame = ScrollableFrame(fr, height, width).get_frame()
        self.ctl_frame = ScrollableFrame(fr).get_frame()
        self.btn_frame = tk.Frame(fr)
        self.btn_frame.pack(side=tk.BOTTOM)
        fr.grid()

        self.logger.debug("leave constructor")

    @debugger
    def add_title(self, name):
        '''
        Add the form title. This is not a tracked item.
        '''
        lab = tk.Label(self.ctl_frame, text=name, font=("Helvetica", 14))
        lab.grid(row=0, column=0, padx=self.padx, pady=self.pady, columnspan=self.span, sticky=(tk.E, tk.W))
        self.row += 1

    @debugger
    def add_entry(self, name, column, _type, inc_row=True, readonly=False, span=None, **kargs):
        '''
        Add an entry line to the form. The name is displayed as the label and is also used
        to access the control when reading it or writing to it.

        Kargs are passed directly to the widget constructor.

        name = The name to use to access the control object.
        column = Name of the database column.
        _type = The type of data stored in the database.
        inc_row = whether to increment the row after adding this line.
        '''
        if not 'width' in kargs:
            kargs['width'] = self.ctrl_width
        self.logger.debug("kargs = %s"%(str(kargs)))

        lab = tk.Label(self.ctl_frame, text=name+':')

        strvar = tk.StringVar(self.ctl_frame)
        item = tk.Entry(self.ctl_frame, textvariable=strvar, **kargs)
        if readonly:
            item.configure(state='readonly')

        lab.grid(row=self.row, column=self.col, padx=self.padx, pady=self.pady, sticky=tk.E)
        self.col += 1
        if span is None:
            span = self.span-1
        item.grid(row=self.row, column=self.col, padx=self.padx, pady=self.pady, columnspan=span, sticky=tk.W)

        if inc_row:
            self.row += 1
            self.col = 0
        else:
            self.col += 1

        def getter():
            return _type(strvar.get())

        def setter(s):
            state = item.configure()['state']
            if state == 'readonly':
                item.configure(state='normal')

            strvar.set(str(s))

            if state == 'readonly':
                item.configure(state='readonly')

        def clear():
            state = item.configure()['state']
            if state == 'readonly':
                item.configure(state='normal')

            strvar.set('')

            if state == 'readonly':
                item.configure(state='readonly')

        self.controls[name] = {'column': column,
                               'obj':item,
                               'get':getter,
                               'set':lambda s: setter(s),
                               'clear':clear,
                               'type':_type,
                               'kind':Form.ENTRY}

    @debugger
    def add_text(self, name, column, inc_row=True, **kargs):
        '''
        Add a multi-line text entry box with scroll bars to the form. The name is displayed
        as the label and is also used to access the control when reading it or writing to it.

        Kargs are passed directly to the widget constructor.

        name = The name of the widgit and the label text
        column = the column in the database to retrieve
        inc_row = whether to increment the row after adding the widget
        '''
        lab = tk.Label(self.ctl_frame, text=name+':')

        if not 'width' in kargs:
            kargs['width'] = self.ctrl_width

        if not 'height' in kargs:
            kargs['height'] = self.text_height

        self.logger.debug("kargs = %s"%(str(kargs)))

        frame = tk.Frame(self.ctl_frame, bd=1, relief=tk.RIDGE)
        text = tk.Text(frame, wrap=tk.NONE, **kargs)
        text.insert(tk.END, '')

        # see https://www.homeandlearn.uk/tkinter-scrollbars.html
        self.vsb = tk.Scrollbar(frame, orient=tk.VERTICAL)
        self.vsb.config(command=text.yview)
        text.config(yscrollcommand=self.vsb.set)
        self.vsb.pack(side=tk.RIGHT,fill=tk.Y)

        self.hsb = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        self.hsb.config(command=text.xview)
        text.config(xscrollcommand=self.hsb.set)
        self.hsb.pack(side=tk.BOTTOM,fill=tk.X)

        text.pack(side=tk.LEFT)

        lab.grid(row=self.row, column=self.col, padx=self.padx, pady=self.pady, sticky=tk.E)
        self.col += 1
        frame.grid(row=self.row, column=self.col, padx=self.padx, pady=self.pady, columnspan=self.span-1, sticky=tk.W)

        if inc_row:
            self.row += 1
            self.col = 0
        else:
            self.col += 1

        def getter():
            return text.get(1.0, tk.END)

        def setter(s):
            text.delete('1.0', tk.END)
            if not s is None:
                text.insert(tk.END, str(s))

        def clear():
            text.delete('1.0', tk.END)

        self.controls[name] = {'column': column,
                               'obj':text,
                               'get':getter,
                               'set':lambda s: setter(s),
                               'clear':clear,
                               'kind':Form.TEXT}

    @debugger
    def add_combo(self, name, table, column, inc_row=True, **kargs):
        '''
        Add a combo box line to the form. The name is displayed as the label and is also used
        to access the control when reading it or writing to it. Combo boxes use a different table
        to store their data in. This widgit automatically retrieves that data when it is displayed.

        The type is always strings.

        Kargs are passed directly to the widget constructor.

        name = the name of the row and the label text
        table = the name of the table to retrieve the data for the combo box
        column = the name of the column to retrieve the value to set the box to
        inc_row = whether to increment the row after adding the widget
        '''

        lab = tk.Label(self.ctl_frame, text=name+':')

        if not 'width' in kargs:
            kargs['width'] = self.ctrl_width

        # Note that the method that displays the frame has to populate this.
        combo = ttk.Combobox(self.ctl_frame, state='readonly', **kargs)

        lab.grid(row=self.row, column=self.col, padx=self.padx, pady=self.pady, sticky=tk.E)
        self.col += 1
        combo.grid(row=self.row, column=self.col, padx=self.padx, pady=self.pady, sticky=tk.W)

        if inc_row:
            self.row += 1
            self.col = 0
        else:
            self.col += 1

        def getter():
            return combo.current()+1

        def setter(s):
            combo.current(int(s)-1)

        def clear():
            try:
                combo.current(0)
            except tk.TclError:
                pass # empty content is not an error

        def populate():
            combo['values'] = self.data.populate_list(table, 'name')

        self.controls[name] = {'column': column,
                               'table': table,
                               'obj':combo,
                               'get':getter,
                               'set':lambda s: setter(s),
                               'clear':clear,
                               'populate':populate,
                               'kind':Form.COMBO}

    @debugger
    def add_dynamic_label(self, name, column, inc_row=True, **kargs):
        '''
        Add a label that can be changed according to a database column.
        '''
        lab = tk.Label(self.ctl_frame, text=name+':')

        value = tk.StringVar(self.ctl_frame)
        val = tk.Label(self.ctl_frame, textvariable=value, **kargs)

        lab.grid(row=self.row, column=self.col, padx=self.padx, pady=self.pady, sticky=tk.E)
        self.col += 1
        val.grid(row=self.row, column=self.col, padx=self.padx, pady=self.pady, sticky=tk.W)

        if inc_row:
            self.row += 1
            self.col = 0
        else:
            self.col += 1

        def getter():
            return value.get()

        def setter(s):
            value.set(str(s))

        def clear():
            value.set('')

        self.controls[name] = {'column': column,
                               'obj':lab,
                               'get':getter,
                               'set':lambda s: setter(s),
                               'clear':clear,
                               'kind':Form.LABEL}

    @debugger
    def add_button(self, name, command=None, **kargs):
        '''
        Add a button to the button line on the form. The name is used as the label on the
        button. If a callback is not provided, then a default callback will be run. Buttons are
        added in the order they are created and arranged accroding default patterns.

        Args and kargs are passed directly to the widget constructor.
        '''
        if command is None:
            if name == "Next":
                command = self.next_callback
            elif name == "Prev":
                command = self.prev_callback
            elif name == "Select":
                command = self.select_callback
            elif name == "New":
                command = self.new_callback
            elif name == "Save":
                command = self.save_callback
            elif name == "Delete":
                command = self.delete_callback
            else:
                raise "unknown name and no command to exec"

        btn = tk.Button(self.btn_frame, text=name, command=command, width=self.btn_width, **kargs)
        btn.pack(padx=self.btn_padx, pady=self.btn_pady, side=tk.TOP)
        self.btn_col += 1

    @debugger
    def get_form(self):
        '''
        Return a dictionary of all of the values that are currently in the form. Form fields are
        returned in the type that will be stored in the database.
        '''
        values = {}
        for item in self.controls:
            values[item] = self.get_form_field(item)
        return values

    @debugger
    def set_form(self, values):
        '''
        Accept a dictionary of all of the values for the form and make them visible. If a
        form field is different from the type that will be stored in the database, then the
        value will be changed to the correct type.
        '''
        for item in values:
            self.set_form_field(item, values[item])

    @debugger
    def clear_form(self):
        '''
        Clear the form with blank/default values.
        '''
        for item in self.controls:
            self.clear_form_field(item)

    @debugger
    def get_form_field(self, name):
        '''
        Return the contents of a form field in the type that the form stores. If the database
        has stored an int, then an int is returned, rather than a string. If the field is a
        combo box, then setting the values is expected to be an array of text to populate the
        control.
        '''
        return self.controls[name]['get']()

    @debugger
    def set_form_field(self, name, value):
        '''
        Set the value of the field according to the type that the field stores. The type will
        be automatically converted from a string, if the type to be stored in the is different.
        '''
        self.controls[name]['set'](value)

    @debugger
    def clear_form_field(self, name):
        '''
        Clear the form field to the default value.
        '''
        self.controls[name]['clear']()

    @debugger
    def commit_form(self):
        '''
        Write the contents of the form to the database. The form does not need to be
        visible for this to take place. Nothing is written to the database until this method
        is called. This assumes that all of the data is in the same table.
        '''
        vals = {}
        row_id = self.row_list[self.row_index]
        for item in self.controls:
            cval = self.controls[item]['get']()
            col = self.controls[item]['column']
            if not cval is None and col != '':
                vals[col] = cval
        if self.data.if_rec_exists(self.table, 'ID', row_id):
            self.data.update_row(self.table, vals, "ID=%d"%(row_id))
        else:
            self.data.insert_row(self.table, vals)

        self.data.commit()
        self.row_list = self.data.get_id_list(self.table)


    @debugger
    def load_form(self):
        '''
        Read the contents of the form from the database and place the values in the
        form controls. If the form is currently visible, then display the values.
        '''
        try:
            row_id = self.row_list[self.row_index]
            row = self.data.get_row_by_id(self.table, row_id)

            for item in self.controls:
                if self.controls[item]['kind'] == Form.COMBO:
                    self.controls[item]['populate']()
                    self.controls[item]['set'](row[self.controls[item]['column']])
                elif self.controls[item]['kind'] == Form.PRODUCT:
                    self.controls[item]['set'](row_id)
                else:
                    self.controls[item]['set'](row[self.controls[item]['column']])
        except IndexError as e:
            showerror('No Records', 'No records exist for this form.\n\nThere are %d records in the table.'%(len(self.row_list)))


    @debugger
    def configure_obj(self, name, **kargs):
        '''
        Call "configure" on an underlying object with the parameters indicated.
        '''
        self.controls[name]['obj'].configure(**kargs)

    @debugger
    def prev_callback(self):
        '''
        Default callback for the Prev button.
        '''
        self.row_index -= 1
        if self.row_index < 0:
            self.row_index = 0
            showinfo('First Record', 'There is no previous record.')
        else:
            self.load_form()

    @debugger
    def next_callback(self):
        '''
        Default callback for the next button.
        '''
        self.row_index += 1
        if self.row_index > len(self.row_list)-1:
            self.row_index = len(self.row_list)-1
            showinfo('Last Record', 'There is no next record.')
        else:
            self.load_form()

    @debugger
    def select_callback(self):
        '''
        Default callback for the select button. This displays a dialog of the "Name" field
        of all of the rows that are defined in the table. If the name field does not exist,
        throw an exception.
        '''
        self.logger.debug("select_callback")

    @debugger
    def new_callback(self):
        '''
        Default callback for the "New" button. This clears the form to default values.
        '''
        for item in self.controls:
            self.controls[item]['clear']()

    @debugger
    def save_callback(self):
        '''
        Default callback for the "Save" button. This writes the for to the database.
        '''
        if askyesno('Save record?', 'Are you sure you want to save this?'):
            self.commit_form()

    @debugger
    def delete_callback(self):
        '''
        Default callback for the delete button. This deletes the current row from the
        database and displays the next one. If deleting the last row, then the first
        row is displayed.
        '''
        if askyesno('Delete record?', 'Are you sure you want to delete this?'):
            self.data.delete_row(self.table, self.row_list[self.row_index])
            self.data.commit()

    @debugger
    def set_layout_row(self, num):
        '''
        Set the layout row to the given number.
        '''
        self.row = num

    @debugger
    def set_layout_col(self, num):
        '''
        Set the layout column to the given number.
        '''
        self.col = num

    @debugger
    def get_layout_row(self):
        '''
        Returnthe layout row.
        '''
        return self.row

    @debugger
    def get_layout_col(self):
        '''
        Return the layout column.
        '''
        return self.col
