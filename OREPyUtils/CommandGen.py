import re, sys

Arg = re.compile('\[[^\]]+\]'  )
Gap = re.compile("[\+]*''[\+]*")
Int = re.compile('[-]*[0-9]+'  )
Bra = re.compile('#{[^}]+#}'   )

Formats =  {
	'p':'exec %s',
	's':'Sudo(%s)',
	'r':'dispatchCommand(sender,%s)',
	't':'sender.sendMessage(%s)',
	'NoFlag':'broadcastMessage(%s)'
}

Colours = {'black'    :'0',
               'blue'     :'1',
               'green'    :'2',
               'cyan'     :'3',
               'red'      :'4',
               'purple'   :'5',
               'orange'   :'6',
               'lgrey'    :'7',
               'grey'     :'8',
               'lblue'    :'9',
               'lgreen'   :'a',
               'aqua'     :'b',
               'lred'     :'c',
               'pink'     :'d',
               'yellow'   :'e',
               'white'    :'f',
               'bold'     :'l',
               'underline':'n',
               'strike'   :'m',
               'italic'   :'o',
               'random'   :'k',
               'clear'    :'r'}

GlobalHat = '''
from Helper import Sudo
from Helper import Color #Deprecated #STFU

from org.bukkit.Bukkit import broadcastMessage, dispatchCommand, getPlayer

def GetName(Name):
	Player = getPlayer(Name)

	if Player == None:
		return Name

	return Player.getName()
'''

class Command:
	def __init__(self, Command):
		self.Locals     = set()
		self.Code       = []
		self.Lines      = [X.strip() for X in Command.split(':')]
		self.ArgsNeeded = 0

		self.GenCode()
		self.GenHat()

	def GenHat(self):
		Hat = []
		Args = [X.strip() for X in self.Lines[0].split('|')]

		Hat = ["@hook.command('%s')"            % "',descripion = '".join(Args),
		       "def onCommand%s(sender, args):" % Args[0]]
        
		if self.ArgsNeeded:
			Hat += ["\tif len(args) < %s :"                           % self.ArgsNeeded,
			        "\t\tsender.sendMessage('You need %s arguments')" % self.ArgsNeeded,
			        "\t\treturn False"]
		
		for Local in self.Locals:
			Hat.append('\t' + Local)  
		
		self.Code = Hat + self.Code
	
	def GenCode(self):
		for Line in self.Lines[1:]:
			LineFormat = Formats['NoFlag'] 
			Special    = set(Arg.findall(Line))

			for Command in Special:
				Original = Command
				Args     = [X.strip().rstrip() for X in Command[1:-1].split('|')]
				First    = Args[0]

				if First in Formats:
					LineFormat = Formats[First]
					Command = ''
				
				elif First == 'c':
					if len(Args) < 2:
						continue

					if Args[1] in Colours.keys():
						Command = "Color('" + Colours[Args[1]] + "')"

					else:
						Command = "Color('" + Args[1] + "')"

				elif First == 'n':
					Command = 'Name'
					self.Locals.add('Name = sender.getName()')

				elif First == 'a':
					if len(Args) == 1:
						Command = 'AllArgs'
						self.Locals.add("AllArgs = ' '.join(args)")

					elif len(Args) > 1:
						if Int.match(Args[-1]):
							ArgInd = int(Args[-1])

							if 'n' in Args:
								Command = 'NameArg%s' % ArgInd
								self.Locals.add('NameArg%s = GetName(args[%s])' % (ArgInd,ArgInd))

							else:
								Command = 'args[' + Args[-1]+  ']'

							self.ArgsNeeded = max(self.ArgsNeeded,ArgInd+1)
				
				Line = Line.replace(Original, "'+" + Command + "+'")

			Line = '+'.join([X for X in Gap.split("'" + Line + "'") if X])

			self.Code.append('\t' + LineFormat % Line)

def Commands(Lines):
	Final = [GlobalHat]

	for Line in Lines:
		if Line.startswith('::'):
			continue
		Final.append('\n'.join(Command(Line.replace("'",r"\'")).Code))

	return '\n\n'.join(Final)

def GenCommands(fileIn = None,fileOut = None, *extra):
	if not fileOut: 
		fileTo = sys.stdout
	else:
		try:
			fileTo = open(fileOut,'w')
		except:
			return 'Cannot open file out'
		
	if not fileIn:
		fileFrom = sys.stdin
	else:
		try:
			fileFrom = open(fileIn)
		except:
			return 'Cannot open file in'
	
	Final = Commands(fileFrom.read().strip().split('\n'))
	fileTo.write(Final)
	fileTo.close()
	return 'Operation sucessful'

if __name__ == "__main__":
	print GenCommands('/servers/test/plugins/OREUtilsV2.py.dir/Data/Commands.txt','ResultCode.py')
	exit()

@hook.command('gencommands')
def onCommandGen(sender,args):
	if sender.hasPermission('ore.gencommand'):
		sender.sendMessage(GenCommands('Commands.txt','plugins/OREUtilsV2.py.dir/OREPyUtils/ResultCode.py'))
	else:
		sender.sendMessage('No permission')
	return True
		
