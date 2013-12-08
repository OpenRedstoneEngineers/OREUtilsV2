import org.bukkit.Bukkit as Bukkit

from java.util.logging import Level

# Deprecated
def Color(colors):
	return ''.join([u'\u00A7' + color for color in colors])

# Execute a command with root permissions
def Sudo(command):
	Bukkit.dispatchCommand(Bukkit.getConsoleSender(), command)

def Info(message):
	Bukkit.getServer().getLogger().log(Level.INFO, message)

def Severe(message):
	Bukkit.getServer().getLogger().log(Level.SEVERE, message)
