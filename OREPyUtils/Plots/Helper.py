import org.bukkit.Bukkit as Bukkit

from java.util.logging import Level

def Info(message):
	Bukkit.getServer().getLogger().log(Level.INFO, message)
