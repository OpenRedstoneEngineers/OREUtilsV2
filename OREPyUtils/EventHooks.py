from org.bukkit.Bukkit import broadcastMessage

from Helper import Color, SendInfo, SendError

def OnEnable(conf=None):
	global val
	
	val = conf.node.properties

	val.Ensure("TNT", False)
	val.Ensure("Lamps", True)

# TNT
@hook.event("entity.ExplosionPrimeEvent", "high")
def OnExplosionPrimeEvent(event):
	if TNT:
		event.setCancelled(True)

# TNT Carts
@hook.event("entity.EntityExplodeEvent", "high")
def OnEntityExplodeEvent(event):
	if val.TNT:
		event.setCancelled(True)

# Lamps
@hook.event("block.BlockPhysicsEvent", "High")
def onBlockChanged(event):
	if val.Lamps:
		if event.getBlock().getTypeId() in [123, 124]:
			event.setCancelled(True)

# Banned items
@hook.event("player.PlayerInteractEvent", "Monitor")
def OnPlayerClick(event):
	if event.getItem() == None:
		return False

	player = event.getPlayer()

	ItemPermission = "ore.ban." + str(event.getItem().getTypeId())

	if player.hasPermission(ItemPermission):
		if not player.hasPermission("ore.ban.override"):
			event.setCancelled(True)

			SendInfo(player, "You are not allowed to use this item.")

	return True

# Time day
@hook.event("player.PlayerJoinEvent", "Normal")
def OnPlayerJoinEvent(event):
	sender = event.getPlayer()

	sender.setPlayerTime(6000, 0)

	SendInfo(sender, "Your time was set to day.")

	return True
