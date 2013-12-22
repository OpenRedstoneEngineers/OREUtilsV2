from collections import defaultdict

from Helper import color

class ChannelMode:
	PUBLIC	 = 0
	PASSWORD = 1
	INVITE   = 2

class Channel:
	def __init__(self, name, mode):
		self.mode    = mode
		self.name    = name
		self.players = []

	def Join(self, player):
		if player in self.players:
			return False

		self.players.append(player)

		self.BroadcastJoin(player.getName())

		return True

	def Leave(self, player):
		if player not in self.players:
			return False

		self.players.remove(player)		

		self.BroadcastLeave(player.getName())

		return True

	def Broadcast(self, msg):
		for player in self.players:
			player.sendMessage(msg)

	def BroadcastMsg(self, playerName, chanMsg):
		msg = "[" + self.name + "] " + playerName + ": " + chanMsg

		self.Broadcast(msg) 

	def BroadcastJoin(self, playerName):
		msg = "[" + self.name + "] " + playerName + " has joined the channel"

		self.Broadcast(msg) 

	def BroadcastLeave(self, playerName):
		msg = "[" + self.name + "] " + playerName + " has left the channel"

		self.Broadcast(msg) 

class ChannelManager:
	MAX_CHANS = 10

	def __init__(self):
		self.Channels      = {}
		self.ActiveChannel = defaultdict(str)

	def GetOrCreate(self, chanName):
		chan = self.Channels.get(chanName)

		if chan == None:
			if len(self.Channels) >= self.MAX_CHANS:
				return None

			chan = Channel(chanName, ChannelMode.PUBLIC)

			self.Channels[chanName] = chan

		return chan

	def Join(self, player, chanName):
		chan = self.GetOrCreate(chanName)

		if chan == None:
			return False

		if not chan.Join(player):
			return False

		self.ActiveChannel[player.getName()] = chanName

		return True

	def Leave(self, player, chanName):
		chan = self.GetOrCreate(chanName)

		if chan == None:
			return False

		if not chan.Leave(player):
			return False

		if self.ActiveChannel[player.getName()] == chanName:
			del self.ActiveChannel[player.getName()]

		if not chan.players:
			del self.Channels[chanName]

		return True

	def ChanMsg(self, player, chanName, msg):
		chan = self.GetOrCreate(chanName)

		if chan == None:
			return False

		if player in chan.players:
			chan.BroadcastMsg(player.getName(), msg)
		
	def LeaveAll(self, player):
		for chan in self.Channels.itervalues():
			chan.Leave(player)

		del self.ActiveChannel[player.getName()]

Chans = ChannelManager()

@hook.command("cchat", usage="/<command> <join|leave|info|switch> <channel>")
def OnCommandCChat(sender, args):
	if len(args) != 2:
		return False

	cmd  = args[0]
	chan = args[1]

	if cmd == "join":
		if Chans.Join(sender, chan):
			sender.sendMessage("Welcome to channel " + color("9") + chan)
		else:
			sender.sendMessage(color("c") + "You are already in that channel")

		return True

	elif cmd == "leave":
		if Chans.Leave(sender, chan):
			sender.sendMessage("You have left the channel")
		else:
			sender.sendMessage("You are not in that channel")

		return True

	elif cmd == "info":
		if chan not in Chans.Channels:
			sender.sendMessage("No such channel")
			return True

		msg = ', '.join([x.getName() for x in Chans.Channels[chan].players])

		sender.sendMessage("Players in channel " + chan + ": " + msg) 

		return True

	elif cmd == "switch":
		if chan not in Chans.Channels:
			sender.sendMessage("No such channel")
			return True

		if sender not in Chans.Channels[chan].players:
			sender.sendMessage("You are not in that channel")
			return True

		Chans.ActiveChannel[sender.getName()] = chan

		return True
	
	return False

@hook.command("ccadmin", usage="/<command> <list|playerinfo|kick>")
def OnCommandCCAdmin(sender, args):
	if not sender.hasPermission("ore.cchat.admin"):
		sender.sendMessage("No permission")
		return True

	if len(args) == 0:
		return False

	cmd = args[0]

	if cmd == "list":
		sender.sendMessage("Active channels:")

		for chan in Chans.Channels.iterkeys():
			sender.sendMessage(chan)

		return True

	elif cmd == "playerinfo":
		if len(args) != 2:
			sender.sendMessage("Usage: /ccadmin playerinfo <player>")
			return True

		sender.sendMessage("Player " + args[1] + ":")

		for chanName, chan in Chans.Channels.iteritems():
			for player in chan.players:
				if player.getName() == args[1]:
					sender.sendMessage(chanName)

		return True

	elif cmd == "kick":
		if len(args) != 3:
			sender.sendMessage("Usage: /ccadmin kick <player> <channel>")
			return True

		chan = Chans.Channels.get(args[2])

		if chan == None:
			sender.sendMessage("No such channel")
			return True

		for player in chan.players:
			if player.getName() == args[1]:
				player.sendMessage("You have been kicked from channel " + args[2])

				sender.sendMessage("Kicked player " + args[1] + " from channel " + args[2])

				chan.Leave(player)

		return True

	return False

@hook.command("cc", usage="/<command> <message>")
def OnCommandCC(sender, args):
	msg = ' '.join(args)

	chan = Chans.ActiveChannel.get(sender.getName())

	if chan == None or chan == "":
		sender.sendMessage("You are not in a channel")
		return True

	Chans.ChanMsg(sender, chan, msg)

	return True

@hook.event("player.PlayerQuitEvent", "monitor")
def OnEventQuit(event):
	Chans.LeaveAll(event.getPlayer())
