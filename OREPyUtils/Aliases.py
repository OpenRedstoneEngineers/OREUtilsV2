from Helper import Sudo, Color

from org.bukkit import Bukkit

from org.bukkit.potion import PotionEffectType
from org.bukkit.potion import PotionEffect

'''
Permission nodes:
ore.fun.join
ore.raw
''' 

@hook.command("fixlag", description="Clears out minecarts, arrows, items, etc.")
def OnCommandFixLag(sender, args):
	Bukkit.dispatchCommand(sender, "rem items -1")
	Bukkit.dispatchCommand(sender, "rem arrows -1")
	Bukkit.dispatchCommand(sender, "rem boats -1")
	Bukkit.dispatchCommand(sender, "rem xp -1")

	Bukkit.dispatchCommand(sender, "butcher -f")

	sender.sendMessage(Color("5") + "T3h lagz, they be gone!")

	return True


@hook.command("fast")
def OnCommandFast(sender, args):
	for potion in sender.getActivePotionEffects():
		sender.removePotionEffect(potion.getType()) 

	sender.addPotionEffect(PotionEffect(PotionEffectType.SPEED, 5000, 50, True))
	sender.addPotionEffect(PotionEffect(PotionEffectType.FAST_DIGGING, 5000, 50, True))
	sender.addPotionEffect(PotionEffect(PotionEffectType.JUMP, 5000, 8, True))

	sender.sendMessage("SUPER SPEED!")

	return True

@hook.command("quick", description="A version of /fast, made for buliding")
def onCommandQuick(sender, args):
	for potion in sender.getActivePotionEffects(): 
		sender.removePotionEffect(potion.getType())

	sender.addPotionEffect(PotionEffect(PotionEffectType.SPEED, 50000, 3, True))
	sender.addPotionEffect(PotionEffect(PotionEffectType.JUMP, 50000, 2, True))
	sender.addPotionEffect(PotionEffect(PotionEffectType.NIGHT_VISION, 50000, 2, True))
	sender.addPotionEffect(PotionEffect(PotionEffectType.INCREASE_DAMAGE, 50000, 2, True))

	sender.sendMessage("Super powers!")

	return True

@hook.command("fixme", description="Removes all active potion effects")
def OnCommmandFixMe(sender, args):
	for potion in sender.getActivePotionEffects():
		sender.removePotionEffect(potion.getType())

	return True

@hook.command("join", description="Make someone join the server!", usage="/<command> <player> [location]")
def onCommandJoin(sender, args):
	if not sender.hasPermission("ore.fun.join"):
		sender.sendMessage("No permission!")
		return True

	if len(args) < 1:
		return False

	Bukkit.broadcastMessage(Color("e") + args[0] + " joined the game.")

	if len(args) > 1:
		Bukkit.broadcastMessage("Player " + args[0] + " comes from " + ' '.join(args[1:]))

	return True

@hook.command("leave", description="Make someone leave the server!", usage="/<command> <player>")
def onCommandLeave(sender, args):
	if not sender.hasPermission("ore.fun.join"):
		sender.sendMessage("No permission!")
		return True

	if not len(args):
		return False

	Bukkit.broadcastMessage(color("e") + args[0] + " left the game.")

	return True

@hook.command("raw")
def onCommandRaw(sender, args):
	if not sender.hasPermission("ore.raw"):
		sender.sendMessage("No permission!")
		return True
	
	Bukkit.broadcastMessage(' '.join(args).replace('&', u'\u00A7'))

	return True
