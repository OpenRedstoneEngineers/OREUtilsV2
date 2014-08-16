"""
Permission nodes:

ore.irc.admin
"""

import IRCBot

from org.bukkit import Bukkit
from org.bukkit import ChatColor

from .. import Helper
from .. import ChannelChat

SendInfo, SendWarning, SendError = Helper.SendInfo, Helper.SendWarning, Helper.SendError # Hack

class AliasInfo:
	def __init__(self, name, isServer, srvcolor):
		self.Name = name
		
		self.IsServer = isServer

		self.SrvColor = srvcolor
		self.BraColor = ChatColor.getByChar(hex(int(ChatColor.getChar(srvcolor), 16) ^ 8)[-1])
		self.NamColor = ChatColor.AQUA
		self.MsgColor = ChatColor.WHITE

	def GetServTag(self):
		return str(self.BraColor) + "[" + str(self.SrvColor) + self.Name + str(self.BraColor) + "]"

	def GetTag(self, name):
		return str(self.BraColor) + "[" + str(self.SrvColor) + self.Name + str(self.BraColor) + "]" + str(self.NamColor) + name + ": " + str(self.MsgColor)

class OREBot(IRCBot.IRCBot):
	Aliases = { "OREBuild"    : AliasInfo("Build",    True, ChatColor.RED),
	            "ORESchool"   : AliasInfo("School",   True, ChatColor.BLUE),
	            "ORESurvival" : AliasInfo("Survival", True, ChatColor.YELLOW),
	            "ORETest"     : AliasInfo("Test",     True, ChatColor.GREEN)  }

	DefaultAlias = AliasInfo("IRC", False, ChatColor.RED)

	Muted = []

	def __init__(self):
		IRCBot.IRCBot.__init__(self, self.HOST, self.PORT, self.NAME, self.NAME)

		if self.PASS != None:
			self.NickServIdentify(self.PASS)

		self.Join(self.CHAN)

	def GetAlias(self, name):
		alias = self.Aliases.get(name)

		if alias == None:
			return self.DefaultAlias
		else:
			return alias

	def OnJoin(self, name):
		Bukkit.broadcastMessage(str(ChatColor.YELLOW) + name + " joined IRC")

	def OnLeave(self, name):
		Bukkit.broadcastMessage(str(ChatColor.YELLOW) + name + " left IRC")

	def OnPrivMsg(self, name, message):
		Helper.Info("Private IRC message from %s: %s" % (name, message))

	def OnChanMsg(self, name, message):
		if name in self.Muted:
			return

		alias = self.GetAlias(name)

		if alias.IsServer:
			args = message.split()

			if args[0].endswith(':'):
				Bukkit.broadcastMessage(alias.GetTag(args[0][:-1]) + " ".join(args[1:]))
			else:
				Bukkit.broadcastMessage(str(ChatColor.YELLOW) + " ".join(args[:2]) + " " + alias.Name.lower())
		else:
			args = message.split(' ')
			
			if args[0].startswith('%'):
				channel = args[0][1:]

				ChannelChat.GetChan().ChanMsgIRC('&1[&3IRC&1]&f'+name, channel, ' '.join(args[1:]))
			elif args[0].startswith('@'):
				reciever = args[0][1:]
				
				for player in Bukkit.getServer().getOnlinePlayers():
					if player.getName() == reciever:
						player.sendMessage(str(ChatColor.BLUE) + "[" + str(ChatColor.AQUA) + "IRC " + name + " -> me" + str(ChatColor.BLUE) + "]" + str(ChatColor.WHITE) + " " + " ".join(args[1:]))
			else:
				Bukkit.broadcastMessage(alias.GetTag(name) + message)		

def Init(host, port, name, nickPass, chan):
	global Bot

	# OREBot.Aliases = aliases

	OREBot.HOST = host
	OREBot.PORT = port
	OREBot.NAME = name
	OREBot.CHAN = chan
	OREBot.PASS = nickPass

	Bot = OREBot()

def Terminate():
	Bot.Quit()

@hook.command("ircadmin")
def OnCommandIRCAdmin(sender, args):
	if not sender.hasPermission("ore.irc.admin"):
		SendError(sender, "No permission!")
		return True

	if len(args) == 0:
		SendInfo(sender, "--- IRC Admin ---")
		SendInfo(sender, "status     - Connection status")
		SendInfo(sender, "disconnect - Disconnect from remote server")
		SendInfo(sender, "reconnect  - Reconnect to remote server")
		SendInfo(sender, "raw        - Send a raw command")
		SendInfo(sender, "mute       - Mute a particular player")
		SendInfo(sender, "unmute     - Guess. I dare you.")

		return True

	cmd = args[0]

	if cmd == "status":
		if Bot.running == True:
			SendInfo(sender, "Connected to %s:%i" % (OREBot.HOST, OREBot.PORT))
		else:
			SendWarning(sender, "No active connection")

	elif cmd == "disconnect":
		if Bot.running == True:
			Bot.Quit()

			SendInfo(sender, "Disconnected from %s:%i" % (OREBot.HOST, OREBot.PORT))
		else:
			SendWarning(sender, "No active connection")

	elif cmd == "reconnect":
		if Bot.running == True:
			Bot.Quit()

		Bot.__init__()

		SendInfo(sender, "Connected to %s:%i" % (OREBot.HOST, OREBot.PORT))

	elif cmd == "raw":
		if Bot.running == True:
			Bot.Send(' '.join(args[1:]) + "\r\n")
		else:
			SendWarning(sender, "No active connection")

	elif cmd == "mute":
		if len(args) < 2:
			SendInfo(sender, "Muted players:")

			for name in OREBot.Muted:
				SendInfo(sender, "-" + name)
		else:
			OREBot.Muted.append(args[1])

	elif cmd == "unmute":
		if len(args) < 2:
			SendInfo(sender, "Muted players:")

			for name in OREBot.Muted:
				SendInfo(sender, "-" + name)
		else:
			if args[1] in OREBot.Muted:
				OREBot.Muted.remove(args[1])

	else:
		SendError(sender, "Invalid action")
		
	return True

@hook.event("player.PlayerChatEvent", "monitor")
def OnEventChat(e):
	Bot.ChanMessage(e.getPlayer().getName() + ": " + e.getMessage())

@hook.event("player.PlayerJoinEvent", "monitor")
def OnEventJoin(e):
	Bot.ChanMessage(e.getPlayer().getName() + " joined the game")

@hook.event("player.PlayerQuitEvent","monitor")
def OnEventJoin(e):
	Bot.ChanMessage(e.getPlayer().getName() + " left the game")
