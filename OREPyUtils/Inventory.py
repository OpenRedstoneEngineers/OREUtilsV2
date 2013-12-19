from collections import defaultdict

import PersistentData

"""
Permission nodes:

ore.inv
"""

def LoadPreset(path):
	global PresetFile, Presets
	
	PresetFile = PersistentData.NodeFile(path)
	PresetFile.Ensure("Players")
	
	Presets = PresetFile.node.Players
	
def SavePreset():
	PresetFile.Dump()

def GetItems(player):
	inv = player.getInventory()

	items = []

	for slot in xrange(9):
		items.append(inv.getItem(slot))

	return items

def SetItems(player, items):
	inv = player.getInventory()

	for slot, item in enumerate(items):
		inv.setItem(slot, item)

@hook.command("inv", usage="Usage: /inv (save|load|remove|list|clear) <name>")
def onCommandInv(sender, args):
	if not sender.hasPermission("ore.inv"):
		sender.sendMessage("No permission!")
		return True

	if len(args) == 2:
		cmd  = args[0]
		name = args[1]

		player = Presets.Ensure(sender.getName())

		if cmd == "save":
			if len(args) != 2:
				return False

			player[args[1]] = GetItems(sender)

			sender.sendMessage("Preset " + args[1] + " saved.")

		elif cmd == "load":
			if len(args) != 2:
				return False
		
			if args[1] in player:
				items = player[args[1]]
				SetItems(sender, items)
			
			else:
				sender.sendMessage("No such preset!")
		elif cmd == "remove":
			if len(args) != 2:
				return False
	
			if args[1] in player:
				del player[args[1]]
				sender.sendMessage("Removed preset " + args[1])
				
			else:
				sender.sendMessage("No such preset!")
	
		elif cmd == "list":
			if player:
				sender.sendMessage("Presets:")
	
				for name in player:
					sender.sendMessage("- " + name)		
			else:
				sender.sendMessage("No presets!")
	
		elif cmd == "clear":
			player.clear()
		
		else:
			sender.sendMessage("Not a valid subcommand")
	else:
		sender.sendMessage("/inv (save|load|remove|list|clear) <name>")
			
	return True
