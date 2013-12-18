LastPos = {}

@hook.command("bstart")
def onCommandBusStart(sender, args):
	if not sender.hasPermission("ore.bus"):
		sender.sendMessage("No permission!")
		return True

	loc = sender.getLocation()

	LastPos[sender.getName()] = loc

	sender.sendMessage("Bus start: %i %i %i" % (loc.getX(), loc.getY(), loc.getZ()))

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
		return True

	sender.sendMessage("Waypoint: %i %i %i" % (second.getX(), second.getY(), second.getZ()))

	Bus(first.getBlockX(), first.getBlockY(), first.getBlockZ(),\
	    second.getBlockX(), second.getBlockY(), second.getBlockZ(), first.getWorld())

	return True

def SetBusRedstone(x, y, z, world):
	world.getBlockAt(x, y, z).setTypeId(1)
	world.getBlockAt(x, y + 1, z).setTypeId(55)

def Bus(x0, y0, z0, x1, y1, z1, world):
	if x0 < x1:
		dx = 1
	else:
		dx = -1

	if y0 < y1:
		dy = 1
	else:
		dy = -1

	if z0 < z1:
		dz = 1
	else:
		dz = -1

	while y0 != y1:
		SetBusRedstone(x0, y0, z0, world)

		if x0 == x1:
			if z0 == z1:
				break
			else:
				z0 += dz
		else:
			x0 += dx

		y0 += dy

	while x0 != x1:
		SetBusRedstone(x0, y0, z0, world)

		x0 += dx

	while z0 != z1:
		SetBusRedstone(x0, y0, z0, world)

		z0 += dz
