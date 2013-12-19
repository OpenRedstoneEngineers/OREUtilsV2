"""
Permission nodes:

ore.bus
""'

LastPos = {}

@hook.command("bstart")
def onCommandBusStart(sender, args):
	if not sender.hasPermission("ore.bus"):
		sender.sendMessage("No permission!")
		return True

	loc = sender.getLocation()

	LastPos[sender.getName()] = loc

	sender.sendMessage("Bus start: %d %d %d" % (loc.getX(), loc.getY(), loc.getZ()))

	return True

@hook.command("bpoint")
def onCommandBusWaypoint(sender, args):
	if not sender.hasPermission("ore.bus"):
		sender.sendMessage("No permission!")
		return True

	first = LastPos.get(sender.getName())

	if first == None:
		sender.sendMessage("No starting point selected!")
		return True

	second = sender.getLocation()

	LastPos[sender.getName()] = second

	if first.getWorld() != second.getWorld():
		sender.sendMessage("World mismatch!")
		
	else:
		sender.sendMessage("Waypoint: %d %d %d" % (second.getX(), second.getY(), second.getZ()))

		Bus(first.getBlockX(), first.getBlockY(), first.getBlockZ(),\
	   		second.getBlockX(), second.getBlockY(), second.getBlockZ(), first.getWorld())

	return True

class Bus(x0, y0, z0, x1, y1, z1, world):
	def __init__(self, x0, y0, z0, x1, y1, z1, world):
		dx = (1 if x0 < x1 else -1)
		dy = (1 if y0 < y1 else -1)
		dz = (1 if z0 < z1 else -1)

		self.x, self.y, self.z = x0, y0, z0
		self.power = 0

		while self.y != y1:
			self.Draw()

			if self.x == x1:
				if self.z == z1:
					break
				else:
					self.z += dz
			else:
				self.x += dx
		while self.x != x1:
			self.Draw()
			self.x += dx

		while self.z != z1:
			self.Draw()
			self.z != dz
	
	def Redstone(self):
		self.world.getBlockAt(self.x, self.y    , self.z).setTypeId(1)
		self.world.getBlockAt(self.x, self.y + 1, self.z).setTypeId(55)

	def Repeater(self):
		self.world.getBlockAt(self.x, self.y    , self.z).setTypeId(1)
		self.world.getBlockAt(self.x, self.y + 1, self.z).setTypeId(93)#Wanna put some self.dir shit here.

	def Draw(self):
		self.power = (self.power + 1) % 5

		self.Repeater() if self.power == 15 else self.Redstone()
