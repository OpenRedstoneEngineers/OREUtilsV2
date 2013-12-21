import Manager

import xml.etree.ElementTree as ET

from Helper import Info

class PlotMap(Manager.PlotManager):
	BLOCK_RESERVED    = (159,10, 0)
	BLOCK_ON          = (159, 3, 0)
	BLOCK_OFF         = (159, 0, 0)
	BLOCK_FRAME_X     = (1,   0, 0)
	BLOCK_FRAME_Y     = (1,   0, 0)
	BLOCK_FRAME_CROSS = (1,   0, 0)
	BLOCK_BASE        = (1,   0, 0)

	def __init__(self, world):
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

		self.world.getBlockAt(position[0] - 2, self.size.pos.y, position[1]    ).setTypeIdAndData(*PlotMap.BLOCK_FRAME_Y)
		self.world.getBlockAt(position[0] - 2, self.size.pos.y, position[1] - 1).setTypeIdAndData(*PlotMap.BLOCK_FRAME_Y)
		self.world.getBlockAt(position[0],     self.size.pos.y, position[1] - 2).setTypeIdAndData(*PlotMap.BLOCK_FRAME_X)
		self.world.getBlockAt(position[0] - 1, self.size.pos.y, position[1] - 2).setTypeIdAndData(*PlotMap.BLOCK_FRAME_X)

		if x == self.size.radius-1:
			self.world.getBlockAt(position[0] + 1, self.size.pos.y, position[1]    ).setTypeIdAndData(*PlotMap.BLOCK_FRAME_Y)
			self.world.getBlockAt(position[0] + 1, self.size.pos.y, position[1] - 1).setTypeIdAndData(*PlotMap.BLOCK_FRAME_Y)

		if y == self.size.radius-1:
			self.world.getBlockAt(position[0],     self.size.pos.y, position[1] + 1).setTypeIdAndData(*PlotMap.BLOCK_FRAME_X)
			self.world.getBlockAt(position[0] - 1, self.size.pos.y, position[1] + 1).setTypeIdAndData(*PlotMap.BLOCK_FRAME_X)


		self.world.getBlockAt(position[0] - 2, self.size.pos.y, position[1] - 2).setTypeIdAndData(*PlotMap.BLOCK_FRAME_CROSS)

	"""
	@brief Mark the plot at the specified position as reserved.
	"""
	def MarkReserved(self, x, y, frame=False):
		if frame:
			self.MarkPlotFrame(x, y)

		position = self.PlotToMapCoords(x, y)

		self.world.getBlockAt(position[0],     self.size.pos.y, position[1]    ).setTypeIdAndData(*PlotMap.BLOCK_RESERVED)
		self.world.getBlockAt(position[0] - 1, self.size.pos.y, position[1]    ).setTypeIdAndData(*PlotMap.BLOCK_RESERVED)
		self.world.getBlockAt(position[0],     self.size.pos.y, position[1] - 1).setTypeIdAndData(*PlotMap.BLOCK_RESERVED)
		self.world.getBlockAt(position[0] - 1, self.size.pos.y, position[1] - 1).setTypeIdAndData(*PlotMap.BLOCK_RESERVED)

	"""
	@brief Mark the plot at the specified position as claimed.
	"""
	def MarkClaimed(self, x, y, frame=False):
		if frame:
			self.MarkPlotFrame(x, y)

		position = self.PlotToMapCoords(x, y)

		self.world.getBlockAt(position[0],     self.size.pos.y, position[1]    ).setTypeIdAndData(*PlotMap.BLOCK_ON)
		self.world.getBlockAt(position[0] - 1, self.size.pos.y, position[1]    ).setTypeIdAndData(*PlotMap.BLOCK_ON)
		self.world.getBlockAt(position[0],     self.size.pos.y, position[1] - 1).setTypeIdAndData(*PlotMap.BLOCK_ON)
		self.world.getBlockAt(position[0] - 1, self.size.pos.y, position[1] - 1).setTypeIdAndData(*PlotMap.BLOCK_ON)

	"""
	@brief Mark the plot at the specified position as unclaimed.
	"""
	def MarkUnclaimed(self, x, y, frame=False):
		if frame:
			self.MarkPlotFrame(x, y)

		position = self.PlotToMapCoords(x, y)

		self.world.getBlockAt(position[0],     self.size.pos.y, position[1]    ).setTypeIdAndData(*PlotMap.BLOCK_OFF)
		self.world.getBlockAt(position[0] - 1, self.size.pos.y, position[1]    ).setTypeIdAndData(*PlotMap.BLOCK_OFF)
		self.world.getBlockAt(position[0],     self.size.pos.y, position[1] - 1).setTypeIdAndData(*PlotMap.BLOCK_OFF)
		self.world.getBlockAt(position[0] - 1, self.size.pos.y, position[1] - 1).setTypeIdAndData(*PlotMap.BLOCK_OFF)

	"""
	@brief Generate a plot map with the specified size.
	"""
	def Generate(self, override=False):
		existing = self.plots.Dict.keys()

		for x in xrange(-self.size.radius, self.size.radius):
			for y in xrange(-self.size.radius, self.size.radius):
				if (x, y) not in existing:
					self.MarkUnclaimed(x, y, frame=True)

				elif override:
					status = self.plots[(x, y)].node.status
					if   status == Manager.PlotStatus.FREE:
						self.MarkUnclaimed(x, y, frame=True)

					elif status == Manager.PlotStatus.CLAIMED:
						self.MarkClaimed(x, y, frame=True)

					elif status == Manager.PlotStatus.RESERVED:
						self.MarkReserved(x, y, frame=True)		

		Info("Generated map")

	"""
	@brief Update the plot map.
	"""
	def Update(self):
		self.Generate(override=True)
