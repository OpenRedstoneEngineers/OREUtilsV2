import urllib
from Helper import SendInfo, SendError

class LookDirection:
	NORTH = 0
	SOUTH = 1
	EAST = 2
	WEST = 3

class AsmError(Exception):
	pass

class TtoR:
	def __init__(self, url, loc, dir, world):
		data = []
		
		if url.startswith('http://') or url.startswith('https://'):
			page = urllib.urlopen(url)
			text = page.read()
			data = text.split('\n')
		else:
			file = open('../../worldedit/schematics'+url)
			text = file.read()
			data = text.split('\n')

		self.Generate(loc, dir, world, data)

	def Generate(self, loc, dir, world, data):
		torch = {LookDirection.WEST:1, LookDirection.EAST:2, LookDirection.NORTH:3, LookDirection.SOUTH:4}
		repeater = {LookDirection.NORTH:3, LookDirection.EAST:0, LookDirection.SOUTH:1, LookDirection.WEST:2}
		movement = {LookDirection.NORTH:(0,-2), LookDirection.SOUTH:(0,2), \
                            LookDirection.EAST:(2,0), LookDirection.WEST:(-2,0)}

		torchp = {LookDirection.NORTH:(0,1), LookDirection.SOUTH:(0,-1), \
                          LookDirection.EAST:(-1,0), LookDirection.WEST:(1,0)}

		left = {LookDirection.NORTH:(-1,0,-1,0), LookDirection.SOUTH:(1,0,1,0), \
                        LookDirection.EAST:(0,-1,0,-1), LookDirection.WEST:(0,1,0,1)}

		for line in range(0, len(data)):
			color = 0
			world.getBlockAt(loc.getBlockX() + line*movement[dir][0], loc.getBlockY() - 1, \
                                         loc.getBlockZ() + line*movement[dir][1]).setTypeIdAndData(24, 0, True)
			world.getBlockAt(loc.getBlockX() + line*movement[dir][0], loc.getBlockY(), \
                                         loc.getBlockZ() + line*movement[dir][1]).setTypeIdAndData(76, 0, True)

			place = 0
			redLength = 15
			for ch in data[line]:
				if ch == ' ':
					color = color + 1
					continue

				if color > 15:
					color = color - 16

				world.getBlockAt(loc.getBlockX() + line*movement[dir][0] + (place+1)*left[dir][0], \
                                                 loc.getBlockY() - 1, \
                                                 loc.getBlockZ() + line*movement[dir][1] + \
                                                 (place+1)*left[dir][1]).setTypeIdAndData(35, color, True)
				world.getBlockAt(loc.getBlockX() + line*movement[dir][0] + (place+1)*left[dir][0], \
                                                 loc.getBlockY(), \
                                                 loc.getBlockZ() + line*movement[dir][1] + \
                                                 (place+1)*left[dir][1]).setTypeIdAndData(55, 0, True)

				if ch == '1':
					world.getBlockAt(loc.getBlockX() + line*movement[dir][0] + \
                                                         (place+1)*left[dir][0] + torchp[dir][0], loc.getBlockY()-1,\
                                                         loc.getBlockZ() + line*movement[dir][1] + \
                                                         (place+1)*left[dir][1] + torchp[dir][1] \
                                                        ).setTypeIdAndData(76, torch[dir], True)

				world.getBlockAt(loc.getBlockX() + line*movement[dir][0] + (place+1)*left[dir][0] \
                                                 + left[dir][2], loc.getBlockY()-1, \
                                                 loc.getBlockZ() + line*movement[dir][1] + (place+1)*left[dir][1] \
                                                 + left[dir][3]).setTypeIdAndData(24, 0, True)
				
				world.getBlockAt(loc.getBlockX() + line*movement[dir][0] + (place+1)*left[dir][0] \
                                                 + left[dir][2], loc.getBlockY(), \
                                                 loc.getBlockZ() + line*movement[dir][1] + (place+1)*left[dir][1] \
                                                 + left[dir][3]).setTypeIdAndData(55, 0, True)

				redLength = redLength - 2

				if redLength <= 0:
					redLength = 15
					world.getBlockAt(loc.getBlockX() + line*movement[dir][0] + \
                                                         (place+1)*left[dir][0] + left[dir][2], loc.getBlockY(), \
                                                         loc.getBlockZ() + line*movement[dir][1] + \
                                                         (place+1)*left[dir][1] + left[dir][3]\
                                                         ).setTypeIdAndData(93, repeater[dir], True)

				world.getBlockAt(loc.getBlockX() + line*movement[dir][0] + (place+1)*left[dir][0], \
                                                 loc.getBlockY() - 3, \
                                                 loc.getBlockZ() + line*movement[dir][1] + (place+1)*left[dir][1] \
                                                ).setTypeIdAndData(24, 0, True)

				world.getBlockAt(loc.getBlockX() + line*movement[dir][0] + (place+1)*left[dir][0], \
                                                 loc.getBlockY() - 2, \
                                                 loc.getBlockZ() + line*movement[dir][1] + (place+1)*left[dir][1] \
                                                ).setTypeIdAndData(55, 0, True)

				world.getBlockAt(loc.getBlockX() + line*movement[dir][0] + (place+1)*left[dir][0] \
                                                 + torchp[dir][0], loc.getBlockY() - 3, \
                                                 loc.getBlockZ() + line*movement[dir][1] + (place+1)*left[dir][1] \
                                                 + torchp[dir][1]).setTypeIdAndData(24, 0, True)

				world.getBlockAt(loc.getBlockX() + line*movement[dir][0] + (place+1)*left[dir][0] \
                                                 + torchp[dir][0], loc.getBlockY() - 2, \
                                                 loc.getBlockZ() + line*movement[dir][1] + (place+1)*left[dir][1] \
                                                 + torchp[dir][1]).setTypeIdAndData(55, 0, True)

				if ch != ' ' and ch != '1' and ch != '0':
					raise AmsError()
				
				place = place+2

@hook.command('ttor', usage='/ttor <url|file>')
def onCommandTtoR(sender, args):
	if not sender.hasPermission("ore.ttor"):
		SendError(sender, 'No permission!')
		return True

	loc = sender.getLocation()
	
	if len(args) < 1:
		return False

	yaw = (loc.getYaw() - 90) % 360
	if yaw < 0:
		yaw = yaw + 360

	if (yaw >= 315) or (yaw >= 0 and yaw <= 45):
		dir = LookDirection.WEST
	elif (yaw > 45 and yaw < 135):
		dir = LookDirection.SOUTH
	elif (yaw >= 135 and yaw <= 225):
		dir = LookDirection.EAST
	else:
		dir = LookDirection.NORTH

	try:
		tmp = TtoR(str(args[0]), loc, dir, sender.getWorld())
	except IOError as E:
		SendError(sender, 'Error opening file!')
	except AsmError as E:
		SendError(sender, 'Error in Asm!')
	except Exception as E:
		SendError(sender, str(E))

	return True
