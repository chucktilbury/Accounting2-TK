#!/usr/bin/env python3
import sys, uuid
import tkinter as tk
import tkinter.ttk as ttk
from events import EventHandler
from utility import debugger, Logger


class __notebook_frame(ttk.Frame):
    '''
    This is the scrollable frame class that is used by the NoteBk class. It
    could be used generically, but it was designed for use here.

    To get the frame to bind widgets to, call the object directly.

    The scrolling functionality supports both a scroll bar as well as the
    mouse wheel.
    '''

    def __init__(self, container, height=300, width=500, scrolling=False, *args, **kwargs):

        self.logger = Logger(self, level=Logger.INFO)
        self.logger.debug("enter constructor")
        super().__init__(container, *args, **kwargs)

        self.canvas = tk.Canvas(self, height=height, width=width)
        self.scrollwindow = tk.Frame(self.canvas)

        self.canvas.create_window((0, 0), window=self.scrollwindow, anchor="nw")


        self.canvas.pack(side="left", fill="both", expand=True)

        if scrolling:
            scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
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

    def __call__(self):
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

class NoteBkBtn(tk.Button):
    '''
    This Button class keeps track of the state is relation to the NoteBk
    class. It makes no sense outside of that context.
    '''

    def __init__(self, master, title, uuid, *args, **kargs):
        self.logger = Logger(self, level=Logger.INFO)
        self.logger.debug("enter constructor")

        super().__init__(master, *args, **kargs)
        self.configure(width=10)
        self.configure(command=self.btn_cmd)
        self.configure(text=title)
        self.last_state = True
        self.title = title
        self.uuid = uuid
        self.events = EventHandler.get_instance()
        self.logger.debug("leave constructor")

    @debugger
    def btn_cmd(self):
        #print('here', self.title)
        self.events.raise_event('clearButtons_%s'%(self.uuid))
        self.set_state(False)
        self.events.raise_event('show_frame_%s'%(self.title), self.title)

    @debugger
    def set_state(self, state):
        self.logger.debug('button: %s, state: %s'%(self.title, str(state)))
        if state:
            self.configure(relief=tk.RAISED)
        else:
            self.configure(relief=tk.SUNKEN)
        self.last_state = state

    @debugger
    def set_last_state(self):
        #print('here1')
        self.set_state(self.last_state)

class NoteBk(tk.Frame):
    '''
    Build a frame where there are buttons on the left and a area for widgets
    on the right. Pressing a button on the left activates a frame that is
    connected to it. The frames on the right are passed in as references to a
    class constructor. NoteBk frames can be nested such that the higher level
    NoteBk can hide and display a lower level NoteBk.

    Frames are kept as a list and are not destroyed during use. They are
    hidden and displayed using the grid layout manager.

    To properly use this container, first instantiate the class, then add
    all of the tabs. The tab name is used for the button and also internally
    to coordinate the tab buttons and display the frames connected to the
    tabs. The tab names are used to connect the widgets in the frame to the
    frame itself.
    '''

    def __init__(self, master, height=500, width=500, *args, **kargs):

        super().__init__(master, *args, **kargs)
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug("enter constructor")

        self.master = master
        self.width = width
        self.height = height
        self.btn_frame = tk.LabelFrame(self.master, height=height, width=20, bd=1)
        self.wid_frame = tk.LabelFrame(self.master, height=height, width=width, bd=1)
        self.uuid = uuid.uuid4().hex

        self.btn_frame.grid(row=0, column=0, sticky=tk.N)
        self.wid_frame.grid(row=0, column=1)#, rowspan=40)

        self.frame_list = {}
        self.frame_index = 0

        self.events = EventHandler.get_instance()
        self.events.register_event('clearButtons_%s'%(self.uuid), self.clear_buttons)
        self.logger.debug("leave constructor")

    @debugger
    def clear_buttons(self):
        #print('here2')
        for item in self.frame_list:
            self.frame_list[item]['btn'].set_state(True)

    @debugger
    def get_uuid(self):
        return self.uuid

    @debugger
    def show_frame(self, title):

        self.logger.debug('index: %d, frame: %s'%(self.frame_list[title]['index'], title))
        for item in self.frame_list:
            self.frame_list[item]['frame'].grid_forget()
            self.frame_list[item]['btn'].set_last_state()

        #print(self.frame_list[title]['frame'])
        self.frame_list[title]['frame'].grid(row=0, column=1)
        self.frame_list[title]['btn'].set_state(False)

        # call the callback when the tab button is pressed, if it was
        # specified when the tab was added.
        if not self.frame_list[title]['callback'] is None:
            self.frame_list[title]['callback']()


    @debugger
    def get_frame(self, title):
        '''
        Use this to get the frame to bind widgets to.
        '''
        return self.frame_list[title]['frame']()

    @debugger
    def add_tab(self, title, frame_class, scrolling=False, height=None, width=None, *args, **kargs):
        '''
        Add a new tab to the notebook.
        '''
        if height is None:
            height = self.height

        if width is None:
            width = self.width

        self.events.register_event('show_frame_%s'%(title), self.show_frame)
        panel_frame = {}
        btn = NoteBkBtn(self.btn_frame, title, self.uuid)
        btn.grid(row=self.frame_index, sticky=(tk.E))
        panel_frame['btn'] = btn

        self.logger.debug("title: \'%s\'"%(title))
        panel_frame['frame'] = ScrollableFrame(self.wid_frame, height=height, width=width, scrolling=scrolling)
        #obj = frame_class(panel_frame['frame'], *args, **kargs)
        obj = frame_class(panel_frame['frame'].scrollwindow, *args, **kargs)

        if 'notebook_callback' in dir(obj):
            panel_frame['callback'] = obj.notebook_callback
        else:
            panel_frame['callback'] = None
        panel_frame['index'] = self.frame_index
        self.frame_list[title] = panel_frame

        self.frame_index += 1

class DummyClass(object):
    '''
    This class allows adding a tab without specifying a frame_class.
    '''
    def __init__(self, master):
        pass
