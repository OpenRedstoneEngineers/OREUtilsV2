from __future__ import division 

from Helper import Sudo 

import org.bukkit.Bukkit.dispatchCommand as dispatchCommand 
import org.bukkit.Bukkit.getPlayerExact	 as getPlayerExact

'''
Permission nodes:

ore.nameformat.others
'''

# Whitelist
Colours = '123456789abcdef'
Fonts = 'lnor'

Presets = {
	'rainbow'   : '4c6e23915d',
	'ice'       : 'f7b3b7f',
	'greyscale' : '87f',
	'england'   : 'f4f4f4f4f4f4f4f4f4f',
	'pink'      : 'dl',
	'reset'     : 'f',
	'fire'      : 'e646e'
}

def Distribute(list1, list2):
	len1   = len(list1)
	change = len1 / float(len(list2))
	
	while len1 > 0:
		len1 -= change

		list1.insert(int(len1), list2.pop())

	return ''.join(list1)

@hook.command("nameformat", description="Colourify your name", usage="Usage: /nameformat [name] <format...>")
def onCommandNameFormat(sender, args):
	if not args:
		return False

	target = sender

	if target.hasPermission('ore.nameformat.others'):
		player = getPlayerExact(args[0])

		if player != None:
			target = player

			del args[0]

	for argi, arg in enumerate(args):	
		preset = Presets.get(arg)

		if preset:
			args[argi] = preset

	formats = []

	for format in ''.join(args):
		if format in Colours:
			formats.append('&' + format)

		elif format in Fonts:
			formats[-1] += '&' + format

		elif format == ' ' and formats[-1]:
			formats.append('')

		else:
			sender.sendMessage('Invalid colour code (' + format + ')')
			return False

	name = target.getName()

	if formats:
		Sudo('nick ' + name + ' ' + Distribute(list(name), formats))

		return True

	return False
