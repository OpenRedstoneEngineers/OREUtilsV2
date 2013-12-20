
from Helper import Sudo
from Helper import Color #Deprecated #STFU

from org.bukkit.Bukkit import broadcastMessage, dispatchCommand, getPlayer

def GetName(Name):
	Player = getPlayer(Name)

	if Player == None:
		return Name

	return Player.getName()


@hook.command('day',descripion = 'Set time to day')
def onCommandday(sender, args):
	sender.sendMessage('Your time was set to day')
	exec 'Sender.setPlayerTime(6000,0)'

@hook.command('night',descripion = 'Set time to night')
def onCommandnight(sender, args):
	sender.sendMessage('Your time was set to night')
	exec 'Sender.setPlayerTime(18000,0)'

@hook.command('c',descripion = 'View format codes')
def onCommandc(sender, args):
	sender.sendMessage(Color('a')+'a'+Color('b')+'b'+Color('c')+'c'+Color('d')+'d'+Color('e')+'e'+Color('f')+'f'+Color('l')+'l'+Color('r')+Color('m')+'m'+Color('r')+Color('n')+'n'+Color('r')+Color('o')+'o')
	sender.sendMessage(Color('1')+'1'+Color('2')+'2'+Color('3')+'3'+Color('4')+'4'+Color('5')+'5'+Color('6')+'6'+Color('7')+'7'+Color('8')+'8'+Color('9')+'9'+Color('0')+'0')

@hook.command('lemur',descripion = 'Bark like a lemur')
def onCommandlemur(sender, args):
	Name = sender.getName()
	broadcastMessage(Color('e')+Name+Color('f')+' Barks and screeches like a lemur')

@hook.command('moo',descripion = 'Moo like a cow')
def onCommandmoo(sender, args):
	Name = sender.getName()
	broadcastMessage(Color('e')+Name+Color('f')+' Moos like a cow')

@hook.command('oink',descripion = 'Oink like a pig')
def onCommandoink(sender, args):
	Name = sender.getName()
	broadcastMessage(Color('e')+Name+Color('f')+' Oinks like a pig')

@hook.command('cluck',descripion = 'Cluck like a chicken')
def onCommandcluck(sender, args):
	Name = sender.getName()
	broadcastMessage(Color('e')+Name+Color('f')+' Clucks like a chicken')

@hook.command('bark',descripion = 'Bark like a dog')
def onCommandbark(sender, args):
	Name = sender.getName()
	broadcastMessage(Color('e')+Name+Color('f')+' Barks like a dog')

@hook.command('baa',descripion = 'Baa like a sheep')
def onCommandbaa(sender, args):
	Name = sender.getName()
	broadcastMessage(Color('e')+Name+Color('f')+' Baas like a sheep')

@hook.command('brains',descripion = 'Brraaiinnss')
def onCommandbrains(sender, args):
	Name = sender.getName()
	broadcastMessage(Color('e')+Name+Color('f')+' Brains like a zombie')

@hook.command('sss',descripion = 'Sss like a creeper')
def onCommandsss(sender, args):
	Name = sender.getName()
	broadcastMessage(Color('e')+Name+Color('f')+' Sses like a creeper')

@hook.command('confuse',descripion = 'errrrrm')
def onCommandconfuse(sender, args):
	Name = sender.getName()
	broadcastMessage(Color('e')+Name+Color('f')+' has ALL the confusion')

@hook.command('nope',descripion = 'Nope.avi')
def onCommandnope(sender, args):
	sender.sendMessage('Chuck testa')

@hook.command('forgive',descripion = 'I\'m sorry')
def onCommandforgive(sender, args):
	if len(args) < 1 :
		sender.sendMessage('You need 1 arguments')
		return False
	NameArg0 = GetName(args[0])
	Name = sender.getName()
	broadcastMessage(Color('6')+Name+Color('5')+' forgives '+Color('6')+NameArg0)

@hook.command('lag',descripion = 'Fix the server\'s lag')
def onCommandlag(sender, args):
	Name = sender.getName()
	Sudo('kick '+Name+' No more lag <3, Mort')

@hook.command('huzza',descripion = 'HUZZZAH')
def onCommandhuzza(sender, args):
	Name = sender.getName()
	broadcastMessage(Color('6')+Name+Color('5')+' yells HUZZA')
	dispatchCommand(sender,'suicide')

@hook.command('lol',descripion = 'haha')
def onCommandlol(sender, args):
	Name = sender.getName()
	broadcastMessage(Color('e')+Name+Color('6')+' lol\'d')

@hook.command('cp',descripion = 'Such lag')
def onCommandcp(sender, args):
	sender.sendMessage('OMG, lagggg')

@hook.command('rage',descripion = 'grrrr')
def onCommandrage(sender, args):
	Name = sender.getName()
	broadcastMessage(Color('4')+Color('l')+Name+' '+Color('c')+Color('l')+'rages')

@hook.command('hap',descripion = 'haphap')
def onCommandhap(sender, args):
	Name = sender.getName()
	broadcastMessage(Color('d')+Name+' '+Color('5')+'haphaphap\'d')

@hook.command('facepalm',descripion = '..No')
def onCommandfacepalm(sender, args):
	Name = sender.getName()
	broadcastMessage(Color('b')+Name+' '+Color('9')+'facepalms')

@hook.command('love',descripion = 'Awww')
def onCommandlove(sender, args):
	AllArgs = ' '.join(args)
	Name = sender.getName()
	broadcastMessage('3')
	broadcastMessage(Color('d')+Name+' '+Color('4')+Color('l')+'<3 '+Color('d')+AllArgs)

@hook.command('hug',descripion = 'for someone you love')
def onCommandhug(sender, args):
	if len(args) < 1 :
		sender.sendMessage('You need 1 arguments')
		return False
	NameArg0 = GetName(args[0])
	Name = sender.getName()
	broadcastMessage(Color('d')+Name+' '+Color('4')+Color('l')+'hugged '+Color('d')+NameArg0)

@hook.command('mistake',descripion = 'odder')
def onCommandmistake(sender, args):
	Name = sender.getName()
	broadcastMessage(Color('4')+'Ohder '+Color('6')+Color('l')+Name+' '+Color('5')+'made a mistake')

@hook.command('waffle',descripion = 'tasty...')
def onCommandwaffle(sender, args):
	Name = sender.getName()
	broadcastMessage(Color('e')+'Guess who likes waffles; '+Color('6')+Color('l')+Name+' '+Color('e')+'does!')

@hook.command('massage',descripion = 'mmmm...')
def onCommandmassage(sender, args):
	if len(args) < 2 :
		sender.sendMessage('You need 2 arguments')
		return False
	NameArg0 = GetName(args[0])
	Name = sender.getName()
	broadcastMessage(Color('d')+Name+' '+Color('4')+'massaged '+Color('d')+NameArg0+'\'s '+args[1])

@hook.command('snuggle',descripion = 'for someone you love')
def onCommandsnuggle(sender, args):
	if len(args) < 1 :
		sender.sendMessage('You need 1 arguments')
		return False
	NameArg0 = GetName(args[0])
	Name = sender.getName()
	broadcastMessage(Color('d')+Name+' '+Color('4')+Color('l')+'snuggled with '+Color('d')+NameArg0)

@hook.command('hate',descripion = ';-;')
def onCommandhate(sender, args):
	AllArgs = ' '.join(args)
	Name = sender.getName()
	broadcastMessage(Color('a')+Name+' '+Color('2')+Color('l')+'hates '+Color('a')+AllArgs)

@hook.command('fixname',descripion = 'Turn your nick off')
def onCommandfixname(sender, args):
	Name = sender.getName()
	Sudo('nick '+Name+' off')

@hook.command('art',descripion = 'Dat colour')
def onCommandart(sender, args):
	broadcastMessage(Color('a')+'Green is '+Color('2')+Color('l')+'NOT '+Color('a')+'a creative colour.')