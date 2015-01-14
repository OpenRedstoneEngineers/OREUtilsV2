import Scripting
import Events
import API
import threading
import sys

# Create an iterable of the names of Exceptions
EventNames = [X for X in dir(Events) if not X[0] == "_"]


class EventManager:
    def __init__(self):
        self.API = API.Base
        self.ScriptManager = Scripting.Hooks(API=self.API)  # Put things in here to be API in scripts

    ##Add inits for threads

    # Called when a command is recieved, to attempt to find the script
    def OnCommand(self, name, args):
        if not self.ScriptManager.Exec(name, args):
            print('Unknown command: ' + name)

    # Called when an event is recieved, to perform relevant scripts
    def OnEvent(self, name, kwargs):
        found = Events.__dict__.get(name)
        if found:
            instance = found(**kwargs)
            self.ScriptManager.Event(instance)

        else:
            ("Unknown event: " + name)

    # Calls events and commands from a console.
    def Core(self, Console):
        for packet in Console.Loop():
            args = packet.split()

            self.API.LoadAPI(args[0])

            commandType = args[1]

            if commandType == 'EVENT':
                kwargs = {x[0]: x[1] for x in (z.split('=') for z in args[3:])}
                self.OnEvent(args[2], kwargs)

            elif commandType == 'CMD':
                self.OnCommand(args[2], args[3:])


if __name__ == "__main__":

    ##Add inits for server APIs

    for Console in API.Base.Consoles.values():
        Console.Init('Blah')

    for Logger in API.Base.Loggers:
        Logger.Init('Log.txt')

    EventManager().Core()
