
import sys, math, time, pprint, pickle
import traceback
from tkinter import messagebox as mbox
import tkinter as tk

class Logger(object):
    '''
    Logger class produces messages on the text console. Used mostly for
    debugging. Supports individual class debugging and debug levels.
    '''

    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    MESSAGE = 4
    STDERR = 0
    STDOUT = 1

    def __init__(self, name, level=DEBUG):

        self.dbg = 0
        self.inf = 1
        self.warn = 2
        self.err = 3
        self.mess = 4
        self.stderr = 0
        self.stdout = 1

        if type(name) == str:
            self.name = name
        else:
            self.name = name.__class__.__name__
        self.level = []
        self.level.insert(0, level)

        #if stream == self.STDERR:
        self.stream = sys.stderr
        #else:
        #self.stream = sys.stdout

    def fmt(self, args, lev):
        t = time.strftime("[%Y%m%d %H:%M:%S]")
        return "%s %s: %s: %s\n"%(t, lev, self.name, args)

    def debug(self, args, frame_num = 1):
        if self.level[0] <= self.dbg:
            s1 = sys._getframe(frame_num).f_code.co_name
            t = time.strftime("[%Y%m%d %H:%M:%S]")
            self.stream.write("%s %s: %s.%s(): %s\n"%(t, "DEBUG", self.name, s1, args))

    def info(self, args):
        if self.level[0] <= self.inf:
            self.stream.write(self.fmt(args, 'INFO'))

    def warning(self, args):
        if self.level[0] <= self.warn:
            self.stream.write(self.fmt(args, 'WARNING'))

    def error(self, args):
        if self.level[0] <= self.err:
            self.stream.write(self.fmt(args, 'ERROR'))

    def msg(self, args):
        if self.level[0] <= self.mess:
            self.stream.write(self.fmt(args, 'MSG'))

    def fatal(self, args):
        self.stream.write(self.fmt(args, 'FATAL ERROR'))
        self.stream.write("System cannot continue\n\n")
        sys.exit(1)

    def push_level(self, level):
        self.level.insert(0, level)

    def pop_level(self):
        if len(self.level) > 1:
            self.level.remove(0)

    def set_level(self, level):
        self.level[0] = level

    def debugger(self, name, args):
        if self.level[0] <= self.dbg:
            t = time.strftime("[%Y%m%d %H:%M:%S]")
            self.stream.write("%s %s: %s.%s(): %s\n"%(t, "DEBUG", self.name, name, args))

logger = Logger("Utility", Logger.INFO)

def base_decorator(decorator):
    '''This decorator can be used to turn simple functions
    into well-behaved decorators, so long as the decorators
    are fairly simple. If a decorator expects a function and
    returns a function (no descriptors), and if it doesn't
    modify function attributes or docstring, then it is
    eligible to use this. Simply apply @simple_decorator to
    your decorator and it will automatically preserve the
    docstring and function attributes of functions to which
    it is applied.'''
    def new_decorator(f):
        g = decorator(f)
        g.__name__ = f.__name__
        g.__doc__ = f.__doc__
        g.__dict__.update(f.__dict__)
        return g
    # Now a few lines needed to make simple_decorator itself
    # be a well-behaved decorator.
    new_decorator.__name__ = decorator.__name__
    new_decorator.__doc__ = decorator.__doc__
    new_decorator.__dict__.update(decorator.__dict__)
    return new_decorator

# debug decorator
@base_decorator
def debugger(func):
    '''
    Debugger decorator places messages in the debug output when the class
    method is entered and when it is exited. It cannot be used with functions
    and it depends on the class having a "logger" member. When the logging
    level is below DEBUG this function does nothing.

    This can only wrap a method in a class that has a logger.
    '''
    def wrapper(*args, **kwargs):
        #try:
        args[0].logger.debugger(func.__name__, "-- enter")
        #print(func.__name__, "-- enter")
        retv = func(*args, **kwargs)
        args[0].logger.debugger(func.__name__, "-- returning: %s"%(str(retv)))
        #print(func.__name__, "-- returning: %s"%(str(retv)))
        return retv
        #except Exception as ex:
        #    print(''.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)))

    return wrapper

