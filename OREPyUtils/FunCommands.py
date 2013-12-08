from __future__ import division

from Helper import Sudo, color

import random

import org.bukkit.Bukkit as Bukkit

from org.bukkit.potion import PotionEffectType
from org.bukkit.potion import PotionEffect
import org.bukkit.Material as Material

import re
Integer = re.compile('[-]*[0-9]+')

itemnamewhitelist = "1234567890abcdeflmnok"

Food = {
	'apple':'260',
	'bowl of soup':'282',
	'loaf of bread':'297',
	'porkchop':'319',
	'fish':'349',
	'cake':'354',
	'cookie':'357',
	'slice of melon':'360',
	'steak':'364',
	'chicken':'365',
	'carrot':'391',
	'potato':'392',
	'pie':'400'
}
				
vowels = 'aeiou'

#food fight
@hook.command("foodfight", description="A polite mealtime activity")
def onCommandFoodfight(sender,args):
	if len(args) == 0:
		sender.sendMessage(color("c") + "You must specify who you are to throw food at.")
		return False

	Item = random.choice(Food.items())
		
	receiver = Bukkit.getPlayer(args[0])

	if receiver == None:
		sender.sendMessage(color("c") + 'No such player.')
		return False

	Sudo("give " + args[0] + ' ' + Item[1] + " 1")

	Singular = ('a ', 'an ')[Item[0][0] in vowels]

	Name  = sender.getName()
	RName = receiver.getName()

	Bukkit.broadcastMessage(color("5") + Name + color("e") + " threw "+ Singular + color("6") + Item[0] + color("c") + " at " + color("5") + RName)

	if random.randint(1,5) == 1:
		receiver.addPotionEffect(PotionEffect(PotionEffectType.BLINDNESS, 40, 1, True))
		Bukkit.broadcastMessage(color("5") + "Headshot!")

	return True

#slap
@hook.command("slap", description="Slappings!")
def onCommandFoodfight(sender,args):
    if len(args) == 0:
        sender.sendMessage(color("c") + "/slap [Player] [Thing]")
        return False

    receiver = Bukkit.getPlayer(args[0])

    if receiver == None:
        sender.sendMessage(color("c") + 'No such player.')
        return False

    if len(args) > 1:
        item = ' '.join(args[1:])
        number = '1'
        for i in args[1:]:
            if not i.isdigit() and i != 'some':
                if number != 1:
                    if i[len(i)-1:] == 's':
                        sudo(' '.join(('give',receiver.getName(),i[:len(i)-1],number)))
                        if i[len(i)-2:] == 'es':
                            Sudo(' '.join(('give',receiver.getName(),i[:len(i)-2],number)))
                    else:
                        Sudo(' '.join(('give ',receiver.getName(),i,number)))
                else:  
                    Sudo(' '.join(('give ',receiver.getName(),i,'1')))
            number = 1
            if i == 'some':
                number = str(random.randint(2,8))
            if i.isdigit():
                number = i
	Word1 = args[1]
    else:
        item = 'large trout'
        Sudo('give '+receiver.getName()+' fish 1')
        i = 'fishy'
	Word1 = 'large'
        material = None

    if receiver == sender:
        receiverName = 'themselves'
    else:
        receiverName = receiver.getName()

    if not (Word1 == 'some' or Word1.isdigit()):
        if Word1[0].lower() in vowels:
            amount = 'an '
        else:
            amount = 'a '
    else:
        amount = ''

    Bukkit.broadcastMessage(color("5") + sender.getName() + color("c") + " slapped " + color("5") + receiverName + color("c") + " about a bit with " + amount + color("6") + item)

    if random.randint(0,1):
        receiver.addPotionEffect(PotionEffect(PotionEffectType.CONFUSION, 160, 3, True))
    else:
        receiver.addPotionEffect(PotionEffect(PotionEffectType.SLOW, 40, 1, True))

    return True
        
    

# Random number
@hook.command("random", description = "Produce a random number.")
def onCommandRandom(sender,args):
	Len = len(args)
	if not Len:
		sender.sendMessage(str(random.random()))
	elif Len == 1:
		if Integer.match(args[0]):
			sender.sendMessage(str(random.randint(0,int(args[0]))))
		else:
			sender.sendMessage('That\'s no integer')
	elif Len == 2:
		if Integer.match(args[0]) and Integer.match(args[1]):
			sender.sendMessage(str(random.randint(int(args[0]),int(args[1])))) 
		else:	
			sender.sendMessage('That\'s no integer')
	else:
		sender.sendMessage('/random [A] [B]')
	return True

#effect
@hook.command("eff", description="Get a custom potion effect!")
def onCommandItemname(sender,args):
    if len(args) == 0:
        sender.sendMessage(color("c") + "You must have an argument -" + color("6") + " /eff [effect] [power] [duration]" + color("c") + " you can also use 'rem' and 'list' as effects, for special functions")
        return False
    
    if args[0] == "rem":
        if len(args) < 2:
            for effect in sender.getActivePotionEffects():
                sender.removePotionEffect(effect.getType())
            return True
        elif int(args[1]) < sender.getActivePotionEffects():
            effect = sender.getActivePotionEffects()[int(args[1])]
            sender.removePotionEffect(effect.getType())
            return True
    if args[0] == "list" and len(args) > 0:
        
        if len(args) < 2:
            Bukkit.dispatchCommand(sender,"e")
        
        else:
            Bukkit.dispatchCommand(sender,"e "+args[1])
        return True
    
    if len(args) < 3:
        sender.sendMessage(color("c") + "You must have the correct amount of arguments -" + color("6") + " /eff [effect] [power] [duration]")
        return False
    
    for i in range(1,2):
        if args[i].isdigit() == False:
            sender.sendMessage(color("c") + "Your power and duration must be integers -" + color("6") + " /eff [effect] [power] [duration]")
            return False

    args[0] = args[0].upper()
    args[0] = args[0].replace(" ","")
    args[0] = args[0].replace(".","")

    if len(args) == 4:
        receiver = Bukkit.getPlayer(args[3])
        if receiver == None:
            sender.sendMessage(color("c") + "Invalid player")
            return False
    else:
        receiver = sender

    receiver.addPotionEffect(PotionEffect(eval("PotionEffectType."+args[0]+int(args[2])+(int(args[1])-1))))
    
    return True
    
#choice
@hook.command("choose",description="For those hard important decisions that you can't leave to chance")
def onCommandChoose(sender, args):

	if not args:
		sender.sendMessage(color("c") + 'You must have some things to choose between')
		return False

	sender.sendMessage(color("5") + color("l") + 'You roll your magic dice!')
	sender.sendMessage(random.choice(args))

	return True
