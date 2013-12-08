from __future__ import with_statement

import random

from Helper import color 

import org.bukkit.Bukkit.broadcastMessage as broadcastMessage

"""
Permission nodes:

ore.derp.reload
"""

Derps = []

def LoadDerps(filename):
	global Derps

	with open(filename) as f:
		Derps = [X.replace('\n', '') for X in f.xreadlines()]

def BroadcastDerp(sender, message):
	broadcastMessage(color("2") + " * " + color("f") + sender.getName() + color("l") + " DERP! " + color("r") + color("d") + message)

@hook.command("derp", description="Let your derp shine!")
def OnCommandDerp(sender, args):
	if len(args) > 0 and args[0].isdigit():
		index = int(args[0])

		if index >= len(Derps) or index < 0:
			sender.sendMessage("Index out of range")
			return True

		BroadcastDerp(sender, Derps[index])

		return True

	if len(args) > 0 and not args[0].isdigit() and sender.hasPermission('ore.derp.reload'):
		if args[0] == "reload":
			LoadDerps("Data/Derps.txt")

			sender.sendMessage(color("e") + "Derps reloaded")

			return True

	BroadcastDerp(sender, random.choice(Derps))

	return True

@hook.command("Derps", description="List available Derps")
def OnCommandDerps(sender, args):
	for counter, derp in enumerate(Derps):
		sender.sendMessage(color("1") + str(counter) + color("f") + ": " + color("a") + derp)

	return True

