from collections import defaultdict

import PersistentData as Data

"""
Permission nodes:

ore.inv
"""

PresetFile = Data.NodeFile("changeme.jpg")
Presets = PresetFile.node

def GetItems(player):
	inv = player.getInventory()

	items = []

	for slot in xrange(9):
		items.append(inv.getItem(slot))

	return items

def SetItems(player, items):
	inv = player.getInventory()

	slot = 0

	for item in items:
		inv.setItem(slot, item)

		slot += 1

@hook.command("inv", usage="Usage: /inv (save|load|remove|list|clear) <name>")
def onCommandInv(sender, args):
	if not sender.hasPermission("ore.inv"):
		sender.sendMessage("No permission!")
		return True

	if not args:
		return False

	cmd = args[0]

	player = Presets.Ensure(sender.getName())

	if cmd == "save":
		if len(args) != 2:
			return False

		player[args[1]] = GetItems(sender)

		sender.sendMessage("Preset " + args[1] + " saved.")

		return True

	elif cmd == "load":
		if len(args) != 2:
			return False

		items = player.get(args[1])

		if items == None:
			sender.sendMessage("No such preset!")
			return True

		SetItems(sender, items)

		return True

	elif cmd == "remove":
		if len(args) != 2:
			return False

		if args[1] in player:
			del player[args[1]]

			sender.sendMessage("Removed preset " + args[1])
		else:
			sender.sendMessage("No such preset!")

		return True

	elif cmd == "list":
		if player:
			sender.sendMessage("Presets:")

			for name in player.iterkeys():
				sender.sendMessage("- " + name)		
		else:
			sender.sendMessage("No presets!")

		return True

	elif cmd == "clear":
		player.clear()

		return True

	return False
