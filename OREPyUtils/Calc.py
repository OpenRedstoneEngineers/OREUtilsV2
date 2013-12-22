# Math expr parser

import re

class TokenLiteral:
	def __init__(self, value):
		self.value = int(value)

	def nud(self, parser):
		return self.value

class TokenEnd:
	lbp = 0

class TokenOpAdd:
	lbp = 10
	def led(self, parser, LHS):
		return LHS + parser.Expr(10)

class TokenOpSub:
	lbp = 10
	def led(self, parser, LHS):
		return LHS - parser.Expr(10) 

class TokenOpMul:
	lbp = 20
	def led(self, parser, LHS):
		return LHS * parser.Expr(20)

class TokenOpDiv:
	lbp = 20
	def led(self, parser, LHS):
		return LHS / parser.Expr(20)

class Parser:
	REGEX = re.compile("\s*(?:(\d+)|(.))")

	def Expr(self, rbp=0):
		token          = self.currToken
		self.currToken = self.NextToken()

		result = token.nud(self)

		while rbp < self.currToken.lbp:
			token          = self.currToken
			self.currToken = self.NextToken()

			result = token.led(self, result)

		return result			

	def Tokenize(self, expr):
		for number, operator in self.REGEX.findall(expr):
			if number:
				yield TokenLiteral(number)

			elif operator == "+":
				yield TokenOpAdd()
			elif operator == "-":
				yield TokenOpSub()
			elif operator == "*":
				yield TokenOpMul()
			elif operator == "/":
				yield TokenOpDiv()
			else:
				raise SyntaxError("Unknown operator " + str(operator))

		yield TokenEnd()

	def Parse(self, expr):
		self.NextToken = self.Tokenize(expr).next

		self.currToken = self.NextToken()

		return self.Expr()

@hook.command("ecalc")
def OnCommandCalc(sender, args):
	parser = Parser()

	expr = ' '.join(args)

	try:
		result = parser.Parse(expr)
	except SyntaxError, E:
		sender.sendMessage("Syntax error: " + str(E))
		return True

	sender.sendMessage(expr + " = " + str(result))

	return True
