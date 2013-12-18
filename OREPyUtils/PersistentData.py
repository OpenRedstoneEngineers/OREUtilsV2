from os.path import isfile as Exists

from ast import literal_eval as Eval

class DictBackend:
	def LoadDict(self, node, x):
		for item, value in x.iteritems():
			if isinstance(value, dict):
				node[item] = Node()

				self.LoadDict(node[item], value)		
			else:
				node[item] = value

	def FromStr(self, node, x):
		try:
			data = Eval(x)

		except:
			data = {}

		self.LoadDict(node, data)

	def ToStr(self, node, embed=0):
		toReturn = ["{\n"]

		for item, value in node.iteritems():
			if isinstance(value, Node):
				toReturn.append((" " * embed) + "'" + item + "' : " + self.ToStr(value, embed + 4) + ",\n")
			else:
				toReturn.append((" " * embed) + "'" + item + "' : " + repr(value) + ",\n")

		toReturn.append((" " * embed) + "}")

		return ''.join(toReturn)

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

class Node:
	def iteritems(self):
		return self.__dict__.iteritems()

	def itervalues(self):
		return self.__dict__.itervalues()

	def iterkeys(self):
		return self.__iter__()

	def __iter__(self):
		return self.__dict__.iterkeys()

	def __contains__(self, item):
		return item in self.__dict__

	def __setitem__(self, Item, To):
		self.__dict__[str(Item)] = To

	def __getitem__(self, Item):
		return self.__dict__[Item]

        def Get(self, name):
                path = name.split('.')
		
		if path[0] in self:
                	node = self[path[0]]

                	if isinstance(node, Node) and len(path) > 1:
                        	return node.Get('.'.join(path[1:]))

                	else:
                        	return node

		return None

        def Set(self, name, value):
                path = name.split('.')

		if len(path) > 1:

			if not (path[0] in self and isinstance(self[path[0]], Node)):
				self[path[0]] = Node()						
			
			self[path[0]].Set('.'.join(path[1:]), value)
		
		else:
			if value == None:
				del self[path[0]]
			else:
				self[path[0]] = value

	def Ensure(self, name, default=None):
		if name not in self:
			if default == None:
				return self.New(name)
		
			else:
				self[name] = default
				
				return default
		
		return self[name]

	def New(self, name):
		new = Node()
		self[name] = new
		return new
		
	def __delitem__(self, Item):
		del self.__dict__[Item]

	def __len__(self):
		return len(self.__dict__)	

	def copy(self):
		new = Node()
		new.__dict__ = self.__dict__.copy()

		return new

        def Dict(self):
                toReturn = {}

                for item, value in self.iteritems():
                        if isinstance(value, Node):
                                toReturn[item] = value.Dict()

                        else:
                                toReturn[item] = value

                return toReturn
	
	def __add__(self, node):
		new = self.copy()

		if isinstance(node, Node):
			for item, value in node.iteritems():
				new[item] = value

		return new

	def __iadd__(self, node):
		if isinstance(node, Node):
			for item,value in node.iteritems():
				self[item] = value
