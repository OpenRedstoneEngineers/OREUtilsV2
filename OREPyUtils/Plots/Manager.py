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

	def __getitem__(self, name):
		try:
			return self.playerNode[name]

		except Exception:
			new = self.playerNode.New(name)

			new.remPlots = 1

			return new

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
	def Claim(self, ownerName, reason):
		if not self.IsClaimable():
			raise OwnerError(self.owner)

		if reason:
			self.reason = reason

		self.status = PlotStatus.CLAIMED
		self.owner  = ownerName
		self.date   = ctime()

	"""
	@brief Reserve this plot.
	"""
	def Reserve(self, ownerName, reason):
		if not self.IsClaimable():
			raise OwnerError(self.owner)

		self.owner  = ownerName 
		self.status = PlotStatus.RESERVED 
		self.date   = ctime()

		if reason:
			self.reason = reason

	"""
	@return a description of this plot.
	"""
	def Info(self):
		desc = "Status: " + PlotStatus.ToStr(self.status)

		if self.status == PlotStatus.CLAIMED:
			if "reason" in self:
				desc += "\nOwner: " + self.owner + "\nClaimed at: " + self.date + "\nDescription: "
			else:
				desc += "\nOwner: " + self.owner + "\nClaimed at: " + self.date
		
		elif self.status == PlotStatus.RESERVED:
			if "reason" in self:
				desc += "\nReservee: " + self.owner + "\nReserved at: " + self.date + "\nReason: " + self.reason
			else:
				desc += "\nReservee: " + self.owner + "\nReserved at: " + self.date

		return desc

"""
@brief Keeps track of a collection of plots, and their respective owners
"""
class PlotManager:
	"""
	@brief allow allowed to build on allower's plots 
	"""
	def AddAllowed(self, allower, allowed):
		self.players[allower].allowed.add(allowed)
	
	"""
	@brief no longer allow allowed to build on allower's plots
	"""
	def RemAllowed(self, allower, allowed):
		if allowed in self.players[allower].allowed:
			self.players[allower].allowed.remove(allowed)
	"""
	@return whether someone can build on a plot
	"""
	def CanBuild(self, x, y, name):
		all = self.WhoCanBuild(x, y)

		return name in all or ('*' in all and '! '+name not in all)

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
		owner = self.plots[(x, y)].owner
		
		return [owner] + self.players[owner].allowed
		
	"""
	@brief Claim the specified plot.
	"""
	def Claim(self, x, y, name="server",reason=""):
		plot = self.plots[(x, y)]

		owner = self.players[name]

		if owner.remPlots == 0:
			raise CannotClaimMoreError() 

		owner.remPlots -= 1

		plot.Claim(name, reason)

	"""
	@brief Unclaim the specified plot.
	"""
	def Unclaim(self, x, y, name):
		plot = self.plots[(x, y)]

		if plot.status in (PlotStatus.CLAIMED, PlotStatus.RESERVED):
			if plot.owner == name:
				del self.plots[(x, y)]

				owner = self.players[name]
				owner.remPlots += 1

			else:
				raise OwnerError(plot.owner)
		else:
			raise UnclaimedError()

	"""
	@brief Forcefully unclaim the specified plot.
	"""
	def UnclaimAdmin(self, x, y):
		plot = self.plots[(x, y)]

		if plot.status in (PlotStatus.CLAIMED, PlotStatus.RESERVED):
			owner = self.players[plot.owner]
			owner.remplots += 1

		del self.plots[(x,y)]
	
	"""
	@brief Reserve the specified plot.
	"""
	def Reserve(self, x, y, name="server", reason=""):
		plot = self.plots[(x, y)]

		plot.Reserve(name, reason)

	"""
	@return the description of the specified plot.
	"""
	def Info(self, x, y):
		plot = self.plots[(x, y)]

		return "Plot (" + str(x) + ", " + str(y) + ")\n" + plot.Info()

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
		print x, y
		return ((x * self.size.x) + (self.size.x // 2),
		        (y * self.size.y) + (self.size.y // 2))

	"""
	@return Save the plot data.
	"""
	def Save(self, path):
		self.file.Dump()

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
			
