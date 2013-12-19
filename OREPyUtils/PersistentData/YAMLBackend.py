from Node import *

class YAMLBackend:
	def Load(self, node, x):
		pass
		# TODO..

	def Save(self, node, embed=0):
		toReturn = ['\n']

		for item, value in node.iteritems():
			if isinstance(value, Node):
				toReturn.append(("\t" * embed) + "'" + item + "': " + self.ToStr(value, embed + 1) + "\n")
			else:
				toReturn.append(("\t" * embed) + "'" + item + "': " + repr(value) + "\n")

		toReturn.append('\n')

		return ''.join(toReturn)
