import re
import math
import tokenize
import StringIO

class SymbolBase:
	NAME = None

	def nud(self, parser):
		raise SyntaxError("Syntax error %s" % self.NAME)

	def led(self, parser, LHS):
		raise SyntaxError("Unknown operator %s" % self.NAME)

SymbolTable = {}

FuncTable = {
	"sin" : math.sin,
	"cos" : math.cos,
	"tan" : math.tan
}

def DefineSymbol(name, bp=0):
	try:
		sym = SymbolTable[name]

	except:
		class sym(SymbolBase):
			pass

		sym.NAME = name
		sym.lbp = bp

		sym.__name__ = "Symbol-" + name

		SymbolTable[name] = sym

	else:
		sym.lbp = max(bp, sym.lbp)

	return sym

def DefineConstant(name, value, bp=0):
	def nud(self, parser):
		return value

	DefineSymbol(name, bp).nud = nud

def OpAddLED(self, parser, LHS):
	return LHS + parser.Expr(self.lbp)
def OpSubLED(self, parser, LHS):
	return LHS - parser.Expr(self.lbp)
def OpMulLED(self, parser, LHS):
	return LHS * parser.Expr(self.lbp)
def OpDivLED(self, parser, LHS):
	return LHS / parser.Expr(self.lbp)

def OpPowLED(self, parser, LHS):
	return LHS ** parser.Expr(self.lbp - 1)

def OpAddNUD(self, parser):
	return +parser.Expr(self.lbp)
def OpSubNUD(self, parser):
	return -parser.Expr(self.lbp)

def OpAndLED(self, parser, LHS):
	RHS = parser.Expr(self.lbp) # Force jython not to optimize the op
	return LHS and RHS
def OpOrLED(self, parser, LHS):
	RHS = parser.Expr(self.lbp)
	return LHS or RHS
def OpNotNUD(self, parser):
	return not parser.Expr(self.lbp)

def OpEqualLED(self, parser, LHS):
	return LHS == parser.Expr(self.lbp)
def OpNEqualLED(self, parser, LHS):
	return LHS != parser.Expr(self.lbp)

def LiteralNUD(self, parser):
	return self.value

def NameNUD(self, parser):
	func = FuncTable.get(self.value)

	if func == None:
		raise SyntaxError("Unknown function %s" % self.value)

	args = []

	parser.Advance("(")

	if parser.currToken.NAME != ")":
		while True:
			args.append(parser.Expr())

			if parser.currToken.NAME != ",":
				break

			parser.Advance(",")

	parser.Advance(")")

	try:
		return func(*args)
	except Exception, E:
		raise SyntaxError(str(E))	

def ParenthNUD(self, parser):
	expr = parser.Expr()
	parser.Advance(")")
	return expr

DefineSymbol("LITERAL").nud = LiteralNUD
DefineSymbol("NAME").nud = NameNUD
DefineSymbol("+", 10).led = OpAddLED
DefineSymbol("-", 10).led = OpSubLED
DefineSymbol("*", 20).led = OpMulLED
DefineSymbol("/", 20).led = OpDivLED
DefineSymbol("^", 30).led = OpPowLED
DefineSymbol("+").nud = OpAddNUD
DefineSymbol("-").nud = OpSubNUD
DefineSymbol("(").nud = ParenthNUD
DefineSymbol(")")
DefineSymbol(",")
DefineSymbol("and", 50).led = OpAndLED
DefineSymbol("or", 50).led = OpOrLED
DefineSymbol("not", 60).nud = OpNotNUD
DefineSymbol("==", 40).led = OpEqualLED
DefineSymbol("!=", 40).led = OpNEqualLED
DefineSymbol("END")

DefineConstant("PI", math.pi)
DefineConstant("E",  math.e)

DefineConstant("True", True)
DefineConstant("False", False)

class Parser:
	def Expr(self, rbp=0):
		token          = self.currToken
		self.currToken = self.NextToken()

		result = token.nud(self)

		while rbp < self.currToken.lbp:
			token          = self.currToken
			self.currToken = self.NextToken()

			result = token.led(self, result)

		return result

	def Advance(self, name):
		if name and name != self.currToken.NAME:
			raise SyntaxError("Expected %s" % name)

		self.currToken = self.NextToken()			

	def Tokenize(self, expr):
		for token in tokenize.generate_tokens(StringIO.StringIO(expr).next):
			if token[0] == tokenize.ENDMARKER:
				break

			elif token[0] == tokenize.NUMBER:
				symbol = SymbolTable["LITERAL"]

				tok = symbol()

				tok.value = float(token[1])

				yield tok

			else:
				symbol = SymbolTable.get(token[1])

				if symbol != None:
					tok = symbol()

				elif token[0] == tokenize.NAME:
					symbol = SymbolTable["NAME"]

					tok = symbol()

					tok.value = token[1]

				else:
					raise SyntaxError("Unknown operator " + str(token[1]))

				yield tok

		symbol = SymbolTable["END"]

		yield symbol()

	def NextToken(self):
		try:
			return self.NextTokenRaw()
		except:
			raise SyntaxError("Unexpected end of input")

	def Parse(self, expr):
		self.NextTokenRaw = self.Tokenize(expr).next

		self.currToken = self.NextToken()

		return self.Expr()

@hook.command("calc", usage="Usage: /calc <expression>")
def OnCommandCalc(sender, args):
	if not args:
		return False

	parser = Parser()

	expr = ' '.join(args)

	try:
		result = parser.Parse(expr)
	except SyntaxError, E:
		sender.sendMessage("Syntax error: " + str(E))
		return True

	sender.sendMessage(expr + " -> " + str(result))

	return True
