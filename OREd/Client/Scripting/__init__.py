import os
import Events

#A class for containing a series of functions When an instance is
#called, the first arg is appended to the class' list of functions
class Functions:
	def __init__(self):
		self.functions = []

	def __call__(self, function):
		self.functions.append(function)

	#Execute all scripts with args
	def Exec(self, args):
        
		for script in self.functions:
			try:
				script(*args)

			except Exception as E:
				return E

#A class for containing all hooks of exceptions and commands
class Hooks:
	def __init__(self, **API):
		self.commands = {}
		self.events = {}
		API["command"] = self.WrapCommand
		API["event"]   = self.WrapEvent		
        	
		for path in os.listdir(os.getcwd()+"/Scripting/Scripts"):
			fullPath = "Scripting/Scripts/"+path
			exec(compile(open(fullPath).read(), fullPath, "exec"), API)

	#Used internally to assign functions to items in dicts
	def GetFunctions(self, name, array):
		if name in array:
			return array[name]

		else:
			instance = Functions()
			array[name] = instance

			return instance

	#Return a Functions instance relating to a command
	def WrapCommand(self, name):
		return self.GetFunctions(name, self.commands)

	#Return a Functions instance relating to an exception
	def WrapEvent(self, event):
		if event[0] != "_" and event in Events.__dict__:
			Event = Events.__dict__[event] 
			return self.GetFunctions(Event, self.events) 

		return False
	#Execute the scripts relating to an event
	def Event(self, event):
		for eventType, scripts  in self.events.items():
			if isinstance(event, eventType):
				scripts.Exec((event,))

	#Execute the scripts relating to a command
	def Exec(self, name, args):
		command = self.commands.get(name)

		if command:
			command.Exec(args)
			return True
