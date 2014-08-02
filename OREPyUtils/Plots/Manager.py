from collections import defaultdict

from .. import PersistentData

import time.ctime as ctime

class PlotStatus:
	FREE     = 0
	CLAIMED  = 1
	RESERVED = 2

	@staticmethod
	def ToStr(status):
		return ["Free", "Claimed", "Reserved"][status]

class PlotBox:
	def __init__(self, node):
		self.node = node

	def __getitem__(self, tuple):
		name = "Plot_%s_%s" % tuple

		if name in self.node:
			return self.node[name]
			
		else:
			plot = Plot()

			self.node[name] = plot

			return plot

	def __delitem__(self, tuple):
		name = "Plot_%s_%s"%tuple

		if name in self.node:
			del self.node[name]

	def __setitem__(self, tuple, value):
		self.node["Plot_%s_%s"%tuple] = value

	def iteritems(self):
		for name, item in self.node.iteritems():
			pos = [int(x) for x in name.split("_")[1:]]
			yield pos, item


class PlayerBox:
	def __init__(self, playerNode):
		self.playerNode = playerNode

	def __getitem__(self, uuid):
		try:
			return self.playerNode[uuid]

		except Exception:
			new = self.playerNode.New(uuid)

			new.remPlots = 1

			return new

	def __iter__(self):
		for uuid in self.playerNode:
			yield uuid


"""
@brief Base class for plot exceptions
"""
class PlotError(Exception):
	pass

"""
@brief Coords are off map
"""
class RangeError(PlotError):
	def __init__(self, pos=None, limit=0):
		self.args = ('Specified plot is out of range',)
		
		if pos:
			self.args[0] += '. (%s,%s) is outside a radius of %s'%pos+(limit,)

"""
@brief Out of plots to claim
"""
class CannotClaimMoreError(PlotError):
	def __init__(self,max=0):
		self.args = ('You cannot claim another plot',)
		
		if max:
			self.args[0] += '. Your limit is %s' % max

"""
@brief Plot is not claimed
"""
class UnclaimedError(PlotError):
	def __init__(self):
		self.args = ('That plot is not claimed',)

"""
@brief Some one else owns this plot
"""
class OwnerError(PlotError):
	def __init__(self, owner=None):
		if owner:
			self.args = ('%s owns this plot' % owner,)
		else:
			self.args = ('This plot is already owned')

"""
@brief dummy error
"""
class DummyError(Exception):
        def __init__(self):
                pass

"""
@brief Represents a single plot
"""
class Plot(PersistentData.Node):
	def __init__(self, node={}):
		self.status = PlotStatus.FREE
		self += node

	"""
	@return whether this plot is claimable.
	"""
	def IsClaimable(self):
		return self.status == PlotStatus.FREE

	"""
	@return whether this plot is claimed.
	"""
	def IsClaimed(self):
		return self.status != PlotStatus.FREE

	"""
	@brief Claim this plot.
	"""
	def Claim(self, owner, ownerUUID, reason):
		if self.status != PlotStatus.RESERVED and not self.IsClaimable():
			raise OwnerError(self.ownerid)
		elif self.status == PlotStatus.RESERVED and str(self.ownerid) != ownerUUID:
                        raise OwnerError(self.ownerid)

		if reason:
			self.reason = reason

		self.status = PlotStatus.CLAIMED
                self.ownerid = str(ownerUUID)
		self.date   = ctime()

	"""
	@brief Reserve this plot.
	"""
	def Reserve(self, owner, ownerUUID, reason):
		if not self.IsClaimable():
			raise OwnerError(owner)

		self.ownerid = str(ownerUUID)
		self.status = PlotStatus.RESERVED
		self.date   = ctime()

		if reason:
			self.reason = reason

	"""
	@return a description of this plot.
	"""
	def Info(self, owner):
		desc = "Status: " + PlotStatus.ToStr(self.status)

		if self.status == PlotStatus.CLAIMED:
			if "reason" in self:
				desc += "\nOwner: " + owner + "\nClaimed at: " + self.date + "\nDescription: " + self.reason
			else:
				desc += "\nOwner: " + owner  + "\nClaimed at: " + self.date
		
		elif self.status == PlotStatus.RESERVED:
			if "reason" in self:
				desc += "\nReservee: " + owner + "\nReserved at: " + self.date + "\nReason: " + self.reason
			else:
				desc += "\nReservee: " + owner + "\nReserved at: " + self.date

		return desc

"""
@brief Keeps track of a collection of plots, and their respective owners
"""
class PlotManager:
	"""
	@brief allow allowed to build on allower's plots 
	"""
	def AddAllowed(self, allower, allowed):
		self.players[str(allower)].Ensure('allowed', [])
		if allowed not in self.players[str(allower)].allowed:
			self.players[str(allower)].allowed.append(allowed)
	
	"""
	@brief no longer allow allowed to build on allower's plots
	"""
	def RemAllowed(self, allower, allowed):
		if 'allowed' in self.players[str(allower)]:
			if allowed in self.players[str(allower)].allowed:
				self.players[str(allower)].allowed.remove(allowed)
			if self.players[str(allower)].allowed:
				del self.players[str(allower)].allowed
	"""
	@return whether someone can build on a plot
	"""
	def CanBuild(self, x, y, uuid):
		all = self.WhoCanBuild(x, y)

		return uuid in all or ('*' in all and '! '+uuid not in all)

	"""
	@return whether the specified plot exists
	"""
	def IsInRange(self, x, y):
		return (x <   self.size.radius) and (y <   self.size.radius) and\
		       (x >= -self.size.radius) and (y >= -self.size.radius)

	"""
	@return get a list of everyone who can build on a plot
	"""
	def WhoCanBuild(self, x, y):
		owner = self.plots[(x, y)].ownerid
		
		return [owner] + self.players[str(owner)].allowed
		
	"""
	@brief Claim the specified plot.
	"""
	def Claim(self, x, y, uuid, name, reason=""):
		plot = self.plots[(x, y)]

                owner = self.players[str(uuid)]
                self.players[str(uuid)].Name = name

		if owner.remPlots == 0:
			raise CannotClaimMoreError() 

                plot.Claim(self.players[str(uuid)].Name, uuid, reason)

                owner.remPlots -= 1
	"""
	@brief Unclaim the specified plot.
	"""
	def Unclaim(self, x, y, uuid):
		plot = self.plots[(x, y)]

		if plot.status in (PlotStatus.CLAIMED, PlotStatus.RESERVED):
			if str(plot.ownerid) == str(uuid):
				del self.plots[(x, y)]

				owner = self.players[str(uuid)]
				owner.remPlots += 1

			else:
				raise OwnerError(self.players[str(plot.ownerid)].Name)
		else:
			raise UnclaimedError()

	"""
	@brief Forcefully unclaim the specified plot.
	"""
	def UnclaimAdmin(self, x, y):
		plot = self.plots[(x, y)]

		if plot.status in (PlotStatus.CLAIMED, PlotStatus.RESERVED):
			owner = self.players[str(plot.ownerid)]
			owner.remplots += 1

		del self.plots[(x,y)]
	
	"""
	@brief Reserve the specified plot.
	"""
	def Reserve(self, x, y, uuid, name, reason=""):
		plot = self.plots[(x, y)]

		owner = self.players[str(uuid)]
		self.players[str(uuid)].Name = name

		plot.Reserve(self.players[str(uuid)].Name, uuid, reason)

	"""
	@return the description of the specified plot.
	"""
	def Info(self, x, y):
                plot = self.plots[(x, y)]

                if 'ownerid' in plot:
                        return "Plot (" + str(x) + ", " + str(y) + ")\n" + plot.Info(self.players[str(plot.ownerid)].Name)
                else:
                      return "Plot (" + str(x) + ", " + str(y) + ")\n" + plot.Info(" ")  

	"""
	@return the number of plots.
	"""
	def GetNumPlots(self):
		return 4 * self.size.radius * self.size.radius

	"""
	@return the coordinates of the plot that contains the specified block.
	"""
	def GetPlotCoords(self, x, z):
		return (x // self.size.x,
		        z // self.size.y)

	"""
	@return the coordinates of the centre of the specified plot.
	"""
	def GetPlotCentre(self, x, y):
		return ((x * self.size.x) + (self.size.x // 2),
		        (y * self.size.y) + (self.size.y // 2))

	"""
	@return Save the plot data.
	"""
	def Save(self, path):
		self.file.Dump()

	def MovePlotMap(self, **attributes):
		for attr, value in attributes.iteritems():
			self.size.Set(attr, value)

	"""
	@return Load the plot data.
	"""
	def LoadOrCreate(self, path):
		self.file = PersistentData.NodeFile(path)

		self.file.node.Ensure("ORE")

		self.file.node.ORE.Ensure("Players")

		self.plotsNode = self.file.node.ORE.Ensure("Plots")

		self.size = self.file.node.ORE.Ensure("Size")

		self.size.Ensure("x", 128)
		self.size.Ensure("y", 128)

		self.size.Ensure("radius", 0)

		self.size.Ensure("pos")
		
		self.size.pos.Ensure("x", 0)
		self.size.pos.Ensure("y", 16)
		self.size.pos.Ensure("z", 0)  
	
		self.players = PlayerBox(self.file.node.ORE.Players)
		
		self.plots = PlotBox(self.plotsNode)
		
		for plot,value in self.plotsNode.iteritems():
			self.plotsNode[plot] = Plot(value)
