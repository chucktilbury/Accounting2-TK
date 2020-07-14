import sys
from utility import Logger, debugger

class EventHandler(object):
    '''
    This class implements a simple way to handle communications between classes.
    It could be used generically, but it was designed for this purpose. It
    operates by making lists of callbacks that can be called from any other
    class. When a callback is registered by multiple classes, every instance is
    called in the order that it was created.

    This is a singleton class. When you instantiate it for another class, use the
    x.get_instance() method. It must never be instantiated directly. When the
    get_instance() method is called for the first time, the object is created.
    '''
    __instance = None

    @staticmethod
    def get_instance():
        '''
        This static method is used to get the singleton object for this class.
        '''
        if EventHandler.__instance == None:
            EventHandler()
        return EventHandler.__instance

    def __init__(self):

        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug("Event Handler start constructor")

        # gate the access to __init__()
        if EventHandler.__instance != None:
            raise Exception("EventHandler class is a singleton. Use get_instance() instead.")
        else:
            EventHandler.__instance = self

        self.__event_list__ = {}

        self.logger.debug("Event Handler leave constructor")

    @debugger
    def register_event(self, name, callback):
        '''
        Store the event in the internal storage.
        '''
        # print("%s: %s: %s.%s"%(
        #             sys._getframe().f_code.co_name,
        #             name,
        #             callback.__self__.__class__.__name__,
        #             callback.__name__))

        if not name in self.__event_list__:
            self.__event_list__[name] = []
        self.__event_list__[name].append(callback)


    @debugger
    def raise_event(self, name, *args):
        '''
        Call all of the callbacks that have been registered.
        '''
        # print("%s: %s"%(sys._getframe().f_code.co_name, name))
        if name in self.__event_list__:
            for cb in self.__event_list__[name]:
                if len(args) != 0:
                    cb(*args)
                else:
                    cb()
        # print("%s: %s"%(sys._getframe().f_code.co_name, "returning"))

    def dump_events(self):
        for item in self.__event_list__:
            print("%s:"%item)
            for cb in self.__event_list__[item]:
                print("\t%s.%s"%(cb.__self__.__class__.__name__, cb.__name__))
