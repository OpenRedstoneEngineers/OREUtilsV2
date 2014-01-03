#Base class for an event
class Event(object):
	def __init__(self, description=''):
		self.desc = description

	def __repr__(self):
		return "Event: "+self.desc

#An event pertaining to a player
class PlayerEvent(Event):
	desc = ''
	def __init__(self, player):
		self.player = player
	
	def GetPlayer(self):
		pass

	def __repr__(self):
		return self.player+" "+self.desc

#An event relating to the server
class ServerEvent(Event):
	pass

#A player joined the game
class Join(PlayerEvent):
	desc = "joined the game"

#A player is no longer in the game
class Leave(PlayerEvent):
	desc = "is no longer in the game"

#A player left of their own free will
class Quit(Leave):
	desc = "left the game"

#A player was kicked
class Kick(Quit):
	desc = "was kicked from the game"

#A player said something
class Talk(PlayerEvent):
	def __init__(self, player, message):
		self.desc   = ": "+message
		self.player = player

#Server started
class Stop(ServerEvent):
	def __init__(self, reason):
		self.desc = reason

	def __repr__(self):
		return "The server stopped : "+self.desc

#Server stopped
class Start(ServerEvent):
	def __init__(self, reason):
		self.desc = reason

	def __repr__(self):
		return "The server has started : "+self.desc
