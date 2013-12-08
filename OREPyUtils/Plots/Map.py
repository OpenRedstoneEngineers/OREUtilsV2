import Manager

import xml.etree.ElementTree as ET

from Helper import Info

class PlotMap(Manager.PlotManager):
	BLOCK_RESERVED    = (159,10 ,0)
	BLOCK_ON          = (159, 3 ,0)
	BLOCK_OFF         = (159, 0 ,0)
	BLOCK_FRAME_X     = (1  , 0 ,0)
	BLOCK_FRAME_Y     = (1  , 0 ,0)
	BLOCK_FRAME_CROSS = (1  , 0 ,0)
	BLOCK_BASE        = (1  , 0 ,0)


	def __init__(self, world, radius, mapPos, plotx, ploty):
		Manager.PlotManager.__init__(self, radius, plotx, ploty)

		self.mapPos = mapPos

		self.world = world
	"""
	@return if specified plot coords are on the map
	"""
	def IsOnMap(self, x, z):
		return abs(x - self.mapPos[0]) < (self.radius * 3) and abs(z - self.mapPos[2]) < (self.radius * 3)

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

		return (newX + self.mapPos[0] + 2, newY + self.mapPos[2] + 2)

	"""
	@return the plot coords of a physical location on the map
	"""
	def MapToPlotCoords(self, x, y):
		newX = x - self.mapPos[0]
		newY = y - self.mapPos[2]

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

		self.world.getBlockAt(position[0] - 2, self.mapPos[1], position[1]    ).setTypeIdAndData(*PlotMap.BLOCK_FRAME_Y)
		self.world.getBlockAt(position[0] - 2, self.mapPos[1], position[1] - 1).setTypeIdAndData(*PlotMap.BLOCK_FRAME_Y)
		self.world.getBlockAt(position[0],     self.mapPos[1], position[1] - 2).setTypeIdAndData(*PlotMap.BLOCK_FRAME_X)
		self.world.getBlockAt(position[0] - 1, self.mapPos[1], position[1] - 2).setTypeIdAndData(*PlotMap.BLOCK_FRAME_X)

		if x == self.radius-1:
			self.world.getBlockAt(position[0] + 1, self.mapPos[1], position[1]    ).setTypeIdAndData(*PlotMap.BLOCK_FRAME_Y)
			self.world.getBlockAt(position[0] + 1, self.mapPos[1], position[1] - 1).setTypeIdAndData(*PlotMap.BLOCK_FRAME_Y)

		if y == self.radius-1:
			self.world.getBlockAt(position[0],     self.mapPos[1], position[1] + 1).setTypeIdAndData(*PlotMap.BLOCK_FRAME_X)
			self.world.getBlockAt(position[0] - 1, self.mapPos[1], position[1] + 1).setTypeIdAndData(*PlotMap.BLOCK_FRAME_X)


		self.world.getBlockAt(position[0] - 2, self.mapPos[1], position[1] - 2).setTypeIdAndData(*PlotMap.BLOCK_FRAME_CROSS)

		self.world.getBlockAt(position[0],     self.mapPos[1] - 1, position[1]    ).setTypeIdAndData(*PlotMap.BLOCK_BASE)
		self.world.getBlockAt(position[0] - 1, self.mapPos[1] - 1, position[1]    ).setTypeIdAndData(*PlotMap.BLOCK_BASE)
		self.world.getBlockAt(position[0],     self.mapPos[1] - 1, position[1] - 1).setTypeIdAndData(*PlotMap.BLOCK_BASE)
		self.world.getBlockAt(position[0] - 1, self.mapPos[1] - 1, position[1] - 1).setTypeIdAndData(*PlotMap.BLOCK_BASE)

	"""
	@brief Mark the plot at the specified position as reserved.
	"""
	def MarkReserved(self, x, y, frame=False):
		if frame:
			self.MarkPlotFrame(x, y)

		position = self.PlotToMapCoords(x, y)

		self.world.getBlockAt(position[0],     self.mapPos[1], position[1]    ).setTypeIdAndData(*PlotMap.BLOCK_RESERVED)
		self.world.getBlockAt(position[0] - 1, self.mapPos[1], position[1]    ).setTypeIdAndData(*PlotMap.BLOCK_RESERVED)
		self.world.getBlockAt(position[0],     self.mapPos[1], position[1] - 1).setTypeIdAndData(*PlotMap.BLOCK_RESERVED)
		self.world.getBlockAt(position[0] - 1, self.mapPos[1], position[1] - 1).setTypeIdAndData(*PlotMap.BLOCK_RESERVED)

	"""
	@brief Mark the plot at the specified position as claimed.
	"""
	def MarkClaimed(self, x, y, frame=False):
		if frame:
			self.MarkPlotFrame(x, y)

		position = self.PlotToMapCoords(x, y)

		self.world.getBlockAt(position[0],     self.mapPos[1], position[1]    ).setTypeIdAndData(*PlotMap.BLOCK_ON)
		self.world.getBlockAt(position[0] - 1, self.mapPos[1], position[1]    ).setTypeIdAndData(*PlotMap.BLOCK_ON)
		self.world.getBlockAt(position[0],     self.mapPos[1], position[1] - 1).setTypeIdAndData(*PlotMap.BLOCK_ON)
		self.world.getBlockAt(position[0] - 1, self.mapPos[1], position[1] - 1).setTypeIdAndData(*PlotMap.BLOCK_ON)

	"""
	@brief Mark the plot at the specified position as unclaimed.
	"""
	def MarkUnclaimed(self, x, y, frame=False):
		if frame:
			self.MarkPlotFrame(x, y)

		position = self.PlotToMapCoords(x, y)

		self.world.getBlockAt(position[0],     self.mapPos[1], position[1]    ).setTypeIdAndData(*PlotMap.BLOCK_OFF)
		self.world.getBlockAt(position[0] - 1, self.mapPos[1], position[1]    ).setTypeIdAndData(*PlotMap.BLOCK_OFF)
		self.world.getBlockAt(position[0],     self.mapPos[1], position[1] - 1).setTypeIdAndData(*PlotMap.BLOCK_OFF)
		self.world.getBlockAt(position[0] - 1, self.mapPos[1], position[1] - 1).setTypeIdAndData(*PlotMap.BLOCK_OFF)

	"""
	@brief Generate a plot map with the specified size.
	"""
	def Generate(self, override=False):
		existing = self.plots.keys()

		for x in xrange(-self.radius, self.radius):
			for y in xrange(-self.radius, self.radius):
				if (x, y) not in existing:
					self.MarkUnclaimed(x, y)
				
				elif override:
					status = self.plots[(x, y)].status
					if   status == PlotStatus.UNCLAIMED:
						self.MarkUnclaimed(x, y, frame=True)

					elif status == PlotStatus.CLAIMED:
						self.MarkClaimed(x, y, frame=True)

					elif status == PlotStatus.RESERVED:
						self.MarkReserved(x, y, frame=True)		

		Info("Generated map")

	"""
	@brief Update the plot map.
	"""
	def Update(self):
		self.Generate(override=True)

	"""
	@brief Serialize the plot map.
	"""
	def Serialize(self, root):
		Manager.PlotManager.Serialize(self, root)

		posNode = ET.SubElement(root, "MapPos")

		posNode.set("x", str(self.mapPos[0]))
		posNode.set("y", str(self.mapPos[1]))
		posNode.set("z", str(self.mapPos[2]))

	"""
	@brief Deserialize the plot map.
	"""
	def Deserialize(self, root):
		Manager.PlotManager.Deserialize(self, root)

		posNode = root.find("MapPos")

		self.mapPos[0] = int(posNode.get("x"))
		self.mapPos[1] = int(posNode.get("y"))
		self.mapPos[2] = int(posNode.get("z"))
