from org.bukkit.Bukkit import broadcastMessage

from Helper import Color

TNT = True

# TNT command
@hook.command("tnt", description = "TNT is fun.")
def OnCommandTNT(sender, args):
	if not sender.hasPermission('ore.tnt'):
		sender.sendMessage("No permission!")
		return True

	global TNT

	TNT = not TNT

	broadcastMessage('TNT has been %sabled'%('re-en','dis')[TNT])
		
	return True

# TNT
@hook.event("entity.ExplosionPrimeEvent", "high")
def OnExplosionPrimeEvent(e):
	if TNT:
		e.setCancelled(True)

# TNT Carts
@hook.event("entity.EntityExplodeEvent", "high")
def OnEntityExplodeEvent(e):
	if TNT:
		e.setCancelled(True)

# Banned items
@hook.event("player.PlayerInteractEvent", "Monitor")
def OnPlayerClick(event):
	if event.getItem() == None:
		return False

	player = event.getPlayer()

	if player.hasPermission("".join(('ore.ban.', str(event.getItem().getTypeId())))):
		if not player.hasPermission("ore.ban.override"):
			event.setCancelled(True)
			player.sendMessage(Color("4") + "You are not allowed to use this item.")

	return True

# Time day
@hook.event("player.PlayerJoinEvent", "Normal")
def OnPlayerJoinEvent(event):
	sender = event.getPlayer()

	sender.setPlayerTime(6000, 0)
	sender.sendMessage("Your time was set to day.")

	return True

# Lamps command
Lamps = False

@hook.command("lamps", description="Toggle lamps")
def OnCommandLamps(sender,args):
	if not sender.hasPermission('ore.lamp'):
		sender.sendMessage("No permission!")
		return True

	global Lamps

	Lamps = not Lamps

	broadcastMessage('Lamps have been %sabled' % ('re-en', 'dis')[Lamps])

	return True

# Lamps
@hook.event("block.BlockPhysicsEvent", "High")
def onBlockChanged(event):
	if Lamps:
		if event.getBlock().getTypeId() in [123, 124]:
			event.setCancelled(True)
