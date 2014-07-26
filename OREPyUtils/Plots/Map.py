import Manager

import xml.etree.ElementTree as ET

from .. import Helper

class PlotMap(Manager.PlotManager):
	def __init__(self, world):
		self.BLOCK_RESERVED       = Config["PlotMap.TopBlocks.Reserved"]
		self.BLOCK_ON             = Config["PlotMap.TopBlocks.On"]
		self.BLOCK_OFF            = Config["PlotMap.TopBlocks.Off"]
		self.BLOCK_FRAME_X        = Config["PlotMap.TopBlocks.Frame.X"]
		self.BLOCK_FRAME_Y        = Config["PlotMap.TopBlocks.Frame.Y"]
		self.BLOCK_FRAME_CROSS    = Config["PlotMap.TopBlocks.Frame.Cross"]
		self.BLOCK_BASE           = Config["PlotMap.TopBlocks.Base"]
		self.BLOCK_BELOW_ON       = Config["PlotMap.BottomBlocks.On"]
		self.BLOCK_BELOW_OFF      = Config["PlotMap.BottomBlocks.Off"]
		self.BLOCK_BELOW_RESERVED = Config["PlotMap.BottomBlocks.Reserved"]
		self.world = world

	"""
	@return if specified plot coords are on the map
	"""
	def IsOnMap(self, x, z):
		return abs(x - self.size.pos.x) < (self.size.radius * 3) and\
		       abs(z - self.size.pos.z) < (self.size.radius * 3)

	"""
	@return the physical location of a plot on the map
	"""
	def PlotToMapCoords(self, x, y):
		newX = x * 3
		newY = y * 3

		if x < 0:
			newX -= 1
		else:
			newX += 1

		if y < 0:
			newY -= 1
		else:
			newY += 1

		return (newX + self.size.pos.x + 2, newY + self.size.pos.z + 2)

	"""
	@return the plot coords of a physical location on the map
	"""
	def MapToPlotCoords(self, x, y):
		newX = x - self.size.pos.x
		newY = y - self.size.pos.z

		if newX > 0:
			newX -= 2

		if newY > 0:
			newY -= 2

		return (newX // 3, newY // 3)
	"""
	@brief Mark the frame for a plot
	"""
	def MarkPlotFrame(self, x, y):
		position = self.PlotToMapCoords(x, y)

		self.world.getBlockAt(position[0] - 2, self.size.pos.y, position[1]    ).setTypeIdAndData(*self.BLOCK_FRAME_Y)
		self.world.getBlockAt(position[0] - 2, self.size.pos.y, position[1] - 1).setTypeIdAndData(*self.BLOCK_FRAME_Y)
		self.world.getBlockAt(position[0],     self.size.pos.y, position[1] - 2).setTypeIdAndData(*self.BLOCK_FRAME_X)
		self.world.getBlockAt(position[0] - 1, self.size.pos.y, position[1] - 2).setTypeIdAndData(*self.BLOCK_FRAME_X)

		if x == self.size.radius-1:
			self.world.getBlockAt(position[0] + 1, self.size.pos.y, position[1]    ).setTypeIdAndData(*self.BLOCK_FRAME_Y)
			self.world.getBlockAt(position[0] + 1, self.size.pos.y, position[1] - 1).setTypeIdAndData(*self.BLOCK_FRAME_Y)

		if y == self.size.radius-1:
			self.world.getBlockAt(position[0],     self.size.pos.y, position[1] + 1).setTypeIdAndData(*self.BLOCK_FRAME_X)
			self.world.getBlockAt(position[0] - 1, self.size.pos.y, position[1] + 1).setTypeIdAndData(*self.BLOCK_FRAME_X)


		self.world.getBlockAt(position[0] - 2, self.size.pos.y, position[1] - 2).setTypeIdAndData(*self.BLOCK_FRAME_CROSS)

	"""
	@brief Mark the plot at the specified position as reserved.
	"""
	def MarkReserved(self, x, y, frame=False):
		if frame:
			self.MarkPlotFrame(x, y)

		position = self.PlotToMapCoords(x, y)

		self.world.getBlockAt(position[0],     self.size.pos.y, position[1]    ).setTypeIdAndData(*self.BLOCK_RESERVED)
		self.world.getBlockAt(position[0] - 1, self.size.pos.y, position[1]    ).setTypeIdAndData(*self.BLOCK_RESERVED)
		self.world.getBlockAt(position[0],     self.size.pos.y, position[1] - 1).setTypeIdAndData(*self.BLOCK_RESERVED)
		self.world.getBlockAt(position[0] - 1, self.size.pos.y, position[1] - 1).setTypeIdAndData(*self.BLOCK_RESERVED)
		self.world.getBlockAt(position[0],     self.size.pos.y - 1, position[1]    ).setTypeIdAndData(*self.BLOCK_BELOW_RESERVED)
		self.world.getBlockAt(position[0] - 1, self.size.pos.y - 1, position[1]    ).setTypeIdAndData(*self.BLOCK_BELOW_RESERVED)
		self.world.getBlockAt(position[0],     self.size.pos.y - 1, position[1] - 1).setTypeIdAndData(*self.BLOCK_BELOW_RESERVED)
		self.world.getBlockAt(position[0] - 1, self.size.pos.y - 1, position[1] - 1).setTypeIdAndData(*self.BLOCK_BELOW_RESERVED)
	"""
	@brief Mark the plot at the specified position as claimed.
	"""
	def MarkClaimed(self, x, y, frame=False):
		if frame:
			self.MarkPlotFrame(x, y)

		position = self.PlotToMapCoords(x, y)

		self.world.getBlockAt(position[0],     self.size.pos.y, position[1]    ).setTypeIdAndData(*self.BLOCK_ON)
		self.world.getBlockAt(position[0] - 1, self.size.pos.y, position[1]    ).setTypeIdAndData(*self.BLOCK_ON)
		self.world.getBlockAt(position[0],     self.size.pos.y, position[1] - 1).setTypeIdAndData(*self.BLOCK_ON)
		self.world.getBlockAt(position[0] - 1, self.size.pos.y, position[1] - 1).setTypeIdAndData(*self.BLOCK_ON)
		self.world.getBlockAt(position[0],     self.size.pos.y - 1, position[1]    ).setTypeIdAndData(*self.BLOCK_BELOW_ON)
		self.world.getBlockAt(position[0] - 1, self.size.pos.y - 1, position[1]    ).setTypeIdAndData(*self.BLOCK_BELOW_ON)
		self.world.getBlockAt(position[0],     self.size.pos.y - 1, position[1] - 1).setTypeIdAndData(*self.BLOCK_BELOW_ON)
		self.world.getBlockAt(position[0] - 1, self.size.pos.y - 1, position[1] - 1).setTypeIdAndData(*self.BLOCK_BELOW_ON)

	"""
	@brief Mark the plot at the specified position as unclaimed.
	"""
	def MarkUnclaimed(self, x, y, frame=False):
		if frame:
			self.MarkPlotFrame(x, y)

		position = self.PlotToMapCoords(x, y)

		self.world.getBlockAt(position[0],     self.size.pos.y, position[1]    ).setTypeIdAndData(*self.BLOCK_OFF)
		self.world.getBlockAt(position[0] - 1, self.size.pos.y, position[1]    ).setTypeIdAndData(*self.BLOCK_OFF)
		self.world.getBlockAt(position[0],     self.size.pos.y, position[1] - 1).setTypeIdAndData(*self.BLOCK_OFF)
		self.world.getBlockAt(position[0] - 1, self.size.pos.y, position[1] - 1).setTypeIdAndData(*self.BLOCK_OFF)
		self.world.getBlockAt(position[0],     self.size.pos.y - 1, position[1]    ).setTypeIdAndData(*self.BLOCK_BELOW_OFF)
		self.world.getBlockAt(position[0] - 1, self.size.pos.y - 1, position[1]    ).setTypeIdAndData(*self.BLOCK_BELOW_OFF)
		self.world.getBlockAt(position[0],     self.size.pos.y - 1, position[1] - 1).setTypeIdAndData(*self.BLOCK_BELOW_OFF)
		self.world.getBlockAt(position[0] - 1, self.size.pos.y - 1, position[1] - 1).setTypeIdAndData(*self.BLOCK_BELOW_OFF)

	"""
	@brief Generate a plot map with the specified size.
	"""
	def Generate(self):
		for x in xrange(-self.size.radius, self.size.radius):
			for y in xrange(-self.size.radius, self.size.radius):
				if "Plot_%s_%s"%(x, y) in self.plots.node:
					status = self.plots[(x, y)].status

					if status == Manager.PlotStatus.FREE:
						self.MarkUnclaimed(x, y, frame=True)
	
					elif status == Manager.PlotStatus.CLAIMED:
						self.MarkClaimed(x, y, frame=True)
	
					elif status == Manager.PlotStatus.RESERVED:
						self.MarkReserved(x, y, frame=True)
				else:
					self.MarkUnclaimed(x, y, frame=True)
				
		Helper.Info("Generated map")
