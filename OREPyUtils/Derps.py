from __future__ import with_statement

import random

from Helper import Color, SendInfo, SendError 

import org.bukkit.Bukkit.broadcastMessage as broadcastMessage

"""
Permission nodes:

ore.derp.reload
"""

Derps = []

def OnEnable(conf=None):
	global Config
	Config = conf.node.properties

	LoadDerps()

def LoadDerps():
	global Derps

	Config.Ensure("DerpPath", "")
	Config.Ensure("MainPath", "")

	filename = Config.DerpPath.replace("[path]", Config.MainPath)

	with open(filename) as f:
		Derps = [X.replace('\n', '') for X in f.xreadlines()]

def BroadcastDerp(sender, message):
	broadcastMessage(Color("2") + " * " + Color("f") + sender.getName() + Color("l") + " DERP! " + Color("d") + message)

@hook.command("derp", description="Let your derp shine!")
def OnCommandDerp(sender, args):
	if len(Derps) == 0:
		SendError(sender, "No registered derps!")
		return True

	if len(args) > 0 and args[0].isdigit():
		Index = int(args[0])

		if Index >= len(Derps) or Index < 0:
			SendError(sender, "Index out of range")
			return True

		BroadcastDerp(sender, Derps[Index])

		return True

	if len(args) > 0 and not args[0].isdigit() and sender.hasPermission('ore.derp.reload'):
		if args[0] == "reload":
			LoadDerps()

			SendInfo(sender, "Derps reloaded")

			return True

	BroadcastDerp(sender, random.choice(Derps))

	return True

@hook.command("derps", description="List available Derps")
def OnCommandDerps(sender, args):
	if len(Derps) == 0:
		SendError(sender, "No registered derps!")
		return True

	for Counter, Derp in enumerate(Derps):
		sender.sendMessage(Color("1") + str(Counter) + Color("f") + ": " + Color("a") + Derp)

	return True
