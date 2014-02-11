import org.bukkit.Bukkit as Bukkit

from org.bukkit.inventory import ItemStack

import re

from java.util.logging import Level

'''
Constructs a colorcode string from the specified color sequence.

NOTE: Deprecated.
'''
def Color(Colors):
	return ''.join([u'\u00A7' + Color for Color in Colors])
	
'''
Transforms a &-encoded string to a colored one.
'''
def Colorify(Text):
	return re.sub("&(?=[?\da-fk-or])", u"\u00A7", Text)

'''
Execute a command with root permissions
'''
def Sudo(Command):
	Bukkit.dispatchCommand(Bukkit.getConsoleSender(), Command)

'''
Log info
'''
def Info(Message):
	Bukkit.getServer().getLogger().log(Level.INFO, Message)

'''
Log a severe error
'''
def Severe(Message):
	Bukkit.getServer().getLogger().log(Level.SEVERE, Message)

'''
Send a plain text message to a player
'''
def SendInfo(Player, Message):
	Player.sendMessage(Color("e") + "[INFO] " + Message)

'''
Send a warning message to a player.

an error message is to be used when a command execution has an issus, but can continue.'''
def SendWarning(Player, Message):
	Player.sendMessage(Color("6") + "[WARNING] " + Message)
'''
Send an error message to a player.

an error message is to be used when a command execution cannot continue.'''
def SendError(Player, Message):
	Player.sendMessage(Color("c") + "[ERROR] " + Message)

'''
Give an item to the specified player.
'''
def GiveItem(Player, Type, Meta=0, Amount=1):
	Player.getInventory().addItem(ItemStack(Type, Amount, Meta))
