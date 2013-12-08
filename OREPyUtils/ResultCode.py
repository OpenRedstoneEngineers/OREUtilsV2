
from Helper import Sudo
from Helper import color #Deprecated #STFU

from org.bukkit.Bukkit import broadcastMessage, dispatchCommand, getPlayer

def GetName(Name):
	Player = getPlayer(Name)

	if Player == None:
		return Name

	return Player.getName()


@hook.command('day',descripion = 'Set your time to day')
def onCommandday(sender, args):
	sender.sendMessage('Your time was set to day')
	exec 'sender.setPlayerTime(6000,0)'

@hook.command('night',descripion = 'Set your time to night')
def onCommandnight(sender, args):
	sender.sendMessage('Your time was set to night')
	exec 'sender.setPlayerTime(18000,0)'

@hook.command('c',descripion = 'View chat formatting codes')
def onCommandc(sender, args):
	sender.sendMessage(color('a')+'a'+color('b')+'b'+color('c')+'c'+color('d')+'d'+color('e')+'e'+color('f')+'f'+color('l')+'l'+color('r')+color('m')+'m'+color('r')+color('n')+'n'+color('r')+color('o')+'o')
	broadcastMessage(color('1')+'1'+color('2')+'2'+color('3')+'3'+color('4')+'4'+color('5')+'5'+color('6')+'6'+color('7')+'7'+color('8')+'8'+color('9')+'9'+color('0')+'0')

@hook.command('lemur',descripion = 'Bark like a lemur')
def onCommandlemur(sender, args):
	Name = sender.getName()
	broadcastMessage(color('e')+Name+color('f')+' Barks and screeches like a lemur')

@hook.command('moo',descripion = 'Moo like a cow')
def onCommandmoo(sender, args):
	Name = sender.getName()
	broadcastMessage(color('e')+Name+color('f')+' Moos like a cow')

@hook.command('oink',descripion = 'Oink like a pig')
def onCommandoink(sender, args):
	Name = sender.getName()
	broadcastMessage(color('e')+Name+color('f')+' Oinks like a pig')

@hook.command('cluck',descripion = 'Cluck like a chicken')
def onCommandcluck(sender, args):
	Name = sender.getName()
	broadcastMessage(color('e')+Name+color('f')+' Clucks like a chicken')

@hook.command('bark',descripion = 'Bark like a dog')
def onCommandbark(sender, args):
	Name = sender.getName()
	broadcastMessage(color('e')+Name+color('f')+' Barks like a dog')

@hook.command('baa',descripion = 'Baa like a sheep')
def onCommandbaa(sender, args):
	Name = sender.getName()
	broadcastMessage(color('e')+Name+color('f')+' Baas like a sheep')

@hook.command('brains',descripion = 'Brraaiinnss')
def onCommandbrains(sender, args):
	Name = sender.getName()
	broadcastMessage(color('e')+Name+color('f')+' Brains like a zombie')

@hook.command('sss',descripion = 'Sss like a creeper')
def onCommandsss(sender, args):
	Name = sender.getName()
	broadcastMessage(color('e')+Name+color('f')+' Sses like a creeper')

@hook.command('confused',descripion = 'errrrrm')
def onCommandconfused(sender, args):
	Name = sender.getName()
	broadcastMessage(color('e')+Name+color('f')+' has ALL the confusion')

@hook.command('nope',descripion = 'Nope.avi')
def onCommandnope(sender, args):
	sender.sendMessage('Chuck testa')

@hook.command('forgive',descripion = 'I\'m sorry')
def onCommandforgive(sender, args):
	if len(args) < 1 :
		sender.sendMessage('You need 1 arguments')
		return False
	Name = sender.getName()
	NameArg0 = GetName(args[0])
	broadcastMessage(color('6')+Name+color('5')+' forgives '+color('6')+NameArg0)

@hook.command('lag',descripion = 'Fix the server\'s lag')
def onCommandlag(sender, args):
	Name = sender.getName()
	sudo('kick '+Name+' No more lag <3, RSW')

@hook.command('huzza',descripion = 'HUZZZAH')
def onCommandhuzza(sender, args):
	Name = sender.getName()
	broadcastMessage(color('6')+Name+color('5')+' yells HUZZA')
	dispatchCommand(sender,'suicide')

@hook.command('lol',descripion = 'haha')
def onCommandlol(sender, args):
	Name = sender.getName()
	broadcastMessage(color('e')+Name+color('6')+' lol\'d')

@hook.command('cp',descripion = 'Such lag')
def onCommandcp(sender, args):
	sender.sendMessage('OMG, lagggg')

@hook.command('rage',descripion = 'grrrr')
def onCommandrage(sender, args):
	Name = sender.getName()
	broadcastMessage(color('4')+color('l')+Name+' '+color('c')+color('l')+'rages')

@hook.command('hap',descripion = 'haphap')
def onCommandhap(sender, args):
	Name = sender.getName()
	broadcastMessage(color('d')+Name+' '+color('5')+'haphaphap\'d')

@hook.command('facepalm',descripion = '..No')
def onCommandfacepalm(sender, args):
	Name = sender.getName()
	broadcastMessage(color('b')+Name+' '+color('9')+'facepalms')

@hook.command('love',descripion = 'Awww')
def onCommandlove(sender, args):
	AllArgs = ' '.join(args)
	Name = sender.getName()
	broadcastMessage(color('d')+Name+' '+color('4')+color('l')+'<3 '+color('d')+AllArgs)

@hook.command('hug',descripion = 'For someone you love')
def onCommandhug(sender, args):
	if len(args) < 1 :
		sender.sendMessage('You need 1 arguments')
		return False
	Name = sender.getName()
	NameArg0 = GetName(args[0])
	broadcastMessage(color('d')+Name+' '+color('4')+color('l')+'hugged '+color('d')+NameArg0)

@hook.command('mistake',descripion = 'odder')
def onCommandmistake(sender, args):
	Name = sender.getName()
	broadcastMessage(color('4')+'Ohder '+color('6')+color('l')+Name+' '+color('5')+'made a mistake')

@hook.command('waffle',descripion = 'tasty...')
def onCommandwaffle(sender, args):
	Name = sender.getName()
	broadcastMessage(color('e')+'Guess who likes waffles; '+color('6')+color('l')+Name+' '+color('e')+'does!')

@hook.command('massage',descripion = 'mmmm...')
def onCommandmassage(sender, args):
	if len(args) < 2 :
		sender.sendMessage('You need 2 arguments')
		return False
	Name = sender.getName()
	NameArg0 = GetName(args[0])
	broadcastMessage(color('d')+Name+' '+color('4')+'massaged '+color('d')+NameArg0+'\'s '+args[1])

@hook.command('snuggle',descripion = 'mmm, you\'re so warm')
def onCommandsnuggle(sender, args):
	if len(args) < 1 :
		sender.sendMessage('You need 1 arguments')
		return False
	Name = sender.getName()
	NameArg0 = GetName(args[0])
	broadcastMessage(color('d')+Name+' '+color('4')+color('l')+'snuggled with '+color('d')+NameArg0)

@hook.command('hate',descripion = ';-;')
def onCommandhate(sender, args):
	AllArgs = ' '.join(args)
	Name = sender.getName()
	broadcastMessage(color('a')+Name+' '+color('2')+color('l')+'hates '+color('a')+AllArgs)
