from Node import *

from DictBackend import *

from os.path import isfile as Exists

class NodeManager:
	def __init__(self, data=None, backend=DictBackend):
		self.backend = backend()
		self.node = Node()

		if isinstance(data, dict): 
			self.backend.LoadDict(self.node, data)
		elif isinstance(data, str):
			self.backend.FromStr(self.node, data)

	def __str__(self):
		return self.backend.ToStr(self.node)

	def Dict(self):
		return self.node.Dict()

class NodeFile(NodeManager):
	def __init__(self, filename, backend=DictBackend, read=True):
		if Exists(filename) and read:
			data = open(filename).read()
		else:
			data = None

		self.filename = filename

		NodeManager.__init__(self, data, backend)

	def Dump(self):
		open(self.filename, 'w').write(str(self))
		print str(self)
