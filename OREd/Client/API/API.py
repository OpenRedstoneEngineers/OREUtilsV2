#This will contain static items of API
#like Console()
from Console import Console as console
from Logger import Logger as logger

class Base(object):
	Console = console()
	Logger  = logger()
