import traceback
import Manager
import Map

from .. import Helper

Info, SendError, SendInfo, SendF = Helper.Info, Helper.SendError, Helper.SendInfo, Helper.SendF

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
        try:
                return Managers[str(sender.getWorld().getName())]
        except:
                SendError(sender, "Cannot run command as console!")

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
			index = int(args[1])-1
		except:
			index = 0

		find = str(args[0]).lower()
                checked = 0

		for pos, plot in manager.plots.node.iteritems():
			pos = (int(x) for x in pos.split("_")[1:])

			if "ownerid"  in plot and find in str(getNameFromUUID(sender, plot.ownerid)).lower():
				if index == checked:
					del args[:2]
					return pos
				checked += 1

			if "reason" in plot and find in plot.reason.lower():
				if index == checked:
					del args[:2]
					return pos
				checked += 1

	pos = GetCoords_Player_AbsOrMap(sender, manager)

	if manager.IsInRange(*pos):
		return pos
		
	SendError(sender, "Unknown plot.")
	return False
"""
@brief returns a user's name from the uuid's of the current online users and the local database
"""
def getNameFromUUID(sender, uuid):
        manager = GetManager_ByPlayer(sender)
        if uuid in manager.players:
                return manager.players[str(uuid)].Name
        
        raise Exception
        
"""
@brief returns a user's UUID from the names of the current online users and the local database
"""
def getUUIDFromName(sender, ownname):
        manager = GetManager_ByPlayer(sender)

        for uuid in manager.players:
                if "Name" in manager.players[str(uuid)] and manager.players[str(uuid)].Name == ownname:
                        return str(uuid)
        raise Exception

"""
@breif update database
"""
@hook.event("player.PlayerJoinEvent", "Normal")
def OnPlayerJoinEvent(event):
        try:
                sender = event.getPlayer()
                manager = GetManager_ByPlayer(sender)
                uuid = sender.getUniqueId()
                uuid = str(uuid)
           	
                if uuid in manager.players and "Name" in manager.players[str(uuid)] and manager.players[str(uuid)].Name != sender.getName():
                        sender.sendMessage(Colorify('6Change in name detected! Old name: &9%s' % manager.players[str(uuid)].Name))
                        manager.players[str(uuid)].Name = sender.getName()
                elif uuid in manager.players and "Name" not in manager.players[str(uuid)]:
                        manager.players[str(uuid)].Name = sender.getName()
        
                return True
        except Exception as E:
                SendError(event.getPlayer(), str(E))
                return True
        
@hook.command("pallow", usage="Usage: /pallow <name>")
def OnCommandPallow(sender, args):
	manager = GetManager_ByPlayer(sender)

	uuid = str(sender.getUniqueId())
	
	if uuid not in manager.players:
		SendError(sender, 'You do not own any plots')
		return True

	else:
		if not args:
			SendError(sender, 'You must specifiy a person to allow')
		else:
			manager.AddAllowed(sender, args[0])
			sender.sendMessage(Colorify('&9'+args[0]+'&6 can now build on your plot'))
	
			manager.AddAllowed(uuid, '*')
			sender.sendMessage(Colorify('&6All players, unless specifed by &c/punallow&6, can build on your plot(s)'))
		else:
                        try:
                                manager.AddAllowed(uuid, getUUIDFromName(sender, str(args[0])))
                                sender.sendMessage(Colorify('&9'+args[0]+'&6 can build on your plot(s)'))
                        except Exception as E:
                                SendError(sender, 'User does not appear in our database!')

			manager.AddAllowed(name, args[0])
			sender.sendMessage(Colorify('&9'+args[0] + '&6 can build on your plot(s)'))

	return True

@hook.command("punallow", usage="Usage: /punallow <name>")
def OnCommandPunallow(sender, args):
	manager = GetManager_ByPlayer(sender) 

	uuid = str(sender.getUniqueId())

	if uuid not in manager.players:
		SendError(sender, 'You do not own any plots')
		return True

	else:
		if not args:
			SendError(sender, 'You must specifiy a person to disallow')
		else:
			manager.RemAllowed(sender, args[0])
			sender.sendMessage(Colorify('&9'+args[0]+'&6 cannot build on your plot'))

	return True
"""
@brief /pinfo

/pinfo X Z
/pinfo
"""
@hook.command("pinfo", usage="Usage: /pinfo [x] [y]")
def onCommandPInfo(sender, args):
        manager = GetManager_ByPlayer(sender)

        try:
                x = int(args[0])
                y = int(args[1])
        except:
                pos = GetCoords_Player_AbsOrMap(sender, manager)
                x = pos[0]
                y = pos[1]
        try:
                if not manager.IsInRange(x, y):
                        SendError(sender, "Out of range.")
                        return True

                sender.sendMessage(Colorify('&e'+manager.Info(x, y)))
	except Exception as E:
                SendError(sender ,str(E))

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
	
	sender.sendMessage(Colorify("&ePlotMap moved to &5"+" ".join(args)))
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
                manager.Reserve(x,y,sender.getUniqueId(), sender.getName(), reason)
	except Manager.PlotError, E:
		SendError(sender, str(E))
		return True
	
	sneder.sendMessage(Colorify("&6Plot reserved."))
        print("%s reserved plot %s,%s"%(sender.getName(), x, y))	

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
@hook.command("pwarp", usage="Usage: /pwarp [x] [z] OR /pwarp <owner> <plot number>")
def OnCommandPwarp(sender, args):
	manager = GetManager_ByPlayer(sender)
	
	try:
		x, y = GetPlot(sender, args, manager)

		pos = manager.GetPlotCentre(x, y)

		loc = sender.getLocation()

		loc.setX(pos[0])
		loc.setY(manager.size.pos.y + 1)
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
def onCommandPclaimAs(sender, args):
        manager = GetManager_ByPlayer(sender)
        x, y = GetPlot(sender, args, manager)
        name = ''

        if len(args) == 3:
                name = str(args[2])
        elif len(args) == 1:
                name = str(args[0])
        else:
                return False

	try:
		manager.Claim(x, y, getUUIDFromName(sender, name), name)
        except Exception as E:
                SendError(sender, str(E))
                return True
	except Manager.PlotError, E:
		SendError(sender, str(E))
		return True
        try:
                sender.sendMessage(Colorify("&6Plot claimed."))
                print("%s claimed plot %s,%s as %s"%(sender.getName(), x, y, name))  
                manager.MarkClaimed(x, y)
        except Exception as E:
                SendError(sender, str(E))

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
			manager.Claim(x, y, str(sender.getUniqueId()), sender.getName(), ' '.join(args))
		else:
			manager.Claim(x, y, str(sender.getUniqueId()), sender.getName())

	except Manager.PlotError, E:
		SendError(sender, str(E))
		return True

	sender.sendMessage(Colorify("&6Plot claimed."))
	print("%s claimed plot %s,%s"%(sender.getName(), x, y))
	manager.MarkClaimed(x, y)

	return True

"""
@brief /punclaim

/punclaim X Z
/punclaim
"""
@hook.command("punclaim", usage="Usage: /punclaim [x] [z]")
def onCommandPunclaim(sender, args):
        manager = GetManager_ByPlayer(sender)
        x, y = GetPlot(sender, args, manager)

	try:
		manager.Unclaim(x, y, sender.getUniqueId(), sender.getName())
	except Manager.PlotError, E:
		SendError(sender, str(E))
		return True
	
        sender.sendMessage(Colorify("&6Plot unclaimed."))
        print("%s unclaimed plot %s,%s"%(sender.getName(), x, y))
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

	sender.sendMessage(Colorify("&eGenerated &5" + str(manager.GetNumPlots()) + "&e plots"))

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
        try:
                info = manager.players[getUUIDFromName(sender, args[0])]
        except Exception:
                SendError(sender, 'User does not appear in our database!')
                return True

	if len(args) > 1:
                info.remPlots += int(args[1])
        else:
                info.remPlots += 1

	sender.sendMessage(Colorify("&eUser &9" + args[0] + "&e can now claim &5" + str(info.remPlots) + "&e additional plots."))

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

        try:
                info = manager.players[getUUIDFromName(sender, args[0])]
        except Exception:
                SendError(sender, 'User does not appear in our database!')
                return True
        if len(args) > 1:
                info.remPlots -= int(args[1])
        else:
                info.remPlots -= 1

        if info.remPlots < 0:
                sender.sendMessage(Colorify("&eUser already at &50&e plots!"))
        else:
                sender.sendMessage(Colorify("&eUser &9" + args[0] + "&e can now claim &5" + str(info.remPlots) + "&e additional plots."))

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

        find = str(args[0])

	reasonMatch = []

	sender.sendMessage(Colorify("&6Matches for owner:"))
	for pos, plot in manager.plots.node.iteritems():

		pos = "%s, %s"%tuple(pos.split("_")[1:])
		try:
                        if "ownerid"  in plot and str(plot.ownerid) == str(getUUIDFromName(sender, find)):
                                sender.sendMessage(Colorify("&5"+pos+"\n&e"+plot.Info(find)))
                except Exception as E:
                        SendError(sender, str(E))
                        return True
		if "reason" in plot and find in plot.reason.lower():
			reasonMatch.append(pos+"\n"+plot.Info(find))

	sender.sendMessage(Colorify("&6Matches for reason:"))

	for reason in reasonMatch:
		sender.sendMessage(Colorify('&6'+reason))

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

                for uuid in manager.players:
                        names.append(str(getNameFromUUID(sender, uuid)))

                sender.sendMessage(Colorify('&9'+', '.join(names)))
                
	return True
