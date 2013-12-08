import Manager
import Map

from Helper import Info

from collections import defaultdict

from org.bukkit.Bukkit import getWorlds

import org.bukkit.Location as Location

"""
Permission nodes:

ore.plot.give
ore.plot.claimas
ore.plot.generate
"""

Managers = defaultdict(Map.PlotMap)

"""
@brief Get plot coords, either actual, or representative on the map
"""
def GetCoords_AbsOrMap(x, y, manager):
	if manager.IsOnMap(x, y):
		return manager.MapToPlotCoords(x, y)

	else:
		return manager.GetPlotCoords(x, y)

"""
@brief Get the actual plot coords of a player
"""
def GetCoords_Player(sender, manager):
	loc = sender.getLocaiton()

	x = int(loc.getX())
	y = int(loc.getZ())

	return manager.GetPlotCoords(x, y)

"""
@brief Get a player's plot coords, either actual, or representative on the map
"""
def GetCoords_Player_AbsOrMap(sender, manager):
	loc = sender.getLocation()

	x = int(loc.getX())
	y = int(loc.getZ())

	return GetCoords_AbsOrMap(x, y, manager)
	
"""
@brief Get the coords of the first plot of a player
"""
def GetCoords_Owner(owner, manager):
	fullName = GetPlayer_Match(owner, manager)
	if not fullName:
		return None
	for pos, plot in manager.plots.iteritems():
		if plot.status == Manager.PlotStatus.CLAIMED:
			if fullName == plot.owner:
				return pos

def GetPlayer_Match(player, manager):
	player = player.lower()
	players = dict((s.lower(),s) for s in manager.players)
	
	if player in players:
		return players[player]
	
	else:
		for match in players:
			if player in match:
				return players[match]
	return None

"""
@brief Get the coords of all plots of a player
"""
def GetAllCoords_Owner(owner, manager):	
	fullName = GetPlayer_Match(owner, manager)
	if not fullName:
		return []
	return [pos for pos, plot in manager.plots.iteritems()\
		if plot.status == Manager.PlotStatus.CLAIMED and\
		plot.owner == owner]
			

#Fucking guess.
def InitManager(world):
	manager = Map.PlotMap(world, 8, (0, 16, 0), 256, 256) # Default params

	manager.LoadOrCreate(world.getName() + "/PlotData.xml")

	manager.Generate()

	manager.Update()

	Managers[world.getName()] = manager

	Info("Initialized plot manager %s" % world.getName())


def InitManagers():
	for world in getWorlds():
		InitManager(world)

def SaveData():
	for world, manager in Managers.iteritems():
		manager.SaveXML(world + "/PlotData.xml")

@hook.command("pallow")
def onCommandPallow(sender, args):
	manager = Managers[sender.getWorld().getName()] 

	name = sender.getName()
	
	if name not in manager.players:
		sender.sendMessage('Who the hell are you?!')
		return False

	else:
		if not args:
			manager.AddAllowed(name, '*')
			sender.sendMessage('All players, unless specifed by /pban, can build on your plot(s)')
		else:
			manager.addallowed(name, args[1])
			sender.sendMessage(args[1]+' can build on your plot(s)')

@hook.command("punallow")
def onCommandPunallow(sender, args):
	manager = Managers[sender.getWorld().getName()]

	name = sender.getName()

	if name not in manager.players:
		sender.sendMessage('Who the hell are you?!')
		return False
	else:
		if not args:
			manager.RemAllowed(name, '*')
			sender.sendMessage('Players cannot build on your plot unless otherwise specified')
		else:
			manager.RemAllowed(name, args[1])
			sender.sendMessage(args[1]+' cannot build on your plot unless otherwise specified')

@hook.command("pwho")
def onCommandPWho(sender, args):

	manager = Managers[sender.getWorld().getName()]
	
	name = sender.getName()

	if name not in manager.players:
		sender.sendMessage('Who the hell are you?!')
		return False

	allowed = []
	banned  = []

	for allow in manager.players[name].allow:
		if  allow.startswith('- '):
			banned.append(allow)
		else:
			allowed.append(allow)

	allowed.sort()
	banned.sort()

	sender.sendMessage('Allowed players:')
	for allow in allowed:
		 sender.sendMessage(' '+allow)

	sender.sendMessage('Banned players:')
	for ban in banned:
		sender.sendMessage(' '+ban)

	
@hook.command("pban")
def onCommandPallow(sender, args):
	manager = Managers[sender.getWorld().getName()]

	name = sender.getName()

	if name not in manager.players:
		sender.sendMessage('Who the hell are you?!')
		return False

	else:
		if not args:
			sender.sendMessage('/pban player')
			return False
		else:
			manager.addallowed(name, '- '+args[1])
			sender.sendMessage(args[1]+' can not build on your plot(s)')


"""
@brief /pinfo

/pinfo X Z
/pinfo
"""
@hook.command("pinfo")
def onCommandPloc(sender, args):
	manager = Managers[sender.getWorld().getName()]

	try:
		x = int(args[0])
		y = int(args[1])

	except:
		pos = GetCoords_Player_AbsOrMap(sender, manager)

		x = pos[0]
		y = pos[1]

	if not manager.IsInRange(x, y):
		sender.sendMessage("Out of range.")
		return True

	sender.sendMessage(manager.Info(x, y))

	return True

"""
@brief /preserve

/preserve X Z
/preserve
"""
@hook.command("preserve")
def onCommandPreserve(sender, args):
	if not sender.hasPermission("ore.plot.reserve"):
		sender.sendMessage("No permission!")
	
	manager = Managers[sender.getWorld().getName()]
	reason = ''
	try:
		x = int(args[0])
		z = int(args[1])
		
		if not manager.IsInRange(x,z):
			sender.sendMessage("Out of range")
		
		if len(args) > 2:
			reason = ' '.join(args[2:])
	except:
		x,y = GetCoords_Player_AbsOrMap(sender, manager)
		
		if args:
			reason = ' '.join(args)

	try:
		manager.Reserve(x,y,sender.getName(),reason)
	
	except Manager.PlotError, E:
		sender.sendMessage(str(E))
		return False
	
        sender.sendMessage("Plot reserved.")
	manager.MarkReserved(x, y)
	
	return True


"""
@brief /pmap

/pmap X Z
/pmap OwnerName
/pmap
"""
@hook.command("pmap")
def onCommandPmap(sender, args):
	manager = Managers[sender.getWorld().getName()]

	try:
		x = int(args[0])
		y = int(args[1])

		if not manager.IsInRange(x, y):
			sender.sendMessage("Out of range.")
			return True

	except:
		if len(args) == 1:
			pos = GetCoords_Owner(args[0], manager)

			if pos == None:
				sender.sendMessage("No such plot.")
				return True

			
			x = pos[0]
			y = pos[1]

		elif len(args) == 2 and args[0].isdigit():
				poses = GetAllCoords_Owner(arg[0], manager)
					
				index = int(args[1])
				
				if index not in range(len(poses)):
			
					sender.sendMessage("No such plot.")
					return True

				x,y = poses[index]

		else:
			pos = GetCoords_Player_AbsOrMap(sender, manager)

			x = pos[0]
			y = pos[1]

			if not manager.IsInRange(x, y):
				sender.sendMessage("Out of range.")
				return True

	pos = manager.PlotToMapCoords(x, y)

	loc = sender.getLocation()

	loc.setX(pos[0])
	loc.setY(manager.mapPos[1] + 1)
	loc.setZ(pos[1])

	sender.teleport(loc)

	return True

"""
@brief /pwarp

/pwarp X Z
/pwarp OwnerName
/pwarp
"""
@hook.command("pwarp")
def onCommandPwarp(sender, args):
	manager = Managers[sender.getWorld().getName()]

	try:
		x = int(args[0])
		y = int(args[1])

		if not manager.IsInRange(x, y):
			sender.sendMessage("Out of range.")
			return True

	except:
		if len(args) == 1:
			pos = GetCoords_Owner(args[0], manager)

			if pos == None:
				sender.sendMessage("No such plot.")
				return True

			x = pos[0]
			y = pos[1]

		if len(args) == 2 and args[1].isdigit():
			poses = GetAllCoords_Owner(args[0], manager)
			
			index = int(args[1])
	
			if index not in range(len(poses)):
				sender.sendMessage("No such plot.")
				return True

			x,y = poses[index]

		else:
			pos = GetCoords_Player_AbsOrMap(sender, manager)

			x = pos[0]
			y = pos[1]

			if not manager.IsInRange(x, y):
				sender.sendMessage("Out of range.")
				return True

	pos = manager.GetPlotCentre(x, y)

	loc = sender.getLocation()

	loc.setX(pos[0])
	loc.setZ(pos[1])

	sender.teleport(loc)

	return True

"""
@brief /pclaimas

/pclaimas X Z Name
/pclaimas Name
"""
@hook.command("pclaimas")
def onCommandPclaimAs(sender, args):
	manager = Managers[sender.getWorld().getName()]

	if not sender.hasPermission("ore.plot.claimas"):
		sender.sendMessage("No permission!")
		return False

	if len(args) < 1:
		return False

	try:
		x = int(args[0])
		y = int(args[1])

		name = str(args[2])

		if not manager.IsInRange(x, y):
			sender.sendMessage("Out of range.")
			return True

	except:
		pos = GetCoords_Player_AbsOrMap(sender, manager)

		x = pos[0]
		y = pos[1]

		name = str(args[0])

	try:
		manager.Claim(x, y, name)
	except Manager.PlotError , E:
		sender.sendMessage(str(E))
		return False
		
	sender.sendMessage("Plot claimed.")
	manager.MarkClaimed(x, y)
	
	return True
"""
@brief /pclaim

/pclaim X Z
/pclaim
"""
@hook.command("pclaim")
def onCommandPclaim(sender, args):
	manager = Managers[sender.getWorld().getName()]

	try:
		x = int(args[0])
		y = int(args[1])

		if not manager.IsInRange(x, y):
			sender.sendMessage("Out of range.")
			return True

	except:
		pos = GetCoords_Player_AbsOrMap(sender, manager)

		x = pos[0]
		y = pos[1]

	try:
		manager.Claim(x, y, sender.getName())
	except Manager.PlotError  , E:
		sender.sendMessage(str(E))
		return False

	sender.sendMessage("Plot claimed.")
	manager.MarkClaimed(x, y)

	return True

"""
@brief /punclaim

/punclaim X Z
/punclaim
"""
@hook.command("punclaim")
def onCommandPunclaim(sender, args):
	manager = Managers[sender.getWorld().getName()]

	try:
		x = int(args[0])
		y = int(args[1])

		if not manager.IsInRange(x, y):
			sender.sendMessage("Out of range.")
			return True

	except:
		pos = GetCoords_Player_AbsOrMap(sender, manager)

		x = pos[0]
		y = pos[1]

	try:
		manager.Unclaim(x, y, sender.getName())
	except Manager.PlotError  , E:
		sender.sendMessage(str(E))
		return False

	sender.sendMessage("Plot unclaimed.")
	manager.MarkUnclaimed(x, y)

	return True

"""
@brief /pgenerate

/pgenerate Radius
"""
@hook.command("pgenerate")
def onCommandPgenerate(sender, args):
	manager = Managers[sender.getWorld().getName()]

	if not sender.hasPermission("ore.plot.generate"):
		sender.sendMessage("No permission!")
		return True

	if len(args) < 1:
		return False

	try:
		manager.radius = int(args[0])
	except:
		return False

	manager.Generate()
	manager.Update()

	sender.sendMessage("Generated "+str(manager.GetNumPlots())+" plots")

	return True

"""
@brief /pgive

/pgive Name
"""
@hook.command("pgive")
def onCommandPgive(sender, args):
	manager = Managers[sender.getWorld().getName()]

	if not sender.hasPermission("ore.plot.give"):
		sender.sendMessage("No permission!")
		return True

	if len(args) < 1:
		return False

	info = manager.players.get(args[0])

	if info == None:
		sender.sendMessage("No such user.")
		return True

	info.remPlots += 1

	sender.sendMessage("User " + args[0] + " can now claim " + str(info.remPlots) + " additional plots.")

	return True

"""
@brief /ptake

/ptake Name
"""
@hook.command("ptake")
def onCommandPtake(sender, args):
	manager = Managers[sender.getWorld().getName()]

	if not sender.hasPermission("ore.plot.give"):
		sender.sendMessage("No permission!")
		return True

	if len(args) < 1:
		return False

	info = manager.players.get(args[0])

	if info == None:
		sender.sendMessage("No such user.")
		return True

	info.remPlots -= 1

	sender.sendMessage("User " + args[0] + " can now claim " + str(info.remPlots) + " additional plots.")

	return True

"""
@brief /psearch

/psearch Name
"""
@hook.command("psearch")
def onCommandPsearch(sender, args):
	manager = Managers[sender.getWorld().getName()]

	if len(args) < 1:
		return False

	owner = str(args[0])

	for pos, plot in manager.plots.iteritems():
		if plot.status == Manager.PlotStatus.CLAIMED:
			if plot.owner == owner:
				sender.sendMessage(manager.Info(pos[0], pos[1]))

	return True

"""
@brief /pusers

/pusers
"""
@hook.command("pusers")
def onCommandPusers(sender, args):
	manager = Managers[sender.getWorld().getName()]

	names = []

	for name in manager.players.iterkeys():
		names.append(name)

	sender.sendMessage(', '.join(names))

	return True
