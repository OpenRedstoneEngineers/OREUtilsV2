from collections import defaultdict

import PersistentData

from Helper import SendInfo, SendError

"""
Permission nodes:

ore.inv
"""

def OnEnable(path="InventoryPresets.json"):
	global PresetFile, Presets
	
	PresetFile = PersistentData.NodeFile(path)

	PresetFile.node.Ensure("Players")
	
	Presets = PresetFile.node.Players

	print(Presets)
	
def OnDisable():
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

@hook.command("inv", usage="Usage: /inv (save|load|remove|list) <name>")
def OnCommandInv(sender, args):
	if not sender.hasPermission("ore.inv"):
		SendError(sender, "No permission!")
		return True

	if len(args) == 2:
		cmd  = args[0]
		name = args[1]

		player = Presets.Ensure(sender.getName())

		if cmd == "save":
			if len(args) != 2:
				return False

			player[args[1]] = GetItems(sender)

			SendInfo(sender, "Preset " + args[1] + " saved.")

		elif cmd == "load":
			if len(args) != 2:
				return False
		
			if args[1] in player:
				items = player[args[1]]
				SetItems(sender, items)
			
			else:
				SendInfo(sender, "No such preset!")

		elif cmd == "remove":
			if len(args) != 2:
				return False
	
			if args[1] in player:
				del player[args[1]]

				SendInfo(sender, "Removed preset " + args[1])				
			else:
				SendError(sender, "No such preset!")
	
		elif cmd == "list":
			if player:
				sender.sendMessage("Presets:")
	
				for name in player:
					sender.sendMessage("- " + name)		
			else:
				SendError(sender, "No presets!")
	
		else:
			SendError(sender, "Invalid action")

	else:
		SendError(sender, "Usage: /inv (save|load|remove|list) <name>")
			
	return True
