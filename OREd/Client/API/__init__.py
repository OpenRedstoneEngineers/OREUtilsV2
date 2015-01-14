# This will contain static items of API
# like Console()
import API.Console
import API.Logger
from collections import defaultdict


class Base(object):
    Consoles = defaultdict(Console.Console)
    Loggers = defaultdict(Logger.Logger)

    @classmethod  # Dot is gonna hate this. - Xeo
    def LoadAPI(cls, serverName):
        cls.Console = cls.Consoles[serverName]
        cls.Logger = cls.Loggers[serverName]
