"""
Permission nodes:

ore.bus
"""

from Helper import SendInfo, SendError


class LastPoint:
    def __init__(self, loc, power=0):
        self.loc = loc
        self.power = power


LastPos = {}


class Bus:
    def __init__(self, x0, y0, z0, x1, y1, z1, world, power=0):
        self.power = power

        dx = (1 if x0 < x1 else -1)
        dy = (1 if y0 < y1 else -1)
        dz = (1 if z0 < z1 else -1)

        self.x, self.y, self.z = x0, y0, z0

        self.world = world

        while self.y != y1:
            self.Draw()

            if self.x == x1:
                if self.z == z1:
                    break
                else:
                    self.z += dz

                    self.dir = (2 if z0 < z1 else 0)
            else:
                self.x += dx

                self.dir = (1 if x0 < x1 else 3)

            self.y += dy

        self.dir = (1 if x0 < x1 else 3)

        while self.x != x1:
            self.Draw()

            self.x += dx

        self.dir = (2 if z0 < z1 else 0)

        while self.z != z1:
            self.Draw()

            self.z += dz

    def Redstone(self):
        self.world.getBlockAt(self.x, self.y, self.z).setTypeId(1)
        self.world.getBlockAt(self.x, self.y + 1, self.z).setTypeId(55)

    def Repeater(self):
        self.world.getBlockAt(self.x, self.y, self.z).setTypeId(1)
        self.world.getBlockAt(self.x, self.y + 1, self.z).setTypeIdAndData(93, self.dir, True)

    def Draw(self):
        self.power = (self.power + 1) % 16

        self.Repeater() if self.power == 15 else self.Redstone()


@hook.command("bstart")
def OnCommandBusStart(sender, args):
    if not sender.hasPermission("ore.bus"):
        SendError(sender, "No permission!")
        return True

    loc = sender.getLocation()

    LastPos[sender.getName()] = LastPoint(loc)

    SendInfo(sender, "Bus start: %d %d %d" % (loc.getX(), loc.getY(), loc.getZ()))

    return True


@hook.command("bpoint")
def OnCommandBusWaypoint(sender, args):
    if not sender.hasPermission("ore.bus"):
        SendError(sender, "No permission!")
        return True

    first = LastPos.get(sender.getName())

    if first == None:
        SendError(sender, "No starting point selected!")
        return True

    second = sender.getLocation()

    if first.loc.getWorld() != second.getWorld():
        SendError(sender, "World mismatch!")

    else:
        SendInfo(sender, "Waypoint: %d %d %d" % (second.getX(), second.getY(), second.getZ()))

        b = Bus(first.loc.getBlockX(), first.loc.getBlockY(), first.loc.getBlockZ(), \
                second.getBlockX(), second.getBlockY(), second.getBlockZ(), \
                first.loc.getWorld(), first.power)

        LastPos[sender.getName()] = LastPoint(second, b.power)

    return True
