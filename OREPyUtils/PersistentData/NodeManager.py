from Node import *

from JSONBackend import *

from os.path import isfile as Exists

class Backend:
	def Load(node, data):
		pass

	def Save(node):
		pass

class NodeManager:
	def __init__(self, data=None, backend=JSONBackend):
		self.backend = backend()
		self.node = Node()

		if isinstance(data, dict): 
			self.Load(self.node, data)

		elif isinstance(data, str):
			self.backend.Load(self.node, data)

	def __str__(self):
		return self.backend.Save(self.node)

	def Dict(self):
		return self.node.Dict()

	def Load(node, x):
		for item, value in x.iteritems():
			if isinstance(value, dict):
				node[item] = Node()

				self.Load(node[item], value)		
			else:
				node[item] = value

class NodeFile(NodeManager):
	def __init__(self, filename, backend=JSONBackend, read=True):
		if Exists(filename) and read:
			data = open(filename).read()
		else:
			data = None

		self.filename = filename

		NodeManager.__init__(self, data, backend)

	def Dump(self):
		open(self.filename, 'w').write(str(self))
		print str(self)
