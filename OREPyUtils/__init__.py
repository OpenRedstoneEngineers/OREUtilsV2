import sys

from Helper import Info, Severe

from PersistentData import *

Failiures = {}

DATA_PATH = "plugins/OREPyUtilsV2.py.dir/Data/"

class ConfigFile(NodeFile):
	def __init__(self):
		NodeFile.__init__(self, DATA_PATH + "config.dict")

		if 'properties' not in self.node:
			self.node.properties = Node()
	
	def __getitem__(self, name):
		if name in self.node.properties:
			return self.node.properties[name]
		
		else:
			return None

	def __setitem__(self, name, value):
		if value == None:
			if name in self.node.properties:
				del self.node.properties[name]

		else:
			self.node.properties[name] = value

CONFIG  = ConfigFile()

Include = CONFIG['Include']

if not isinstance(Include, list):
	Include = [
		'CommandGen',
		'Aliases',
		'FunCommands',
		'Derps',
		'NameSystem',
		'UsefulCommands',
		'EventHooks',
		'ChannelChat',
		'Plots',
		'IRCBot',
		'ResultCode'
	]

	CONFIG['Include'] = Include

for N in Include:
        try:
                exec 'import ' + N

        except Exception, E:
                print '[!]Error importing ' + N

                Failiures[N] = str(E)

        else:
                print '[i]Imported ' + N

@hook.command('property', description='Plugin properties')
def onCommandProperty(sender, args):
	if not sender.hasPermission("ore.config"):
		sender.sendMessage("No permission!")
		return True

	if len(args) == 0:
		sender.sendMessage(str(CONFIG))

	elif len(args) == 1:
		sender.sendMessage(args[0] + "=" + str(CONFIG[args[0]]))
	
	elif len(args) >= 2:
		if args[1] == 'None':
			CONFIG[args[0]] = None
		else:
			try:
				CONFIG[args[0]] = Eval(' '.join(args[1:]))

			except:
				sender.sendMessage('/property [property] [set to]')

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
			Plots.Frontend.InitManagers()

		except Exception , E:
			Severe("[!]Error starting plot system")

			Failiures['Plots'] = str(E)

	if 'Derps' not in Failiures:
		try:
			Derps.LoadDerps(DATA_PATH + "Derps.txt")

		except Exception , E:
			Severe('[!]Error loading derps')

			Failiures['Derps'] = str(E)

	if 'UsefulCommands' not in Failiures:
		try:
			UsefulCommands.LoadHelp(DATA_PATH + "Help.txt")

		except Exception , E:
			Severe('[!]Error loading help')

			Failiures['UsefulCommands'] = str(E)

	if "IRCBot" not in Failiures:
		try:
			IRCBot.Init("irc.freenode.net", 6667, "ORETest", "****", "#OREServerChat")

		except Exception , E:
			Severe('[!]Error loading IRCBot')

			Failiures['IRCBot'] = str(E)

@hook.disable
def OnDisable():
	CONFIG.Dump()

	if 'Plots' not in Failiures:
		Plots.Frontend.SaveData()

	if 'IRCBot' not in Failiures:
		IRCBot.Terminate()
