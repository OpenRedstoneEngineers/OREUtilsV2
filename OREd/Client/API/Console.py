from Connection import Connection

class Console(Connection):
	def Raw(self, message):
		self.Send('raw '+message)
