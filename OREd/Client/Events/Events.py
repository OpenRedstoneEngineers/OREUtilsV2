#Base class for an event
class Event(object):
	def __init__(self, string):
		self.string = string

	def __repr__(self):
		return "Event: "+self.string

#An event pertaining to a player
class PlayerEvent(Event):
	def __init__(self, player, description=None):
		self.player = player
		self.string = description

	def GetPlayer(self):
		pass
#A player joined the game
class JoinEvent(PlayerEvent):	
	pass

#A player is no longer in the game
class QuitEvent(PlayerEvent):
	pass

#A player left of their own free will
class LeaveEvent(QuitEvent):
	pass

#A player was kicked
class KickEvent(QuitEvent):
	pass

#A player said something
class TalkEvent(PlayerEvent):
	pass
