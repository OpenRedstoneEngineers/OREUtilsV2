import traceback
import Manager
import Map

from .. import Helper

Info, SendError, SendInfo = Helper.Info, Helper.SendError, Helper.SendInfo

from collections import defaultdict

from org.bukkit.Bukkit import getWorlds

import org.bukkit.Location as Location

"""
Permission nodes:

ore.plot.give
ore.plot.claimas
ore.plot.generate
"""

"""
WorldName(str) <-> Manager
"""
Managers = {}

"""
@brief Get plot coords, either actual, or representative on the map.
"""
def GetCoords_AbsOrMap(x, y, manager):
	if manager.IsOnMap(x, y):
		return manager.MapToPlotCoords(x, y)
	else:
		return manager.GetPlotCoords(x, y)

"""
@brief Get the actual plot coords of a player.
"""
def GetCoords_Player(sender, manager):
	loc = sender.getLocation()

	x = int(loc.getX())
	y = int(loc.getZ())

	return manager.GetPlotCoords(x, y)

"""
@brief Get a player's plot coords, either actual, or representative on the map.
"""
def GetCoords_Player_AbsOrMap(sender, manager):
	loc = sender.getLocation()

	x = int(loc.getX())
	y = int(loc.getZ())

	return GetCoords_AbsOrMap(x, y, manager)
	
"""
@brief Get the coords of the first plot of a player.
"""
def GetCoords_Owner(owner, manager):
	fullName = GetPlayer_Match(owner, manager)

	if not fullName:
		return None

	for pos, plot in manager.plots.iteritems():
		if plot.status == Manager.PlotStatus.CLAIMED:
			if fullName == plot.owner:
				return pos

"""
@brief Retrieve the full name of a player from a partial one.
"""
def GetPlayer_Match(player, manager):
	player = player.lower()

	players = dict((s.lower(), s) for s in manager.players.playerNode)
	
	# Full match
	if player in players:
		return players[player]

	# Partial match
	for match in players:
		if player in match:
			return players[match]

	return None

"""
@brief Get the coords of all plots of a player.
"""
def GetAllCoords_Owner(owner, manager): 
	fullName = GetPlayer_Match(owner, manager)

	if not fullName:
		return []

	Coords = []

	for pos, plot in manager.plots.node.iteritems():
		if plot.status == Manager.PlotStatus.CLAIMED and plot.owner == fullName:
			Coords.append(pos)

	return Coords

"""
@brief Get the plot manager responsible for the world the specified player is in.
"""
def GetManager_ByPlayer(sender):
	return Managers[str(sender.getWorld().getName())]

"""
@brief Initialize the plot manager of the specified world.
"""
def InitManager(world):
	manager = Map.PlotMap(world)

	manager.LoadOrCreate(world.getName() + "/PlotData.json")

	# Generate in-game plot map
	manager.Generate()

	Managers[world.getName()] = manager

	Info("Initialized plot manager %s" % world.getName())

"""
@brief Initialize the plot managers of all loaded worlds.
"""
def InitManagers():
	for world in getWorlds():
		InitManager(world)

"""
@brief Serialize the plot data to disk.
"""
def SaveData():
	for world, manager in Managers.iteritems():
		manager.Save(world + "/PlotData.json")

def GetPlot(sender, args, manager):
	if args:
		try:
			pos = int(args[0]), int(args[1])

			if manager.IsInRange(*pos):
				del args[:2]
				return pos
		except:
			pass

		try:
			index = int(args[1])

		except:
			index = 0

		find = args[0].lower()

		for pos, plot in manager.plots.node.iteritems():
			pos = (int(x) for x in pos.split("_")[1:])

			if "owner"  in plot and find in plot.owner.lower():
				if not index:
					del args[:2]
					return pos
				index -= 1

			if "reason" in plot and find in plot.reason.lower():
				if not index:
					del args[:2]
					return pos
				index -= 1

	pos = GetCoords_Player_AbsOrMap(sender, manager)

	if manager.IsInRange(*pos):
		return pos
		
	SendError(sender, "Unknown plot.")
	return False


@hook.command("pallow", usage="Usage: /pallow <name>")
def OnCommandPallow(sender, args):
	manager = GetManager_ByPlayer(sender)

	name = sender.getName()

	if name not in manager.players:
		SendError(sender, 'You do not own any plots')
		return False

	else:
		if not args:
			SendError(sender, 'You must specifiy a person to allow')
		else:
			manager.AddAllowed(sender, args[0])
			SendInfo(sender, args[0] + ' can build on your plot')

	return True

@hook.command("punallow", usage="Usage: /punallow <name>")
def OnCommandPunallow(sender, args):
	manager = GetManager_ByPlayer(sender) 

	name = sender.getName()

	if name not in manager.players:
		SendError(sender, 'You do not own any plots')
		return True

	else:
		if not args:
			SendError(sender, 'You must specifiy a person to disallow')
		else:
			manager.RemAllowed(sender, args[0])
			SendInfo(sender, args[0]+' cannot build on your plot')

	return True

"""
@brief /pinfo

/pinfo X Z
/pinfo
"""
@hook.command("pinfo", usage="Usage: /pinfo [x] [y]")
def OnCommandPInfo(sender, args):
	manager = GetManager_ByPlayer(sender)

	try:
		x = int(args[0])
		y = int(args[1])

	except:
		pos = GetCoords_Player_AbsOrMap(sender, manager)

		x = pos[0]
		y = pos[1]

	if not manager.IsInRange(x, y):
		SendError(sender, "Out of range.")
		return True

	SendInfo(sender, manager.Info(x, y))

	return True

"""
@brief /pmapmove

/pmapmove X Y Z
"""
@hook.command("pmapmove", usage="Usage: /pmapmove [x] [y] [z]")
def OnCommandPmapmove(sender, args):
	if not sender.hasPermission("ore.plot.mapmove"):
		SendError(sender, "No permission!")
		return True
		
	manager = GetManager_ByPlayer(sender)
	
	if len(args) != 3:
		SendError(sender, "Three arguments (x, y, and z) are required")
		return True
		
	try:
		coords = [int(x) for x in args]
		
	except:
		SendError(sender, "All arguments must be an integer")
		return True
		
	manager.MovePlotMap(**dict(zip(("pos.x", "pos.y", "pos.z"), coords)))
	
	SendInfo(sender, "PlotMap moved to "+" ".join(args))
	return True

"""
@brief /preserve

/preserve X Z
/preserve
"""
@hook.command("preserve", usage="Usage: /preserve [x] [z]")
def OnCommandPreserve(sender, args):
	if not sender.hasPermission("ore.plot.reserve"):
		SendError(sender, "No permission!")
		return True
	
	manager = GetManager_ByPlayer(sender)

	reason = ''

	try:
		x = int(args[0])
		z = int(args[1])
		
		if not manager.IsInRange(x,z):
			SendError(sender, "Out of range")
			return True		

		if len(args) > 2:
			reason = ' '.join(args[2:])
	except:
		x, y = GetCoords_Player_AbsOrMap(sender, manager)
		
		if args:
			reason = ' '.join(args)

	try:
		manager.Reserve(x,y,sender.getName(),reason)
	
	except Manager.PlotError, E:
		SendError(sender, str(E))
		return True
	
	SendInfo(sender, "Plot reserved.")

	manager.MarkReserved(x, y)
	
	return True

"""
@brief /pmap

/pmap X Z
/pmap OwnerName
/pmap
"""
@hook.command("pmap", usage="Usage: /pmap [x] [y] OR /pmap <owner>")
def OnCommandPmap(sender, args):
	manager = GetManager_ByPlayer(sender)

	x, y = GetPlot(sender, args, manager)

	pos = manager.PlotToMapCoords(x, y)

	loc = sender.getLocation()

	loc.setX(pos[0])
	loc.setY(manager.size.pos.y + 1)
	loc.setZ(pos[1])

	sender.teleport(loc)

	return True

"""
@brief /pwarp

/pwarp X Z
/pwarp OwnerName
/pwarp
"""
@hook.command("pwarp", usage="Usage: /pwarp [x] [z] OR /pwarp <owner>")
def OnCommandPwarp(sender, args):
	manager = GetManager_ByPlayer(sender)
	
	try:
		x, y = GetPlot(sender, args, manager)

		pos = manager.GetPlotCentre(x, y)

		loc = sender.getLocation()

		loc.setX(pos[0])
		loc.setZ(pos[1])

		sender.teleport(loc)

		return True

	except:
		traceback.print_exc()

"""
@brief /pclaimas

/pclaimas X Z Name
/pclaimas Name
"""
@hook.command("pclaimas", usage="Usage: /pclaimas [x] [z] <name>")
def OnCommandPclaimAs(sender, args):
	manager = GetManager_ByPlayer(sender)

	x, y = GetPlot(sender, args, manager) 

	try:
		manager.Claim(x, y, name)

	except Manager.PlotError, E:
		SendError(sender, str(E))
		return True
		
	SendInfo(sender, "Plot claimed.")
	manager.MarkClaimed(x, y)
	
	return True

"""
@brief /pclaim

/pclaim X Z
/pclaim
"""
@hook.command("pclaim", usage="Usage: /pclaim [x] [z]")
def OnCommandPclaim(sender, args):
	manager = GetManager_ByPlayer(sender)

	x, y = GetPlot(sender, args, manager) 

	try:

		if args:
			manager.Claim(x, y, sender.getName(), ' '.join(args))
		else:
			manager.Claim(x, y, sender.getName())

	except Manager.PlotError, E:
		SendError(sender, str(E))
		return True

	SendInfo(sender, "Plot claimed.")
	manager.MarkClaimed(x, y)

	return True

"""
@brief /punclaim

/punclaim X Z
/punclaim
"""
@hook.command("punclaim", usage="Usage: /punclaim [x] [z]")
def OnCommandPunclaim(sender, args):
	manager = GetManager_ByPlayer(sender)

	x, y = GetPlot(sender, args, manager) 

	try:
		manager.Unclaim(x, y, sender.getName())

	except Manager.PlotError, E:
		SendError(sender, str(E))
		return True

	SendInfo(sender, "Plot unclaimed.")
	manager.MarkUnclaimed(x, y)

	return True

"""
@brief /pgenerate

/pgenerate Radius
/pgenerate override
/pgenerate
"""
@hook.command("pgenerate", usage="Usage: /pgenerate [radius]")
def OnCommandPgenerate(sender, args):
	manager = GetManager_ByPlayer(sender)

	if not sender.hasPermission("ore.plot.generate"):
		SendError(sender, "No permission!")
		return True

	try:
		manager.size.radius = int(args[0])
	except:
		pass

	manager.Generate()

	SendInfo(sender, "Generated " + str(manager.GetNumPlots()) + " plots")

	return True

"""
@brief /pgive

/pgive Name Amount
"""
@hook.command("pgive", usage="Usage: /pgive <name> <amount>")
def OnCommandPgive(sender, args):
	manager = GetManager_ByPlayer(sender)

	if not sender.hasPermission("ore.plot.give"):
		SendError(sender, "No permission!")
		return True

	if len(args) < 1:
		return False

	info = manager.players[args[0]]

	info.remPlots += 1

	SendInfo(sender, "User " + args[0] + " can now claim " + str(info.remPlots) + " additional plots.")

	return True

"""
@brief /ptake

/ptake Name Amount
"""
@hook.command("ptake", usage="Usage: /ptake <name> <amount>")
def OnCommandPtake(sender, args):
	manager = GetManager_ByPlayer(sender)

	if not sender.hasPermission("ore.plot.give"):
		SendError(sender, "No permission!")
		return True

	if len(args) < 1:
		return False

	info = manager.players[args[0]]

	info.remPlots -= 1

	SendInfo(sender, "User " + args[0] + " can now claim " + str(info.remPlots) + " additional plots.")

	return True

"""
@brief /psearch

/psearch Name
"""
@hook.command("psearch", usage="Usage: /psearch <name>")
def OnCommandPsearch(sender, args):
	manager = GetManager_ByPlayer(sender)

	if len(args) < 1:
		return False

	find = ' '.join(args).lower()

	reasonMatch = []

	SendInfo(sender, "Matches for owner:")

	for pos, plot in manager.plots.node.iteritems():
		pos = "%s, %s" % tuple(pos.split("_")[1:])

		if "owner"  in plot and find in plot.owner.lower():
			SendInfo(sender, pos+"\n"+plot.Info())

		if "reason" in plot and find in plot.reason.lower():
			reasonMatch.append(pos+"\n"+plot.Info())

	SendInfo(sender, "Matches for reason:")

	for reason in reasonMatch:
		SendInfo(sender, reason)

	return True

"""
@brief /pusers

/pusers
"""
@hook.command("pusers", usage="Usage: /pusers")
def OnCommandPusers(sender, args):
	manager = GetManager_ByPlayer(sender)

	if not manager.players:
		SendError(sender, "No users!")

	else:
		names = []

		for name in manager.players:
			names.append(name)

		SendInfo(sender, ', '.join(names))

	return True
