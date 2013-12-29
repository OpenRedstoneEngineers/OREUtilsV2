#Something is wrong
class ServerException(BaseEvent):
    pass

#An error produced by a plugin
class PluginException(ServerException):
    pass

#An error produced by our plugin @@@
class PythonException(PluginException):
    pass

#An error produced by a plugin while enabling @@@
class EnableException(PluginException):
    pass

#An error produced by a plugin while disabling @@@
class DisableException(PluginException):
    pass

#An error produced by our plugin while enabling @@@
class PythonEnableException(PythonException, EnableException):
    pass

#An error produced by our plugin while disabling @@@
class PythonDisableException(PythonException, DisableException):
    pass

#The server has become inoperable
class ServerCriticalException(ServerException):
    pass

#The server is no longer responding @@@
class ServerTimeoutException(ServerCriticalException):
    pass

#The server has eaten all the RAM
class ServerRAMException(ServerCriticalException):
    pass

#The server has eaten all RAM and Java is stupid @@@
class ServerUnhandledRAMException(ServerRAMException):
    pass

#The server has eaten all RAM and Java has killed itself @@@
class ServerHandledRAMException(ServerRAMException):
    pass

#The server is eating all CPU @@@
class ServerCPUException(ServerCriticalException):
    pass


    
