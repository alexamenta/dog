"""
this is heavily inspired by
https://github.com/wesleywerner/mvc-game-design
"""
from game import Move
from weakref import WeakSet


class Event():
    """
    A superclass for events.
    """

    def __init__(self):
        self.name = "Generic event"
    def __str__(self):
        return self.name
   

class QuitEvent(Event):
    """
    Quit event.
    """

    def __init__(self):
        self.name = "Quit event"


class TickEvent(Event):
    """
    Tick event.
    """

    def __init__(self):
        self.name = "Tick event"


class InputEvent(Event):
    """
    Input event.
    """

    def __init__(self, unicodechar, clickpos):
        self.name = "Input event"
        self.char = unicodechar
        self.clickpos = clickpos

    def __str__(self):
        return '%s, char=%s, clickpos=%s' % (self.name, self.char, self.clickpos)


class MoveEvent(Event):
    """
    Move event.
    Move Player to Position.
    """

    def __init__(self, move):
        """
        move (game.Move): a move
        """
        self.move = move


class InitializeEvent(Event):
    """
    Tells all listeners to initialize themselves.
    This includes loading libraries and resources.

    Avoid initializing such things within listener __init__ calls
    to minimize snafus (if some rely on others being yet created.)
    """

    def __init__(self):
        self.name = "Initialize event"


class EventManager():
    """
    Coordinates communication between the Model, View, and Controller.
    """

    def __init__(self):
        self.listeners = WeakSet()

    def RegisterListener(self, listener):
        """
        Add listener to spam list.
        It will receive Post()ed events through its notify(event) call.
        """

        self.listeners.add[listener]

    def Post(self, event):
        """
        Post a new event to the message queue.
        It will be broadcast to all listeners.
        """

        # uncomment for debug purposes
        # 
        # if not isinstance(event, TickEvent):
        #    print(str(event))
        
        for listener in self.listeners.keys():
            listener.notify(event)
