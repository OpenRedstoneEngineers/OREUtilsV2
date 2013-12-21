import Connection

"""
@brief IRC Protocol Wrapper.
"""
class IRCBot(Connection.Connection):
	def __init__(self, hostname, port, nick, name):
		Connection.Connection.__init__(self, hostname, port)

		self.name = name
		self.nick = nick

		self.channel = None

		if self.running == False:
			return

		self.Send("NICK %s\r\n" % nick)
		self.Send("USER %s %s bla :%s\r\n" % (name, name, name))

	def NickServIdentify(self, password):
		self.Send("PRIVMSG NickServ :IDENTIFY %s\r\n" % password)

	def Quit(self):
		if self.running == False:
			return

		self.Send("QUIT\r\n")

		self.Stop()

	def Join(self, chan):
		if self.running == False:
			return

		self.channel = chan

		self.Send("JOIN :%s\r\n" % chan)

	def Nickname(self, nick):
		if self.running == False:
			return

		self.nick = nick

		self.Send("NICK %s\r\n" % nick)

	def OnMessage(self, data):
		cmds = data.split("\r\n")

		for cmd in cmds:
			self.HandleIRCCmd(cmd)

	def HandleIRCCmd(self, data):
		args = data.split()

		if len(args) > 1 and args[0] == "PING":
			self.Send("PONG " + ' '.join(args[1:]) + "\r\n")

		elif len(args) > 1 and args[1] == "JOIN":
			self.OnJoin(args[0].split('!')[0][1:])

		elif len(args) > 1 and args[1] == "PART":
			self.OnLeave(args[0].split('!')[0][1:])

		elif len(args) > 3 and args[1] == "PRIVMSG":
			sender = args[0].split('!')[0][1:]
			receiver = args[2]

			msg = ' '.join(args[3:])[1:]

			if receiver == self.nick:
				self.OnPrivMsg(sender, msg)
			else:
				self.OnChanMsg(sender, msg)

	def ChanMessage(self, message):
		if self.channel == None or self.running == False:
			return

		self.Send("PRIVMSG %s :%s\r\n" % (self.channel, message))

	def PrivMsg(self, target, message):
		if self.running == False:
			return

		self.Send("PRIVMSG %s :%s\r\n" % (target, message))
