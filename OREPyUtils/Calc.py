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
FuncTable = {}

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

def DefineFunction(name, func, bp=0):
	def nud(self, parser):
		return parser.Expr(self.lbp)

	DefineSymbol(name, bp).nud = nud

	FuncTable[name] = func

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
def LiteralNUD(self, parser):
	return self.value
def ParenthNUD(self, parser):
	expr = parser.Expr()
	parser.Advance(")")
	return expr

def FunctionLED(self, parser, LHS):
	args = []

	if parser.currToken.NAME != ")":
		while True:
			args.append(parser.Expr())

			if parser.currToken.NAME != ",":
				break

			parser.Advance(",")

	parser.Advance(")")

	func = FuncTable.get(LHS)

	if func == None:
		raise SyntaxError("Unknown function %s" % LHS)

	return func(*args)

DefineSymbol("LITERAL").nud = LiteralNUD
DefineSymbol("+", 10).led = OpAddLED
DefineSymbol("-", 10).led = OpSubLED
DefineSymbol("*", 20).led = OpMulLED
DefineSymbol("/", 20).led = OpDivLED
DefineSymbol("+").nud = OpAddNUD
DefineSymbol("-").nud = OpSubNUD
DefineSymbol("**", 30).led = OpPowLED
DefineSymbol("(").nud = ParenthNUD
DefineSymbol("(").led = FunctionLED
DefineSymbol(")")
DefineSymbol(",")
DefineSymbol("END")

DefineConstant("PI", math.pi)
DefineConstant("E",  math.e)

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

				if symbol == None:
					raise SyntaxError("Unknown operator " + str(token[1]))

				yield symbol()

		symbol = SymbolTable["END"]

		yield symbol()

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
