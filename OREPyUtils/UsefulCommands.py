from __future__ import division

import os

from org.bukkit.Bukkit import dispatchCommand
from org.bukkit.Bukkit import getPlayer
from org.bukkit.Bukkit import broadcastMessage

from Helper import Color, Colorify, Info

help = {}
keys = []

def OnEnable(**kwargs):
	global help, keys

	try:
		keys = help.keys()
		keys.sort()
		help = open(kwargs['path']).read()

	except:
		Info("[!]Could not find help file")
		
@hook.command("encode")
def Encode(sender,args):
	sender.sendMessage(' '.join(args).encode('hex'))
	return True

@hook.command("decode")
def Decode(sender,args):
	String = ''.join(args)
	Final  = []

	for Ind in range(0, len(String), 2):
		try:
			Final.append(chr(int(String[Ind:Ind + 2], 16)))

		except:
			sender.sendMessage('Invalid Char!')
			return True

	sender.sendMessage(''.join(Final))

	return True

@hook.command('rename', description='Rename the item in your hand', usage="Usage: /rename <name>")
def onCommandLore(sender, args):
	if not args:
		return False

	argstring = Colorify(' '.join(args))

	item = sender.getItemInHand()

	meta = item.getItemMeta()

	if meta == None:
		sender.sendMessage("No item in hand")
		return True

	meta.setDisplayName(argstring)

	item.setItemMeta(meta)

	sender.sendMessage("Renamed item!")

	return True

@hook.command('e')
def onCommandBookGet(sender, args):
	item = sender.getItemInHand()

	if item.getTypeId() not in (386, 387):
		sender.sendMessage(Color("c") + 'You must have a book')
		return False

	metadata = item.getItemMeta()
	s = ''	  

	for i in metadata.getPages():
		s = s+'\n'+i

	n = 0

	while 1:
		a = '#a'+str(n)

		if len(args) <= n:
			break

		s = s.replace(a, args[n])
		n += 1

	n = 0

	while 1:
		a = '#r'+str(n)

		if len(args) <= n:
			break

		s = s.replace(a, ' '.join(args[n:]))
		n += 1

	n = 0

	while 1:
		a = '#n'+str(n)

		if len(args) <= n:
			break

		name = getPlayer(args[n])

		if name != None:
			s = s.replace(a, name.getName())

		n += 1

	s = s.replace('#a', ' '.join(args))
	s = s.replace('#p', 'ping &b')
	s = s.replace('#m', sender.getName())
	s = s.split('\n')[1:]
	n = 0

	if len(args) > 0 and '@'+args[0] in s:
		n = s.index('@'+args[0])+1
		no = 0

		while True:
			if n == len(s):
				break

			if no == 3 and not sender.hasPermission('xeoperms.give'):
				break
			
			command = s[n]
			if command[0:2] == '#b':
				broadcastMessage(Color("e") + s[n][2:] + Color("6") + ' ('+ sender.getName() + ')')
			elif command.split()[0] != 'e':
				dispatchCommand(sender, command)
 
			if not n+1 == len(s) and s[n+1][0] == '@':
				break
 
			n += 1
			no += 1
		sender.sendMessage('Command(s) run!')
		return True

	for i in s:
		if n == 3 and not sender.hasPermission('xeoperms.give'):
			break
		if len(i) == 0:
			break
		if i[0] == '@':
			break

		if i[0:2] == '#b':
			broadcastMessage(Color("e") + i[2:] + Color("6") + ' ('+sender.getName()+')')
		elif i.split()[0] != 'e':
			dispatchCommand(sender, i)
		n += 1

	sender.sendMessage(Color("a") + 'Command(s) run!')

	return True

@hook.command('schems', usage="Usage: /schems <list|load|save> name")
def onCommandSchems(sender, args):
	Name = sender.getName()

	if len(args) == 2 and args[0] in ("load", "save"):
		dispatchCommand(sender, '/schematic ' + args[0] + ' ' + Name + '/' + args[1].split('/')[0])
	
		return True

	elif len(args) == 1 and args[0] == "list":
		try:
			UserSchems = os.listdir('/var/www/schems/files/' + Name)
		except:
			sender.sendMessage("No schematics!")
			return True

		sender.sendMessage('List of your schematics:')

		for item in UserSchems:
			sender.sendMessage(item)

		return True

	return False

@hook.command('pass')
def passset(sender, args):
	dispatchCommand(sender, 'dbp set ' + ' '.join(args))
	return True

@hook.command('orehelp')
def onCommandOREHelp(sender,args):
	if len(args) == 0:
		matches = len(keys)

		for i in keys:
			sender.sendMessage(Color("e") + '/' + Color("6") + i + Color("e") + help[i]['short'])

	elif args[0] in keys:
		matches = 1

		sender.sendMessage(Color("a") + '/' + Color("2") + args[0] + Color("a") + help[args[0]]['long'])
	else:		
		matches = 0 

	for i in keys:
		if i.find(args[0]) == 0:
			matches += 1
			sender.sendMessage(Color("e") + '/' + Color("6") + i + Color("e") + help[i]['short'])

	for i in keys:
		if i.find(args[0]) > 0:
			matches += 1
			sender.sendMessage(Color("f") + '/' + ChatColor.GRAY + Color("f") + help[i]['short'])

	if matches == 0:
		sender.sendMessage(Color("c") + '====' + Color("4") + 'No matches found' + Color("c") + '====')
	else:
		sender.sendMessage(Color("e") + '====' + Color("c") + str(matches) + Color("6") + 'matches found' + Color("e") + '====')

	return True
