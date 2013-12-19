from __future__ import division
import math as m
import random, os
import org.bukkit.Bukkit.dispatchCommand  as runas
import org.bukkit.Bukkit.getPlayer        as getPlayer
import org.bukkit.Bukkit.broadcastMessage as bcast

from Helper import color,Info


help = {}
keys = []

#[Numbers,Constants,().,+-]
colourschemes = [['3','1','9','7']]
colour = 'f'
comp = []
appeneded = False
Times = {}


def OnEnable(**kwargs):
	global help,keys
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

	for Ind in range(0,len(String),2):
		try:
			Final.append(chr(int(String[Ind:Ind+2],16)))

		except:
			sender.sendMessage('Invalid Char!')
			break
	sender.sendMessage(''.join(Final))

	return True

def Calc(calc,sender):
    calc = calc.lower()
    lbs = calc.count('(')
    rbs = calc.count(')')

    if lbs > 0 and rbs > 0:
        c=0

        for i in calc:
            if i == '(':
                c+=1

            elif i == ')':
                c-=1

                if c<0:
                    return None

        if c>0:
            return None
    
    wlist = '0123456789*+-/^|&~.,() '

    calc = calc.replace('abs(','fabs(')
    calc = calc.replace('deg(','dEgrEEs(')
    calc = calc.replace('rad(','radians(')
    calc = calc.replace('rand()','random()')
    calc = calc.replace('ceil()','cEil(')
    calc = calc.replace('^','**')
    calc = calc.replace(' xor ','^')
    calc = calc.replace(' and ','&')
    calc = calc.replace(' or ','|')
    calc = calc.replace('not ','~')
    calc = calc.replace('pi','('+str(m.pi)+')')
    calc = calc.replace('e','('+str(m.e)+')')
    calc = calc.lower()
    

    funcs = ['cos','sin','tan','acos','asin','atan','sqrt','acosh','asinh','atanh','cosh','sinh','tanh','ceil','floor','fabs','gamma','lgamma','degrees','radians','log']
    calc2=calc

    for j in funcs:
        i=j+'('
        calc = calc.replace(i,'(')
        calc2= calc2.replace(i,'m.'+i)

    rfuncs = ['random','randint','uniform','randrange']

    for j in rfuncs:
        i=j+'('
        calc = calc.replace(i,'(')
        calc2= calc2.replace(i,'random.'+i)
    
    for i in calc:
        if not i in wlist:
            sender.sendMessage("The character %s is not allowed! Allowed characters: "%i+wlist)

            return ValueError

    try:
        q = eval(calc2)

    except:
        return None
    return q

@hook.command("calc", description="Calculate things!")
def onCommandCalc(sender,args):
    global colour, appended, comp

    if len(args)==0:
        sender.sendMessage('This function requires an expression to calculate!')
        return False

    if ''.join(args).count('*') > 1:
        sender.sendMessage('NO. * *s')
        return False

    if '^' in ''.join(args):
        sender.sendMessage('NO. ^s')
        return False

    c=Calc(' '.join(args),sender)

    if c==None:
        sender.sendMessage('Invalid expression!')
        return False

    elif c==ValueError:
        return False

    sta = ''.join(args)
    sta = sta.replace('deg(','dEgrEEs(')
    sta = sta.replace('ceil()','cEil(')
    sta = list(sta.replace('pi','PI'))
    comp = []
    colour = '7'
    cs = random.choice(colourschemes)

    for a in sta:
        appended = False

        if a.isdigit():
            coladd(cs[0])

        if 'ePI'.find(a) != -1:
            coladd(cs[1])

        if '(),.'.find(a) != -1:
            coladd(cs[2])

        if not appended:
            coladd(cs[3])
        comp.append(a)

    sender.sendMessage(color('7') + ''.join(comp).lower() + color('7') + " = " + color('3') + color('l') + str(c))

    return True 

def coladd(c):
    global colour, comp, appended
    appended = True

    if colour != c:
        colour = c
        comp.append(color("c"))#?

#Rename
@hook.command('rename', description='Rename the item in your hand')
def onCommandLore(sender, args):
    if len(args) == 0:
        sender.sendMessage(color("c") + 'You must have a name!')
        return False

    argstring = ' '.join(args).replace('#f',u'\u00A7')
    I = sender.getItemInHand()
    Imeta = I.getItemMeta()
    Imeta.setDisplayName(argstring)
    I.setItemMeta(Imeta)
    return True

@hook.command('e')
def onCommandBookGet(sender, args):
    item = sender.getItemInHand()

    if item.getTypeId() not in (386,387):
        sender.sendMessage(color("c") + 'You must have a book')
        return False

    # YAY for descriptive names -Dot
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
                bcast(color("e") + s[n][2:] + color("6") + ' ('+ sender.getName() + ')')
            elif command.split()[0] != 'e':
                runas(sender, command)
 
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
            bcast(color("e") + i[2:] + color("6") + ' ('+sender.getName()+')')
        elif i.split()[0] != 'e':
            runas(sender, i)
        n += 1

    sender.sendMessage(color("a") + 'Command(s) run!')

    return True

@hook.command('schems')
def onCommandSchems(sender, args):
    Name = sender.getName()
    try:
        UserSchems = os.listdir('/var/www/schems/files/'+Name)
    except:return False
    if len(args) == 2:
        Sub = args[0]
        if Sub   in ('load','save'):
            runas(sender,'/schematic '+Sub+' '+Name+'/'+args[1].split('/')[0])
            return True
    elif len(args) == 1:
        Sub = args[0]
        if Sub ==  'list':
            sender.sendMessage('List of your schematics:')
            for item in UserSchems:
                sender.sendMessage(item)
            return True

    sender.sendMessage('/schems list | load <name> | save <name>')

@hook.command('pass')
def passset(sender, args):
    runas(sender,'dbp set '+' '.join(args))
    return True

@hook.command('orehelp')
def onCommandOREHelp(sender,args):
	if len(args) == 0:
		matches = len(keys)

		for i in keys:
			sender.sendMessage(color("e") + '/' + color("6") + i + color("e") + help[i]['short'])

	elif args[0] in keys:
		matches = 1

		sender.sendMessage(color("a") + '/' + color("2") + args[0] + color("a") + help[args[0]]['long'])
	else:       
		matches = 0 

	for i in keys:
		if i.find(args[0]) == 0:
			matches += 1
			sender.sendMessage(color("e") + '/' + color("6") + i + color("e") + help[i]['short'])

	for i in keys:
		if i.find(args[0]) > 0:
			matches += 1
			sender.sendMessage(color("f") + '/' + ChatColor.GRAY + color("f") + help[i]['short'])

	if matches == 0:
		sender.sendMessage(color("c") + '====' + color("4") + 'No matches found' + color("c") + '====')
	else:
		sender.sendMessage(color("e") + '====' + color("c") + str(matches) + color("6") + 'matches found' + color("e") + '====')

	return True
