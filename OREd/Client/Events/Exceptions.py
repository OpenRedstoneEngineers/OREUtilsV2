from Events import Event

#Something has gone wrong.
class ServerException(Event):
	pass

#An error produced by a plugin
class PluginException(ServerException):
	pass

#An error produced by a plugin while enabling @@@
class EnableException(PluginException):
	pass

#An error produced by a plugin while disabling @@@
class DisableException(PluginException):
	pass

#The server has become inoperable
class CriticalException(ServerException):
	pass

#The server is no longer responding @@@
class TimeoutException(CriticalException):
	pass

#The server has eaten all the RAM
class RAMException(CriticalException):
	pass

#The server has eaten all RAM and Java is stupid @@@
class UnhandledRAMException(RAMException):
	pass

#The server has eaten all RAM and Java has killed itself @@@
class HandledRAMException(RAMException):
	pass

#The server is eating all CPU @@@
class CPUException(CriticalException):
	pass


    
