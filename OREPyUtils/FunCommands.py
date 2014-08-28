from __future__ import division

from Helper import Sudo, Color, SendInfo, SendError, GiveItem

import random

import org.bukkit.Bukkit as Bukkit

from org.bukkit.potion import PotionEffectType
from org.bukkit.potion import PotionEffect
from org.bukkit        import Material

import re
Integer = re.compile('[-]*[0-9]+')

Food = {
	'apple'          : 260,
	'bowl of soup'   : 282,
	'loaf of bread'  : 297,
	'porkchop'       : 319,
	'fish'           : 349,
	'cake'           : 354,
	'cookie'         : 357,
	'slice of melon' : 360,
	'steak'          : 364,
	'chicken'        : 365,
	'carrot'         : 391,
	'potato'         : 392,
	'pie'            : 400
}
				
Vowels = 'aeiou'

@hook.command("foodfight", description="A polite mealtime activity")
def OnCommandFoodfight(sender,args):
	if len(args) == 0:
		SendError(sender, "You must specify who you are to throw food at.")
		return True

	Item = random.choice(Food.items())
		
	receiver = Bukkit.getPlayer(args[0])

	if receiver == None:
		SendError(sender, 'No such player.')
		return True

	GiveItem(receiver, Item[1])

	Singular = ('a ', 'an ')[Item[0][0] in Vowels]

	Name  = sender.getName()
	RName = receiver.getName()

	Bukkit.broadcastMessage(Color("5") + Name + Color("e") + " threw " + Singular + Color("6") + Item[0] + Color("c") + " at " + Color("5") + RName)

	if random.randint(1, 5) == 1:
		receiver.addPotionEffect(PotionEffect(PotionEffectType.BLINDNESS, 40, 1, True))

		Bukkit.broadcastMessage(Color("5") + "Headshot!")

	return True

@hook.command("slap", description="Slappings!")
def OnCommandFoodfight(sender,args):
	if len(args) == 0:
		SendError(sender, "Usage: /slap [Player] [Object]")
		return True

	receiver = Bukkit.getPlayer(args[0])

	if receiver == None:
		SendError(sender, 'No such player.')
		return True

	if len(args) > 1:
		item = ' '.join(args[1:])
		number = '1'

		for i in args[1:]:
			if not i.isdigit() and i != 'some':
				if number != 1:
					if i[len(i)-1:] == 's':
						Sudo(' '.join(('give',receiver.getName(),i[:len(i)-1],number)))

						if i[len(i)-2:] == 'es':
							Sudo(' '.join(('give',receiver.getName(),i[:len(i)-2],number)))

					else:
						Sudo(' '.join(('give',receiver.getName(),i,number)))

				else:  
					Sudo(' '.join(('give',receiver.getName(),i,'1')))

			number = 1

			if i == 'some':
				number = str(random.randint(2,8))

			if i.isdigit():
				number = i

		Word1 = args[1]

	else:
		item  = 'large trout'
		i     = 'fishy'
		Word1 = 'large'

		material = None

		GiveItem(receiver, 349) # Fish

	if receiver == sender:
		receiverName = 'themselves'
	else:
		receiverName = receiver.getName()

	if not (Word1 == 'some' or Word1.isdigit()):
		if Word1[0].lower() in Vowels:
			amount = 'an '
		else:
			amount = 'a '
	else:
		amount = ''

	Bukkit.broadcastMessage(Color("5") + sender.getName() + Color("c") + " slapped " + Color("5") + receiverName + Color("c") + " about a bit with " + amount + Color("6") + item)

	if random.randint(0, 1):
		receiver.addPotionEffect(PotionEffect(PotionEffectType.CONFUSION, 160, 3, True))
	else:
		receiver.addPotionEffect(PotionEffect(PotionEffectType.SLOW, 40, 1, True))

	return True
		
# Random number
@hook.command("random", description = "Produce a random number.")
def OnCommandRandom(sender,args):
	Len = len(args)

	if not Len:
		sender.sendMessage(str(random.random()))

	elif Len == 1:
		if Integer.match(args[0]):
			sender.sendMessage(str(random.randint(0,int(args[0]))))
		else:
			SendError(sender, 'Expected integer')

	elif Len == 2:
		if Integer.match(args[0]) and Integer.match(args[1]):
			sender.sendMessage(str(random.randint(int(args[0]),int(args[1])))) 
		else:	
			SendError(sender, 'Expected integer')
	else:
		SendError(sender, 'Usage: /random [A] [B]')

	return True

#effect
@hook.command("eff", description="Get a custom potion effect!")
def OnCommandItemname(sender,args):
	if len(args) == 0:
		SendError(sender, "You must have an argument -" + Color("6") + " /eff [effect] [power] [duration]" + Color("c") + " you can also use 'rem' and 'list' as effects, for special functions")
		return True
	
	if args[0] == "rem":
		if len(args) < 2:
			for effect in sender.getActivePotionEffects():
				sender.removePotionEffect(effect.getType())

			return True

		elif int(args[1]) < sender.getActivePotionEffects():
			effect = sender.getActivePotionEffects()[int(args[1])]
			sender.removePotionEffect(effect.getType())

			return True

	if args[0] == "list":		
		if len(args) < 2:
			Bukkit.dispatchCommand(sender, "e")
		else:
			Bukkit.dispatchCommand(sender, "e " + args[1])

		return True
	
	if len(args) < 3:
		SendError(sender, "You must have the correct amount of arguments -" + Color("6") + " /eff [effect] [power] [duration]")
		return True
	
	for i in range(1,2):
		if args[i].isdigit() == False:
			sender.sendMessage(Color("c") + "Your power and duration must be integers -" + Color("6") + " /eff [effect] [power] [duration]")
			return False

	args[0] = args[0].upper()
	args[0] = args[0].replace(" ", "")
	args[0] = args[0].replace(".", "")

	if len(args) == 4:
		receiver = Bukkit.getPlayer(args[3])

		if receiver == None:
			SendError("Invalid player")
			return True

	else:
		receiver = sender

	EffectStr = "PotionEffectType." + args[0]

	try:
		receiver.addPotionEffect(PotionEffect(eval(EffectStr), int(args[2]), int(args[1] - 1)))
	except: sender.sendMessage("Invalid effect")	

	return True
	
#choice
@hook.command("choose",description="For those hard important decisions that you can't leave to chance")
def OnCommandChoose(sender, args):
	if not args:
		SendError(sender, 'You must have some things to choose between')
		return True

	sender.sendMessage(Color("5") + Color("l") + 'You roll your magic dice!')
	sender.sendMessage(random.choice(args))

	return True
