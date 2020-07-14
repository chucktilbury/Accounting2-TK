'''
This is the module that implements the notebook container.

There are 2 frames. The top frame holds the buttons and the bottom frame holds controls.

'''

import tkinter as tk
import tkinter.ttk as ttk
from utility import debugger, Logger

class Notebook(tk.Frame):
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

    def __init__(self, master, height=700, width=1000, *args, **kwargs):

        super().__init__(master, **kwargs)
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug("enter constructor")

        self.master = master
        self.width = width
        self.height = height
        self.btn_frame = tk.LabelFrame(self.master, height=height, width=20, bd=1)
        self.wid_frame = tk.LabelFrame(self.master, height=height, width=width, bd=1)

        self.btn_frame.grid(row=0, column=0, sticky=tk.W)
        self.wid_frame.grid(row=1, column=0)

        self.frame_list = []
        self.frame_index = 0

        self.logger.debug("leave constructor")

    @debugger
    def show_frame(self, index):

        self.logger.debug('index: %d'%(index))
        #if not self.callback is None:
        #    self.callback()

        for item in self.frame_list:
            item['frame'].grid_forget()
            item['btn'].configure(relief=tk.RAISED)

        self.frame_list[index]['frame'].grid(row=1, column=0)
        self.frame_list[index]['btn'].configure(relief=tk.SUNKEN)

        if not self.frame_list[index]['callback'] is None:
            self.frame_list[index]['callback']()

    @debugger
    def get_frame(self, index):
        '''
        Use this to get the frame to bind widgets to.
        '''
        self.logger.debug("index: %d"%(index))
        return self.frame_list[index]['frame']

    @debugger
    def add_tab(self, title, *args, **kargs):
        '''
        Add a new tab to the notebook.
        '''
        panel_frame = {}
        self.logger.debug("title: \'%s\'"%(title))
        panel_frame['frame'] = tk.Frame(self.wid_frame, height=self.height, width=self.width)

        btn = tk.Button(self.btn_frame, text=title, width=10, relief=tk.RAISED, command=lambda idx=self.frame_index: self.show_frame(idx))
        btn.grid(column=self.frame_index, row=0, sticky=(tk.W))

        panel_frame['btn'] = btn
        panel_frame['callback'] = None

        self.frame_index += 1
        self.frame_list.append(panel_frame)

    @debugger
    def set_callback(self, index, callback):
        '''
        This callback will be called when the tab is selected.
        '''
        self.frame_list[index]['callback'] = callback
