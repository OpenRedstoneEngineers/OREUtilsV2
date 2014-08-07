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

A warning message is to be used when a command execution has an issue, but can continue.
'''
def SendWarning(Player, Message):
	Player.sendMessage(Color("6") + "[WARNING] " + Message)

'''
Send an error message to a player.

An error message is to be used when a command execution cannot continue.
'''
def SendError(Player, Message):
	Player.sendMessage(Color("c") + "[ERROR] " + Message)

'''
Give an item to the specified player.
'''
def GiveItem(Player, Type, Meta=0, Amount=1):
	Player.getInventory().addItem(ItemStack(Type, Amount, Meta))

'''
printf like function for color formatting strings to send
'''
def SendF(player, msg, *args):
	if len(args) == 0:
		formats = 'e'
	else:
		formats = args

	max = len(formats) - 1
	out = ' '

	for ind, i in enumerate(msg.split("{/c}")):
		if ind <= max:
			out = out + i + Color(formats[ind])
		else:
			out = out + i + Color(formats[max])
	
	player.sendMessage(out[1:])
