from __future__ import division

import os
from ast import literal_eval as Eval

from org.bukkit.Bukkit import dispatchCommand
from org.bukkit.Bukkit import getPlayer
from org.bukkit.Bukkit import broadcastMessage

from Helper import Color, Colorify, Info, SendInfo, SendError

help = {}
keys = []

def OnEnable(conf=None):
	global help, keys

	Config = conf.node.properties

	Config.Ensure("HelpPath", "")
	Config.Ensure("MainPath", "")

	filename = Config.HelpPath.replace("[path]", Config.MainPath)

	try:
		help = Eval(open(filename).read())

		keys = help.keys()
		keys.sort()

	except:
		Info("[!]Could not find help file")
		
@hook.command("encode")
def OnCommandEncode(sender,args):
	sender.sendMessage(' '.join(args).encode('hex'))
	return True

@hook.command("decode")
def OnCommandDecode(sender,args):
	String = ''.join(args)
	Final  = []

	for Ind in range(0, len(String), 2):
		try:
			Final.append(chr(int(String[Ind:Ind + 2], 16)))

		except:
			SendError(sender, 'Invalid Char!')
			return True

	sender.sendMessage(''.join(Final))

	return True

@hook.command('rename', description='Rename the item in your hand', usage="Usage: /rename <name>")
def OnCommandRename(sender, args):
	if not args:
		return False

	argstring = Colorify(' '.join(args))

	item = sender.getItemInHand()

	meta = item.getItemMeta()

	if meta == None:
		SendError(sender, "No item in hand")
		return True

	meta.setDisplayName(argstring)

	item.setItemMeta(meta)

	SendInfo(sender, "Renamed item!")

	return True

@hook.command("execbook")
def OnCommandExecBook(sender, args):
	if not sender.hasPermission("ore.execbook"):
		SendError(sender, "No permission!")
		return

	item = sender.getItemInHand()

	if item.getTypeId() not in (386, 387):
		SendError(sender, 'You must have a book')
		return True

	meta = item.getItemMeta()

	pages = []

	for page in meta.getPages():
		pages.append(page)

	program = '\n'.join(pages)

	for i in xrange(len(args)):
		program = program.replace('#a' + str(i), args[i])

	program = program.replace("#a", ' '.join(args))
	program = program.replace("#m", sender.getName())
	program = program.replace("#p", "ping &b")

	cmds = program.split('\n')

	if len(cmds) > 3 and not sender.hasPermission("ore.execbook.admin"):
		SendError(sender, "Cannot execute more than three commands")
		return True

	for cmd in cmds:
		if cmd in ("execbook", ""):
			continue

		dispatchCommand(sender, cmd)

	SendInfo(sender, "Exectued %d commands!" % len(cmds))

	return True

@hook.command('schems', usage="Usage: /schems <list|load|save> name")
def OnCommandSchems(sender, args):
	Name = sender.getName()

	if len(args) == 2 and args[0] in ("load", "save"):
		dispatchCommand(sender, '/schematic ' + args[0] + ' ' + Name + '/' + args[1].split('/')[0])
	
		return True

	elif len(args) == 1 and args[0] == "list":
		try:
			UserSchems = os.listdir('/var/www/schems/files/' + Name)
		except:
			SendError(sender, "Could not read the schematic directory.")
			return True

		sender.sendMessage('List of your schematics:')

		for item in UserSchems:
			sender.sendMessage(item)

		return True

	return False

@hook.command('pass')
def OnCommandPass(sender, args):
	dispatchCommand(sender, 'dbp set ' + ' '.join(args))
	return True

@hook.command('orehelp')
def OnCommandOREHelp(sender, args):
	if len(args) == 0:
		matches = len(keys)

		for i in keys:
			sender.sendMessage(Color("e") + '/' + Color("6") + i + Color("e") + help[i]['short'])
	else:
		# Full match
		if args[0] in keys:
			matches = 1

			sender.sendMessage(Color("a") + '/' + Color("2") + args[0] + Color("a") + help[args[0]]['long'])

		# Partial match
		else:		
			matches = 0 

			# Starting with
			for i in keys:
				if i.find(args[0]) == 0:
					matches += 1
					sender.sendMessage(Color("e") + '/' + Color("6") + i + Color("e") + help[i]['short'])

			# Containing
			for i in keys:
				if i.find(args[0]) > 0:
					matches += 1
					sender.sendMessage(Color("e") + '/' + Color("6") + i + Color("e") + help[i]['short'])

	# Print number of matches
	if matches == 0:
		sender.sendMessage(Color("c") + '==== ' + Color("4") + 'No matches found' + Color("c") + ' ====')
	else:
		sender.sendMessage(Color("e") + '==== ' + Color("c") + str(matches) + Color("6") + ' matches found' + Color("e") + ' ====')

	return True

