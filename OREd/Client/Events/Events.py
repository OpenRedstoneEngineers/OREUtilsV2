#Base class for an event
class Event(object):
	def __init__(self, server, description=''):
		self.string = description

	def __repr__(self):
		return "Event: "+self.string

#An event pertaining to a player
class PlayerEvent(Event):
	def __init__(self, server, player, description=''):
		self.player = player
		self.string = description

	def GetPlayer(self):
		pass

#An event relating to the server
class ServerEvent(Event):
	pass
#A player joined the game
class Join(PlayerEvent):	
	pass

#A player is no longer in the game
class Leave(PlayerEvent):
	pass

#A player left of their own free will
class Quit(Leave):
	pass

#A player was kicked
class Kick(Quit):
	pass

#A player said something
class Talk(PlayerEvent):
	pass

#Server started
class Stop(ServerEvent):
	pass

#Server stopped
class Start(ServerEvent):
	pass
