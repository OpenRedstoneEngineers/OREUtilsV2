from collections import defaultdict

import xml.etree.ElementTree as ET

import org.apache.xerces.parsers.SAXParser as Parser
import xml.parsers.expat as Evil
Evil._xerces_parser = Parser

import time.ctime as ctime

from Helper import Info

class PlotStatus:
	FREE     = 0
	CLAIMED  = 1
	RESERVED = 2

	@staticmethod
	def ToStr(status):
		return ["Free", "Claimed", "Reserved"][status]

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
class Plot:
	def __init__(self, status = PlotStatus.FREE):
		self.status = status

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

		self.reason = reason

		self.status = PlotStatus.CLAIMED

		self.owner = ownerName

		self.date = ctime()

	"""
	@brief Reserve this plot.
	"""
	def Reserve(self, ownerName, reason):
		if not self.IsClaimable():
			raise OwnerError(self.owner)

		self.date   = ctime()

		self.owner  = ownerName
		
		self.reason = reason

		self.status = PlotStatus.RESERVED

	"""
	@brief Unclaim this plot.
	"""
	def Unclaim(self):
		if not self.IsClaimed():
			raise UnclaimedError()

		if self.status == PlotStatus.RESERVED:
			del self.owner
			del self.reason
			del self.date

		elif self.status == PlotStatus.CLAIMED:
			del self.owner
			del self.date

		self.status = PlotStatus.FREE

	"""
	@return a description of this plot.
	"""
	def Info(self):
		desc = "Status: "+PlotStatus.ToStr(self.status)

		if   self.status == PlotStatus.CLAIMED:
			if self.reason != "":
				desc += "\nOwner: "   +self.owner+"\nClaimed at: " +self.date+"\nDescription: "
			else:
				desc += "\nOwner: "   +self.owner+"\nClaimed at: " +self.date
		
		elif self.status == PlotStatus.RESERVED:
			if self.reason != "":
				desc += "\nReservee: "+self.owner+"\nReserved at: "+self.date+"\nReason: "+self.reason
		
			else:
				desc += "\nReservee: "+self.owner+"\nReserved at: "+self.date
		return desc

	"""
	@brief Convert a plot object to an XML tree.
	"""
	def Serialize(self, x, y):
		node = ET.Element("Plot")

		node.set("x", str(x))
		node.set("y", str(y))

		status = ET.SubElement(node, "Status")

		status.text = str(self.status)

		if self.status in (PlotStatus.CLAIMED, PlotStatus.RESERVED):
			owner       = ET.SubElement(node, "Owner")
			date        = ET.SubElement(node, "Date")
			reason      = ET.SubElement(node, "Reason")
			
			owner.text  = self.owner
			date.text   = self.date
			reason.text = self.reason

		return node

	"""
	@brief Convert an XML tree to a plot object.
	"""
	def Deserialize(self, node):
		pos = (int(node.get("x")),
		       int(node.get("y")))

		self.status = int(node.find("Status").text)

		if self.status in (PlotStatus.CLAIMED, PlotStatus.RESERVED):
			self.owner  = node.find("Owner").text
			self.date   = node.find("Date").text
			self.reason = node.find("Reason").text

		return pos

class PlayerInfo:
	def __init__(self, remPlots = 1, allowed = set()):
		self.remPlots = remPlots
		self.allowed  = allowed

	"""
	@brief Convert a player info object to an XML tree.
	"""
	def Serialize(self, name):
		node = ET.Element("Player")

		node.set("name", name)

		remPlots = ET.SubElement(node, "RemPlots")
		allowed  = ET.SubElement(node, "Allowed") 

		remPlots.text = str(self.remPlots)
		allowed.text  = str(list(self.allowed))

		return node

	"""
	@brief Convert an XML tree to a player info object.
	"""
	def Deserialize(self, node):
		name = node.get("name")

		self.remPlots = int(node.find("RemPlots").text)
		self.allowed  = set(list(node.find("Allowed").text))
		
		return name

"""
@brief Keeps track of a collection of plots, and their respective owners
"""
class PlotManager:
	def __init__(self, radius, plotx, ploty):
		self.radius = radius
		self.plotx  = plotx
		self.ploty  = ploty

		self.plots = defaultdict(Plot)

		self.players = defaultdict(PlayerInfo)

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
		return (x < self.radius) and (y < self.radius) and (x >= -self.radius) and (y >= -self.radius)

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

		if plot.status in (PlotStatus.CLAIMED,PlotStatus.RESERVED):
			if plot.owner == name:
				plot.Unclaim()

				owner = self.players[name]
				owner.remPlots += 1

			else:
				raise OwnerError(plot.owner)
		else:
			raise UnclaimedError

	"""
	@brief Forcefully unclaim the specified plot.
	"""
	def UnclaimAdmin(self, x, y):
		plot = self.plots[(x, y)]

		hasOwner = plot.status == PlotStatus.CLAIMED

		if hasOwner:
			owner = self.players[plot.owner]

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

		return "Plot ("+str(x)+", "+str(y)+")\n"+plot.Info()

	"""
	@return the number of plots.
	"""
	def GetNumPlots(self):
		return 4 * self.radius * self.radius

	"""
	@return the coordinates of the plot that contains the specified block.
	"""
	def GetPlotCoords(self, x, z):
		return (x // self.plotx,
		        z // self.ploty)

	"""
	@return the coordinates of the centre of the specified plot.
	"""
	def GetPlotCentre(self, x, y):
		return ((x * self.plotx) + (self.plotx // 2),
		        (y * self.ploty) + (self.ploty // 2))

	"""
	@brief Serialize the plot data
	"""
	def Serialize(self, root):
		plotsNode = ET.SubElement(root, "Plots")

		for pos, plot in self.plots.iteritems():
			plotsNode.append(plot.Serialize(pos[0], pos[1]))

		playersNode = ET.SubElement(root, "Players")

		for name, info in self.players.iteritems():
			playersNode.append(info.Serialize(name))

		sizeNode = ET.SubElement(root, "PlotSize")

		sizeNode.set("x", str(self.plotx))
		sizeNode.set("y", str(self.ploty))

	"""
	@brief Deserialize the plot data
	"""
	def Deserialize(self, root):
		plotsNode = root.find("Plots")

		for node in plots.findall("Plot"):
			plot = Plot()

			pos = plot.Deserialize(node)

			self.plots[pos] = plot

		playersNode = root.find("Players")

		for node in players.findall("Player"):
			info = PlayerInfo()

			name = info.Serialize(node)

			self.players[name] = info

		sizeNode = root.find("PlotSize")

		self.plotx = int(sizeNode.get("x"))
		self.ploty = int(sizeNode.get("y"))

	"""
	@return Save the plot data.
	"""
	def SaveXML(self, path):
		root = ET.Element("ORE")

		self.Serialize(root)

		f = open(path)

		f.write(ET.tostring(root))

		f.close()

	"""
	@return Load the plot data.
	"""
	def LoadXML(self, path):
		f = open(path)
		
		root = ET.parse(f)#FUCK YOU

		f.close()

		self.Deserialize(root.find("ORE"))	

	"""
	@brief Try to load the plot data, but if the specified file doesn't exist, create it.
	"""
	def LoadOrCreate(self, path):
		try:
			self.LoadXML(path)

		except Exception:
			Info("Creating empty plot data file " + path)

			self.SaveXML(path)

