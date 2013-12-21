from collections import defaultdict

from .. import PersistentData

import time.ctime as ctime

from Helper import Info

class PlotStatus:
	FREE     = 0
	CLAIMED  = 1
	RESERVED = 2

	@staticmethod
	def ToStr(status):
		return ["Free", "Claimed", "Reserved"][status]

class PlotBox:
	def __init__(self, plotNode):
		self.Dict = {}
		self.plotNode = plotNode

	def __getitem__(self, tuple):
		try:
			return self.Dict[tuple]
		
		except Exception:
			new  = self.plotNode.New("Plot_%s_%s"%tuple)
			plot = Plot(new)
			self.Dict[tuple] = plot
			new.status = PlotStatus.FREE

			return plot

	def __setitem__(self, tuple, value):
		self.Dict[tuple] = value

class PlayerBox:
	def __init__(self, playerNode):
		self.playerNode = playerNode

	def __getitem__(self, name):
		try:
			return self.playerNode(name)

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
			self.args = ('This plot is already owned',)

"""
@brief Represents a single plot
"""
#would turn to Plot(Node), but import's don't work that way ;-; #They do
class Plot:
	def __init__(self, node):
		self.node = node

	"""
	@return whether this plot is claimable.
	"""
	def IsClaimable(self):
		return self.node.status == PlotStatus.FREE

	"""
	@return whether this plot is claimed.
	"""
	def IsClaimed(self):
		return self.node.status != PlotStatus.FREE
	"""
	@brief Claim this plot.
	"""
	def Claim(self, ownerName, reason):
		if not self.IsClaimable():
			raise OwnerError(self.node.owner)

		self.node.reason = reason

		self.node.status = PlotStatus.CLAIMED

		self.node.owner = ownerName

		self.node.date = ctime()

	"""
	@brief Reserve this plot.
	"""
	def Reserve(self, ownerName, reason):
		if not self.IsClaimable():
			raise OwnerError(self.node.owner)

		self.node.date   = ctime()

		self.node.owner  = ownerName
		
		self.node.reason = reason

		self.node.status = PlotStatus.RESERVED

	"""
	@brief Unclaim this plot.
	"""
	def Unclaim(self):
		if not self.IsClaimed():
			raise UnclaimedError()

		if self.node.status == PlotStatus.RESERVED:
			del self.node.owner
			del self.node.reason
			del self.node.date

		elif self.node.status == PlotStatus.CLAIMED:
			del self.node.owner
			del self.node.date

		self.node.status = PlotStatus.FREE

	"""
	@return a description of this plot.
	"""
	def Info(self):
		desc = "Status: "+PlotStatus.ToStr(self.node.status)

		if   self.node.status == PlotStatus.CLAIMED:
			if self.node.reason != "":
				desc += "\nOwner: "   +self.node.owner+\
				"\nClaimed at: " +self.node.date+"\nDescription: "
			else:
				desc += "\nOwner: "   +self.node.owner+\
				"\nClaimed at: " +self.node.date
		
		elif self.node.status == PlotStatus.RESERVED:
			if self.node.reason != "":
				desc += "\nReservee: "+self.node.owner+\
				"\nReserved at: "+self.node.date+"\nReason: "+self.node.reason
		
			else:
				desc += "\nReservee: "+self.node.owner+\
				"\nReserved at: "+self.node.date
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

		plot.Claim(name,reason)

	"""
	@brief Unclaim the specified plot.
	"""
	def Unclaim(self, x, y, name):
		plot = self.plots[(x, y)]

		if plot.node.status in (PlotStatus.CLAIMED, PlotStatus.RESERVED):
			if plot.node.owner == name:
				plot.Unclaim()

				owner = self.players[name]
				owner.remPlots += 1

			else:
				raise OwnerError(plot.node.owner)
		else:
			raise UnclaimedError

	"""
	@brief Forcefully unclaim the specified plot.
	"""
	def UnclaimAdmin(self, x, y):
		plot = self.plots[(x, y)]

		hasOwner = plot.node.status == PlotStatus.CLAIMED

		if hasOwner:
			owner = self.players[plot.node.owner]

		plot.Unclaim()
	
		if hasOwner:
			owner.remPlots += 1

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

		for name, node in self.plotsNode.iteritems():
			plot = Plot(node)
			print name
			pos  = tuple([int(X) for X in name.split("_")[1:]])

			self.plots[pos] = plot


