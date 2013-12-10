from __future__ import division 

from Helper import Sudo 

import org.bukkit.Bukkit.dispatchCommand as dispatchCommand 
import org.bukkit.Bukkit.getPlayerExact  as getPlayerExact

# Permission nodes: 

# Color Whitelist
colours = '123456789abcdef'

# Format Whitelist
fonts = 'lnor'

# Presets
preset = {
    'rainbow'   : '4c6e23915d',
    'ice'       : 'f7b3b7f',
    'greyscale' : '87f',
    'england'   : 'f4f4f4f4f4f4f4f4f4f',
    'pink'      : 'dl',
    'reset'     : 'f',
    'fire'      : 'e646e'
}

def Distribute(list1,list2):
	len1    = len(list1)
	change  = len1/float(len(list2))
    
	while len1 > 0:
		len1 -= change
		list1.insert(int(len1),list2.pop())

	return ''.join(list1)

@hook.command("nameformat", description="Colourify your name")
def onCommandNameFormat(target, args):
	if args:
		if target.hasPermission('ore.nameformat.others'):
			player = getPlayerExact(args[0])
	
			if player != None:
				target = player

				del args[0]

		formats = []

		for format in ' '.join(args):
			if format in colours:
				formats.append('&'+format)

			elif format in fonts:
				formats[-1] += '&'+format

			elif format == ' ' and formats[-1]:
				formats.append('')

			else:
				sender.sendMessage('invalid colour code ('+format+')')

				return False

		name = target.getName()

		if formats:
			Sudo('nick '+name+' '+Distribute(list(name), formats))

			return True
	
	sender.sendMessage('/nameformat [name] <colours...>')
	
	return False

#rankdown
@hook.command("rankup", description="Promote a user.")
def onCommandRankup(sender, args):
    if len(args) == 1:
        dispatchCommand(sender, "pex promote "+args[0])
        return True

    return False

#rankdown
@hook.command("rankdown", description="Demote a user.")
def onCommandRankdown(sender,args):
    if len(args) == 1:
        dispatchCommand(sender, "pex demote "+args[0])
        return True

    return False

#fixname
@hook.command('fixname', description='Fix your name formatting.')
def onCommandFixname(sender,args):
    Sudo('nick '+sender.getName()+' off')
    return True
