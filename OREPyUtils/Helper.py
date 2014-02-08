import org.bukkit.Bukkit as Bukkit

import re

from java.util.logging import Level

# Deprecated
def Color(colors):
	return ''.join([u'\u00A7' + color for color in colors])
def color(colors):
	return Color(colors)
	
# lets you use &-coded strings
def Colorify(text):
	return re.sub("&(?=[?\da-fk-or])", u"\u00A7", text)

'''
Execute a command with root permissions
'''
def Sudo(Command):
	Bukkit.dispatchCommand(Bukkit.getConsoleSender(), Command)

def Info(Message):
	Bukkit.getServer().getLogger().log(Level.INFO, Message)

def Severe(Message):
	Bukkit.getServer().getLogger().log(Level.SEVERE, Message)

def SendInfo(Player, Message):
	Player.sendMessage(Color("e") + "[INFO] " + Message)

def SendWarning(Player, Message):
	Player.sendMessage(Color("6") + "[WARNING] " + Message)

def SendError(Player, Message):
	Player.sendMessage(Color("c") + "[ERROR] " + Message)
