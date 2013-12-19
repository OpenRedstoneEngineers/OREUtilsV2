from Node import *

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
