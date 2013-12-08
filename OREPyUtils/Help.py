from org.bukkit import ChatColor

import re

help = eval(open('Help.txt').read())
keys = help.keys()
keys.sort()

@hook.command('orehelp')
def onCommandFineGuy(sender,args):
	if len(args) == 0:
		matches = len(keys)
		for i in keys:
			sender.sendMessage(ChatColor.YELLOW + '/' + ChatColor.GOLD + i + ChatColor.YELLOW + help[i]['short'])

	elif args[0] in keys:
		matches = 1
		sender.sendMessage(ChatColor.GREEN + '/' + ChatColor.DARK_GREEN + args[0] + ChatColor.GREEN + help[args[0]]['long'])

	else:       
		matches = 0 

	for i in keys:
		if i.find(args[0]) == 0:
			matches += 1
			sender.sendMessage(ChatColor.YELLOW + '/' + ChatColor.GOLD + i + ChatColor.YELLOW + help[i]['short'])

	for i in keys:
		if i.find(args[0]) > 0:
			matches += 1
			sender.sendMessage(ChatColor.WHITE + '/' + ChatColor.GRAY + ChatColor.WHITE + help[i]['short'])

	if matches == 0:
		sender.sendMessage(ChatColor.RED + '====' + ChatColor.DARK_RED + 'No matches found' + ChatColor.RED + '====')
	else:
		sender.sendMessage(ChatColor.YELLOW + '====' + ChatColor.RED + str(matches) + ChatColor.GOLD + 'matches found' + ChatColor.YELLOW + '====')

	return True



