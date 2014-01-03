from API import Base

class Player(Base):
	def __init__(self, name, Console):
		self.name = name

	def Tell(self, message):
		self.Console.Raw('t %s %s'%(self.name, message))

	def Kick(self, message=''):
		self.Console.Raw('kick %s %s'%(self.name, message))

	def Ban(self, message=''):
		self.Console.Raw('ban %s %s'%(self.name, message))

	def GetRank(self):
		pass
