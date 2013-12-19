from Node import *

from ast import literal_eval as Eval

class JSONBackend:
	def LoadDict(self, node, x):
		for item, value in x.iteritems():
			if isinstance(value, dict):
				node[item] = Node()

				self.LoadDict(node[item], value)		
			else:
				node[item] = value

	def Load(self, node, x):
		try:
			data = Eval(x)

		except:
			data = {}

		self.LoadDict(node, data)

	def Save(self, node, embed=0):
		toReturn = ["{\n"]

		for item, value in node.iteritems():
			if isinstance(value, Node):
				toReturn.append(("\t" * embed) + "'" + item + "' : " + self.Save(value, embed + 1) + ",\n")
			else:
				toReturn.append(("\t" * embed) + "'" + item + "' : " + repr(value) + ",\n")

		toReturn.append(("\t" * embed) + "}")


		return ''.join(toReturn)
