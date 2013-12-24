from Node import *

from ast import literal_eval as Eval

class YAMLBackend:
	def Load(self, node, x):
		self.LoadSection(node, x.split("\n"))
	
	def LoadSection(self, node, lines, indent=0):
		while lines:
			line = lines[0]

			strip = line.lstrip()
			
			newIndent = len(line) - len(strip)
			
			split = strip.split(':')
			key = split[0]
			
			if newIndent < indent:
				return
			
			del lines[0]

			if line.endswith(":"):
				node[key] = Node()
				self.LoadSection(node[key], lines, indent + 1)
			
			else:
				try:
					value = Eval(":".join(split[1:]))

				except:
					value = ":".join(split[1:])

				node[key] = value

	def Save(self, node, embed=0):
		toReturn = ['\n']

		for item, value in node.iteritems():
			if isinstance(value, Node):
				toReturn.append(("\t" * embed) + "'" + item + "': " + self.ToStr(value, embed + 1) + "\n")
			else:
				toReturn.append(("\t" * embed) + "'" + item + "': " + repr(value) + "\n")

		toReturn.append('\n')

		return ''.join(toReturn)
