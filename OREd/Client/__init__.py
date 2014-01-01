import Scripting
import Events
import API

#Create an iterable of the names of Exceptions
EventNames = [X for X in dir(Events) if not X[0] == "_"]

import sys

class EventManager:
	def __init__(self):
		self.API = API.Base
		self.ScriptManager = Scripting.Hooks(API=self.API)#Put things in here to be API in scripts

	def OnCommand(self, name, args):
		if not self.ScriptManager.Exec(name, args):
			print('Unknown command: '+name)

	def OnEvent(self, name, kwargs):
		found = Events.__dict__.get(name)
		if found:
			instance = found(**kwargs)
			self.ScriptManager.Event(instance)
            
		else:
			("Unknown event: "+name)
        
if __name__ == "__main__":
	e = EventManager()
	API.Base.Console.Init('Blah')
	API.Base.Logger.Init('Log.txt')
