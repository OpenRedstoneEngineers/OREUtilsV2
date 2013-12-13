import sys

from Helper import Info, Severe

from PersistentData import *

Failiures = {}

DATA_PATH = "plugins/OREUtilsV2.py.dir/Data/"

class ConfigFile(NodeFile):
	def __init__(self):
		NodeFile.__init__(self, DATA_PATH + "config.json")

		if 'properties' not in self.node:
			self.node.New('properties')
	
	def __getitem__(self, name):
		return self.node.properties.Get(name)

	def __setitem__(self, name, value):
		self.node.properties.Set(name, value)

CONFIG  = ConfigFile()

Include = CONFIG['Include']

if not isinstance(Include, list):

	Include = []
	Severe('[!]No Include list in config!')
	Failiures['All'] = 'No Include list found in config'


def ImportFiles():
	for N in Include:
        	try:
                	exec 'import ' + N

        	except Exception, E:
                	Severe('[!]Error importing ' + N)

        	        Failiures[N] = str(E)
	
        	else:
                	Info('[i]Imported ' + N)

ImportFiles()

@hook.command('property', description='Plugin properties')
def onCommandProperty(sender, args):
	if not sender.hasPermission("ore.config"):
		sender.sendMessage("No permission!")
		return True

	if len(args) == 0:
		sender.sendMessage(str(CONFIG))

	elif len(args) == 1:
		sender.sendMessage(args[0] + " = " + str(CONFIG[args[0]]))
	
	elif len(args) >= 2:
		if args[1] == 'None':
			CONFIG[args[0]] = None
		else:
			try:
				setTo = Eval(' '.join(args[1:]))

			except:
				sender.sendMessage('/property [property] [set to]')
			else:
				CONFIG[args[0]] = setTo
		CONFIG.Dump()

@hook.command('status', description = 'View module loading failiures')
def OnCommandFail(sender,args):
	if len(args) == 1:
		if args[0] in Failiures:
			sender.sendMessage('[!!]Module failed: ' + Failiures[Args[0]])
		
		elif args[0] in Include:
			sender.sendMessage('All is good')
		
		else:
			sender.sendMessage('[!]Unknown module')

	else:	
		for Fail, Reason in Failiures.iteritems():
			sender.sendMessage('[!!]' + Fail + ' has failed: ' + Reason)

	return True
	
@hook.enable
def OnEnable():
	if 'Plots' not in Failiures:
		try:
			Plots.Frontend.InitManagers(NodeFile)

		except Exception , E:

			Severe("[!]Error starting plot system")
			Failiures['Plots'] = str(E)

	if 'Derps' not in Failiures:
		if isinstance(CONFIG['DerpPath'], str):
			DerpPath = CONFIG['DerpPath'].replace('[path]', DATA_PATH)

			try:
				Derps.LoadDerps(DATA_PATH + "Derps.txt")
	
			except Exception , E:

				Severe('[!]Error loading derps')
				Failiures['Derps'] = str(E)
		
		else:
			Severe('[!]No DerpPath in config')
			Failiures['Derps'] = 'No DerpPath in config'

	if 'UsefulCommands' not in Failiures:
		if isinstance(CONFIG['HelpPath'], str):
			HelpPath = CONFIG['HelpPath'].replace('[path]', DATA_PATH)
			
			try:
				UsefulCommands.LoadHelp(HelpPath)

			except Exception , E:

				Severe('[!]Error loading help')
				Failiures['UsefulCommands'] = str(E)

		else:
			Severe('[!]No HelpPath in config')
			Failiures['UsefulCommands'] = 'No HelpPath in config'
			

	if "IRCBot" not in Failiures:
		args = []

		for conf in ['Server', 'Port', 'Name', 'NamePass', 'Chan']:
			args.append(CONFIG['IRC.'+conf])

		if None in args:
			Severe('No IRC.'+conf+' in config')
			Failiures['IRCBot'] = 'No IRC.'+conf+' in config'
				
		
		else:
			try:
				IRCBot.Init(*args)
		
			except Exception , E:

				Severe('[!]Error loading IRCBot')
				Failiures['IRCBot'] = str(E)

@hook.disable
def OnDisable():
	if 'Plots' not in Failiures:
		try:
			Plots.Frontend.SaveData()

		except Exception , E:
			Severe('[!]Error unloading Plots: '+str(E))

	if 'IRCBot' not in Failiures:
		try:
			IRCBot.Terminate()

		except Exception , E:
			Severe('[!]Error unloading IRCBot: '+str(E))
