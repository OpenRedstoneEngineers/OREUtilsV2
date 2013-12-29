import Scripting
import Events
print(help(Events.Events))

#Create an iterable of the names of Exceptions
EventNames = [X for X in dir(Events) if not X[0] == "_"]
print(EventNames)

import sys

class EventManager:
    def __init__(self):
        self.ScriptManager = Scripting.Hooks()

    def OnCommand(self, name, args):
        if not self.ScriptManager.Exec(name, args):
            print('Unknown command: '+name)

    def OnEvent(self, name, args):
        found = Events.__dict__.get(name)
        if found:
            instance = found(args)
            self.ScriptManager.Event(instance)
            
        else:
            print("Unknown event: "+name)
        
if __name__ == "__main__":
    e = EventManager()
