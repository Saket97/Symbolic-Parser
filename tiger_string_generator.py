from random import *
from parser_string_generator import parser_main
output = []
pos = 0
Threshold = 40

def error():
	assert("Unreachable")

def consume(x):
	global pos
	if (x == "eps"):
		pass
	else:
		output[pos] = x
		output.append("~")
		pos = pos + 1
		assert(pos < 10000)
	#print "consumed ",x

def choose(d, L1, L2):
	x = ""
	if d < Threshold or len(L2) == 0:
		x = choice(L1 + L2)
	else:
		x = choice(L2)
	return x


def Prog(d):
	global pos
	#print "Prog called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "string"  ,"for"  ,"nil"  ,"("  ,"-"  ,"break"  ,"while"  ,"let"  ,"integer"  ,"id"  ,"if" ],[])
		#print output[pos] 
		output[pos] = "let"
	if output[pos] == "string" or output[pos] == "for" or output[pos] == "nil" or output[pos] == "(" or output[pos] == "-" or output[pos] == "break" or output[pos] == "while" or output[pos] == "let" or output[pos] == "integer" or output[pos] == "id" or output[pos] == "if" :
		Exp(d+1)
	else:
		error()

def Exp(d):
	global pos
	#print "Exp called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "string"  ,"for"  ,"nil"  ,"("  ,"-"  ,"break"  ,"while"  ,"let"  ,"integer"  ,"id"  ,"if" ],[])
		#print output[pos] 
	if output[pos] == "string" or output[pos] == "for" or output[pos] == "nil" or output[pos] == "(" or output[pos] == "-" or output[pos] == "break" or output[pos] == "while" or output[pos] == "let" or output[pos] == "integer" or output[pos] == "id" or output[pos] == "if" :
		ExpOR(d+1)
		ExpORPr(d+1)
	else:
		error()

def ExpOR(d):
	global pos
	#print "ExpOR called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "string"  ,"for"  ,"nil"  ,"("  ,"-"  ,"break"  ,"while"  ,"let"  ,"integer"  ,"id"  ,"if" ],[])
		#print output[pos] 
	if output[pos] == "string" or output[pos] == "for" or output[pos] == "nil" or output[pos] == "(" or output[pos] == "-" or output[pos] == "break" or output[pos] == "while" or output[pos] == "let" or output[pos] == "integer" or output[pos] == "id" or output[pos] == "if" :
		ExpAND(d+1)
		ExpANDPr(d+1)
	else:
		error()

def ExpORPr(d):
	global pos
	#print "ExpORPr called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "|" ],[ ">="  ,"then"  ,"<="  ,"in"  ,"!="  ,"end"  ,"&"  ,")"  ,"+"  ,"*"  ,"-"  ,","  ,"/"  ,"to"  ,"var"  ,";"  ,"type"  ,"<"  ,">"  ,"function"  ,"do"  ,"else"  ,"]"  ,"dol"  ,"="  ,"}" ])
		#print output[pos] 
	if output[pos] == "|" :
		consume("|")
		Exp(d+1)
	elif output[pos] == ">=" or output[pos] == "then" or output[pos] == "<=" or output[pos] == "in" or output[pos] == "!=" or output[pos] == "end" or output[pos] == "&" or output[pos] == ")" or output[pos] == "+" or output[pos] == "*" or output[pos] == "-" or output[pos] == "," or output[pos] == "/" or output[pos] == "to" or output[pos] == "var" or output[pos] == ";" or output[pos] == "type" or output[pos] == "<" or output[pos] == ">" or output[pos] == "function" or output[pos] == "do" or output[pos] == "else" or output[pos] == "]" or output[pos] == "dol" or output[pos] == "=" or output[pos] == "}" :
		consume("eps")
	else:
		error()

def ExpANDPr(d):
	global pos
	#print "ExpANDPr called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "&" ],[ ">="  ,"then"  ,"<="  ,"in"  ,"!="  ,"end"  ,")"  ,"+"  ,"*"  ,"-"  ,","  ,"/"  ,"to"  ,"var"  ,";"  ,"type"  ,"<"  ,">"  ,"function"  ,"do"  ,"else"  ,"]"  ,"dol"  ,"="  ,"}"  ,"|" ])
		#print output[pos] 
	if output[pos] == "&" :
		consume("&")
		ExpOR(d+1)
	elif output[pos] == ">=" or output[pos] == "then" or output[pos] == "<=" or output[pos] == "in" or output[pos] == "!=" or output[pos] == "end" or output[pos] == ")" or output[pos] == "+" or output[pos] == "*" or output[pos] == "-" or output[pos] == "," or output[pos] == "/" or output[pos] == "to" or output[pos] == "var" or output[pos] == ";" or output[pos] == "type" or output[pos] == "<" or output[pos] == ">" or output[pos] == "function" or output[pos] == "do" or output[pos] == "else" or output[pos] == "]" or output[pos] == "dol" or output[pos] == "=" or output[pos] == "}" or output[pos] == "|" :
		consume("eps")
	else:
		error()

def ExpAND(d):
	global pos
	#print "ExpAND called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "string"  ,"for"  ,"nil"  ,"("  ,"-"  ,"break"  ,"while"  ,"let"  ,"integer"  ,"id"  ,"if" ],[])
		#print output[pos] 
	if output[pos] == "string" or output[pos] == "for" or output[pos] == "nil" or output[pos] == "(" or output[pos] == "-" or output[pos] == "break" or output[pos] == "while" or output[pos] == "let" or output[pos] == "integer" or output[pos] == "id" or output[pos] == "if" :
		ArithExp(d+1)
		RelationExp(d+1)
	else:
		error()

def ArithExp(d):
	global pos
	#print "ArithExp called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "string"  ,"for"  ,"nil"  ,"("  ,"-"  ,"break"  ,"while"  ,"let"  ,"integer"  ,"id"  ,"if" ],[])
		#print output[pos] 
	if output[pos] == "string" or output[pos] == "for" or output[pos] == "nil" or output[pos] == "(" or output[pos] == "-" or output[pos] == "break" or output[pos] == "while" or output[pos] == "let" or output[pos] == "integer" or output[pos] == "id" or output[pos] == "if" :
		Term(d+1)
		TermPr(d+1)
	else:
		error()

def RelationExp(d):
	global pos
	#print "RelationExp called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ ">="  ,"<="  ,"!="  ,"<"  ,">"  ,"=" ],[ "then"  ,"in"  ,"end"  ,"&"  ,")"  ,"+"  ,"*"  ,"-"  ,","  ,"/"  ,"to"  ,"var"  ,";"  ,"type"  ,"function"  ,"do"  ,"else"  ,"]"  ,"dol"  ,"}"  ,"|" ])
		#print output[pos] 
	if output[pos] == ">=" or output[pos] == "<=" or output[pos] == "!=" or output[pos] == "<" or output[pos] == ">" or output[pos] == "=" :
		RelationOp(d+1)
		ArithExp(d+1)
	elif output[pos] == "then" or output[pos] == "in" or output[pos] == "end" or output[pos] == "&" or output[pos] == ")" or output[pos] == "+" or output[pos] == "*" or output[pos] == "-" or output[pos] == "," or output[pos] == "/" or output[pos] == "to" or output[pos] == "var" or output[pos] == ";" or output[pos] == "type" or output[pos] == "function" or output[pos] == "do" or output[pos] == "else" or output[pos] == "]" or output[pos] == "dol" or output[pos] == "}" or output[pos] == "|" :
		consume("eps")
	else:
		error()

def Term(d):
	global pos
	#print "Term called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "string"  ,"for"  ,"nil"  ,"("  ,"-"  ,"break"  ,"while"  ,"let"  ,"integer"  ,"id"  ,"if" ],[])
		#print output[pos] 
	if output[pos] == "string" or output[pos] == "for" or output[pos] == "nil" or output[pos] == "(" or output[pos] == "-" or output[pos] == "break" or output[pos] == "while" or output[pos] == "let" or output[pos] == "integer" or output[pos] == "id" or output[pos] == "if" :
		Factor(d+1)
		FactorPr(d+1)
	else:
		error()

def TermPr(d):
	global pos
	#print "TermPr called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "+"  ,"-" ],[ ">="  ,"then"  ,"<="  ,"in"  ,"!="  ,"end"  ,"&"  ,")"  ,"*"  ,","  ,"/"  ,"to"  ,"var"  ,";"  ,"type"  ,"<"  ,">"  ,"function"  ,"do"  ,"else"  ,"]"  ,"dol"  ,"="  ,"}"  ,"|" ])
		#print output[pos] 
	if output[pos] == "+" :
		consume("+")
		Term(d+1)
		TermPr(d+1)
	elif output[pos] == "-" :
		consume("-")
		Term(d+1)
		TermPr(d+1)
	elif output[pos] == ">=" or output[pos] == "then" or output[pos] == "<=" or output[pos] == "in" or output[pos] == "!=" or output[pos] == "end" or output[pos] == "&" or output[pos] == ")" or output[pos] == "*" or output[pos] == "," or output[pos] == "/" or output[pos] == "to" or output[pos] == "var" or output[pos] == ";" or output[pos] == "type" or output[pos] == "<" or output[pos] == ">" or output[pos] == "function" or output[pos] == "do" or output[pos] == "else" or output[pos] == "]" or output[pos] == "dol" or output[pos] == "=" or output[pos] == "}" or output[pos] == "|" :
		consume("eps")
	else:
		error()

def FactorPr(d):
	global pos
	#print "FactorPr called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "*"  ,"/" ],[ ">="  ,"then"  ,"<="  ,"in"  ,"!="  ,"end"  ,"&"  ,")"  ,"+"  ,"-"  ,","  ,"to"  ,"var"  ,";"  ,"type"  ,"<"  ,">"  ,"function"  ,"do"  ,"else"  ,"]"  ,"dol"  ,"="  ,"}"  ,"|" ])
		#print output[pos] 
	if output[pos] == "*" :
		consume("*")
		Factor(d+1)
		FactorPr(d+1)
	elif output[pos] == "/" :
		consume("/")
		Factor(d+1)
		FactorPr(d+1)
	elif output[pos] == ">=" or output[pos] == "then" or output[pos] == "<=" or output[pos] == "in" or output[pos] == "!=" or output[pos] == "end" or output[pos] == "&" or output[pos] == ")" or output[pos] == "+" or output[pos] == "-" or output[pos] == "," or output[pos] == "to" or output[pos] == "var" or output[pos] == ";" or output[pos] == "type" or output[pos] == "<" or output[pos] == ">" or output[pos] == "function" or output[pos] == "do" or output[pos] == "else" or output[pos] == "]" or output[pos] == "dol" or output[pos] == "=" or output[pos] == "}" or output[pos] == "|" :
		consume("eps")
	else:
		error()

def Factor(d):
	global pos
	#print "Factor called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "for"  ,"("  ,"-"  ,"while"  ,"let"  ,"id"  ,"if" ],[ "string"  ,"nil"  ,"break"  ,"integer" ])
		#print output[pos] 
	if output[pos] == "nil" :
		consume("nil")
	elif output[pos] == "integer" :
		consume("integer")
	elif output[pos] == "string" :
		consume("string")
	elif output[pos] == "(" :
		consume("(")
		ExpList(d+1)
		consume(")")
	elif output[pos] == "-" :
		UnaryOp(d+1)
		Exp(d+1)
	elif output[pos] == "if" :
		consume("if")
		Exp(d+1)
		consume("then")
		Exp(d+1)
		IF_extra(d+1)
	elif output[pos] == "while" :
		consume("while")
		Exp(d+1)
		consume("do")
		Exp(d+1)
	elif output[pos] == "for" :
		consume("for")
		consume("id")
		consume(":=")
		Exp(d+1)
		consume("to")
		Exp(d+1)
		consume("do")
		Exp(d+1)
	elif output[pos] == "break" :
		consume("break")
	elif output[pos] == "let" :
		consume("let")
		DecList(d+1)
		consume("in")
		ExpList(d+1)
		consume("end")
	elif output[pos] == "id" :
		LValue(d+1)
	else:
		error()

def IF_extra(d):
	global pos
	#print "IF_extra called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "else" ],[ ">="  ,"then"  ,"<="  ,"in"  ,"!="  ,"end"  ,"&"  ,")"  ,"+"  ,"*"  ,"-"  ,","  ,"/"  ,"to"  ,"var"  ,";"  ,"type"  ,"<"  ,">"  ,"function"  ,"do"  ,"]"  ,"dol"  ,"="  ,"}"  ,"|" ])
		#print output[pos] 
	if output[pos] == "else" :
		consume("else")
		Exp(d+1)
	elif output[pos] == ">=" or output[pos] == "then" or output[pos] == "<=" or output[pos] == "in" or output[pos] == "!=" or output[pos] == "end" or output[pos] == "&" or output[pos] == ")" or output[pos] == "+" or output[pos] == "*" or output[pos] == "-" or output[pos] == "," or output[pos] == "/" or output[pos] == "to" or output[pos] == "var" or output[pos] == ";" or output[pos] == "type" or output[pos] == "<" or output[pos] == ">" or output[pos] == "function" or output[pos] == "do" or output[pos] == "]" or output[pos] == "dol" or output[pos] == "=" or output[pos] == "}" or output[pos] == "|" :
		consume("eps")
	else:
		error()

def DecList(d):
	global pos
	#print "DecList called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "var"  ,"function"  ,"type"  ,"in" ],[])
		#print output[pos] 
	if output[pos] == "var" or output[pos] == "function" or output[pos] == "type" or output[pos] == "in" :
		DL_extra(d+1)
	else:
		error()

def DL_extra(d):
	global pos
	#print "DL_extra called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "var"  ,"function"  ,"type" ],[ "in" ])
		#print output[pos] 
	if output[pos] == "var" or output[pos] == "function" or output[pos] == "type" :
		Dec(d+1)
		DL_extra(d+1)
	elif output[pos] == "in" :
		consume("eps")
	else:
		error()

def Dec(d):
	global pos
	#print "Dec called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "var"  ,"function"  ,"type" ],[])
		#print output[pos] 
	if output[pos] == "type" :
		TyDec(d+1)
	elif output[pos] == "var" :
		VarDec(d+1)
	elif output[pos] == "function" :
		FunDec(d+1)
	else:
		error()

def TyDec(d):
	global pos
	#print "TyDec called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "type" ],[])
		#print output[pos] 
	if output[pos] == "type" :
		consume("type")
		TypeId(d+1)
		consume("=")
		Ty(d+1)
	else:
		error()

def Ty(d):
	global pos
	#print "Ty called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "integer"  ,"array"  ,"{"  ,"string"  ,"id" ],[])
		#print output[pos] 
	if output[pos] == "array" :
		consume("array")
		consume("of")
		TypeId(d+1)
	elif output[pos] == "integer" or output[pos] == "string" or output[pos] == "id" :
		TypeId(d+1)
	elif output[pos] == "{" :
		consume("{")
		FieldList(d+1)
		consume("}")
	else:
		error()

def FieldList(d):
	global pos
	#print "FieldList called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "id" ],[ ")"  ,"}" ])
		#print output[pos] 
	if output[pos] == ")" or output[pos] == "}" :
		consume("eps")
	elif output[pos] == "id" :
		consume("id")
		consume(":")
		TypeId(d+1)
		FL_extra(d+1)
	else:
		error()

def FL_extra(d):
	global pos
	#print "FL_extra called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "," ],[ ")"  ,"}" ])
		#print output[pos] 
	if output[pos] == "," :
		consume(",")
		consume("id")
		consume(":")
		TypeId(d+1)
		FL_extra(d+1)
	elif output[pos] == ")" or output[pos] == "}" :
		consume("eps")
	else:
		error()

def FieldExpList(d):
	global pos
	#print "FieldExpList called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "id" ],[])
		#print output[pos] 
	if output[pos] == "id" :
		consume("id")
		consume("=")
		Exp(d+1)
		FEL_extra(d+1)
	else:
		error()

def FEL_extra(d):
	global pos
	#print "FEL_extra called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "," ],[])
		#print output[pos] 
	if output[pos] == "," :
		consume(",")
		consume("id")
		consume("=")
		Exp(d+1)
		FEL_extra(d+1)
	else:
		error()

def TypeId(d):
	global pos
	#print "TypeId called..."
	if output[pos] == "~":
		output[pos] = choose(d, [],[ "integer"  ,"string"  ,"id" ])
		#print output[pos] 
	if output[pos] == "id" :
		consume("id")
	elif output[pos] == "integer" :
		consume("integer")
	elif output[pos] == "string" :
		consume("string")
	else:
		error()

def VD_extra(d):
	global pos
	#print "VD_extra called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ ":" ],[ ":="  ,"=" ])
		#print output[pos] 
	if output[pos] == ":=" or output[pos] == "=" :
		consume("eps")
	elif output[pos] == ":" :
		consume(":")
		TypeId(d+1)
	else:
		error()

def VarDec(d):
	global pos
	#print "VarDec called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "var" ],[])
		#print output[pos] 
	if output[pos] == "var" :
		consume("var")
		consume("id")
		VD_extra(d+1)
		consume(":=")
		Exp(d+1)
	else:
		error()

def FunDec(d):
	global pos
	#print "FunDec called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "function" ],[])
		#print output[pos] 
	if output[pos] == "function" :
		consume("function")
		consume("id")
		consume("(")
		FieldList(d+1)
		consume(")")
		VD_extra(d+1)
		consume("=")
		Exp(d+1)
	else:
		error()

def LValue(d):
	global pos
	#print "LValue called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "id" ],[])
		#print output[pos] 
	if output[pos] == "id" :
		consume("id")
		LD_extra(d+1)
	else:
		error()

def LD_extra(d):
	global pos
	#print "LD_extra called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ ">="  ,"then"  ,"<="  ,":="  ,"in"  ,"!="  ,"end"  ,"&"  ,")"  ,"("  ,"+"  ,"*"  ,"-"  ,","  ,"/"  ,"."  ,"to"  ,"var"  ,";"  ,"type"  ,"<"  ,">"  ,"function"  ,"do"  ,"else"  ,"["  ,"]"  ,"dol"  ,"="  ,"{"  ,"}"  ,"|" ],[])
		#print output[pos] 
	if output[pos] == ">=" or output[pos] == "then" or output[pos] == "<=" or output[pos] == ":=" or output[pos] == "in" or output[pos] == "!=" or output[pos] == "end" or output[pos] == "&" or output[pos] == ")" or output[pos] == "+" or output[pos] == "*" or output[pos] == "-" or output[pos] == "," or output[pos] == "/" or output[pos] == "." or output[pos] == "to" or output[pos] == "var" or output[pos] == ";" or output[pos] == "type" or output[pos] == "<" or output[pos] == ">" or output[pos] == "function" or output[pos] == "do" or output[pos] == "else" or output[pos] == "]" or output[pos] == "dol" or output[pos] == "=" or output[pos] == "}" or output[pos] == "|" :
		FunctionRecordArrayPr(d+1)
	elif output[pos] == "(" or output[pos] == "[" or output[pos] == "{" :
		FunctionRecordArray(d+1)
	else:
		error()

def FunctionRecordArray(d):
	global pos
	#print "FunctionRecordArray called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "("  ,"["  ,"{" ],[])
		#print output[pos] 
	if output[pos] == "[" :
		consume("[")
		Exp(d+1)
		consume("]")
		FRA_extra1(d+1)
	elif output[pos] == "(" :
		consume("(")
		ArgList(d+1)
		consume(")")
	elif output[pos] == "{" :
		consume("{")
		consume("id")
		consume("=")
		Exp(d+1)
		FRA_extra(d+1)
		consume("}")
	else:
		error()

def FRA_extra(d):
	global pos
	#print "FRA_extra called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "," ],[ "}" ])
		#print output[pos] 
	if output[pos] == "," :
		consume(",")
		consume("id")
		consume("=")
		Exp(d+1)
		FRA_extra(d+1)
	elif output[pos] == "}" :
		consume("eps")
	else:
		error()

def FRA_extra1(d):
	global pos
	#print "FRA_extra1 called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ ">="  ,"then"  ,"<="  ,":="  ,"in"  ,"!="  ,"end"  ,"&"  ,")"  ,"+"  ,"*"  ,"-"  ,","  ,"/"  ,"."  ,"to"  ,"var"  ,";"  ,"type"  ,"<"  ,">"  ,"function"  ,"do"  ,"else"  ,"["  ,"]"  ,"dol"  ,"="  ,"of"  ,"}"  ,"|" ],[])
		#print output[pos] 
	if output[pos] == ">=" or output[pos] == "then" or output[pos] == "<=" or output[pos] == ":=" or output[pos] == "in" or output[pos] == "!=" or output[pos] == "end" or output[pos] == "&" or output[pos] == ")" or output[pos] == "+" or output[pos] == "*" or output[pos] == "-" or output[pos] == "," or output[pos] == "/" or output[pos] == "." or output[pos] == "to" or output[pos] == "var" or output[pos] == ";" or output[pos] == "type" or output[pos] == "<" or output[pos] == ">" or output[pos] == "function" or output[pos] == "do" or output[pos] == "else" or output[pos] == "[" or output[pos] == "]" or output[pos] == "dol" or output[pos] == "=" or output[pos] == "}" or output[pos] == "|" :
		FunctionRecordArrayPr(d+1)
	elif output[pos] == "of" :
		consume("of")
		Exp(d+1)
	else:
		error()

def FRAP_extra1(d):
	global pos
	#print "FRAP_extra1 called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ ":=" ],[ ">="  ,"then"  ,"<="  ,"in"  ,"!="  ,"end"  ,"&"  ,")"  ,"+"  ,"*"  ,"-"  ,","  ,"/"  ,"to"  ,"var"  ,";"  ,"type"  ,"<"  ,">"  ,"function"  ,"do"  ,"else"  ,"]"  ,"dol"  ,"="  ,"}"  ,"|" ])
		#print output[pos] 
	if output[pos] == ":=" :
		consume(":=")
		Exp(d+1)
	elif output[pos] == ">=" or output[pos] == "then" or output[pos] == "<=" or output[pos] == "in" or output[pos] == "!=" or output[pos] == "end" or output[pos] == "&" or output[pos] == ")" or output[pos] == "+" or output[pos] == "*" or output[pos] == "-" or output[pos] == "," or output[pos] == "/" or output[pos] == "to" or output[pos] == "var" or output[pos] == ";" or output[pos] == "type" or output[pos] == "<" or output[pos] == ">" or output[pos] == "function" or output[pos] == "do" or output[pos] == "else" or output[pos] == "]" or output[pos] == "dol" or output[pos] == "=" or output[pos] == "}" or output[pos] == "|" :
		consume("eps")
	else:
		error()

def FunctionRecordArrayPr(d):
	global pos
	#print "FunctionRecordArrayPr called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ ">="  ,"then"  ,"<="  ,":="  ,"in"  ,"!="  ,"end"  ,"&"  ,")"  ,"+"  ,"*"  ,"-"  ,","  ,"/"  ,"."  ,"to"  ,"var"  ,";"  ,"type"  ,"<"  ,">"  ,"function"  ,"do"  ,"else"  ,"["  ,"]"  ,"dol"  ,"="  ,"}"  ,"|" ],[])
		#print output[pos] 
	if output[pos] == ">=" or output[pos] == "then" or output[pos] == "<=" or output[pos] == ":=" or output[pos] == "in" or output[pos] == "!=" or output[pos] == "end" or output[pos] == "&" or output[pos] == ")" or output[pos] == "+" or output[pos] == "*" or output[pos] == "-" or output[pos] == "," or output[pos] == "/" or output[pos] == "." or output[pos] == "to" or output[pos] == "var" or output[pos] == ";" or output[pos] == "type" or output[pos] == "<" or output[pos] == ">" or output[pos] == "function" or output[pos] == "do" or output[pos] == "else" or output[pos] == "[" or output[pos] == "]" or output[pos] == "dol" or output[pos] == "=" or output[pos] == "}" or output[pos] == "|" :
		FRAP_extra(d+1)
		FRAP_extra1(d+1)
	else:
		error()

def FRAP_extra(d):
	global pos
	#print "FRAP_extra called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "."  ,"[" ],[ ">="  ,"then"  ,"<="  ,":="  ,"in"  ,"!="  ,"end"  ,"&"  ,")"  ,"+"  ,"*"  ,"-"  ,","  ,"/"  ,"to"  ,"var"  ,";"  ,"type"  ,"<"  ,">"  ,"function"  ,"do"  ,"else"  ,"]"  ,"dol"  ,"="  ,"}"  ,"|" ])
		#print output[pos] 
	if output[pos] == ">=" or output[pos] == "then" or output[pos] == "<=" or output[pos] == ":=" or output[pos] == "in" or output[pos] == "!=" or output[pos] == "end" or output[pos] == "&" or output[pos] == ")" or output[pos] == "+" or output[pos] == "*" or output[pos] == "-" or output[pos] == "," or output[pos] == "/" or output[pos] == "to" or output[pos] == "var" or output[pos] == ";" or output[pos] == "type" or output[pos] == "<" or output[pos] == ">" or output[pos] == "function" or output[pos] == "do" or output[pos] == "else" or output[pos] == "]" or output[pos] == "dol" or output[pos] == "=" or output[pos] == "}" or output[pos] == "|" :
		consume("eps")
	elif output[pos] == "." :
		consume(".")
		consume("id")
		FRAP_extra(d+1)
	elif output[pos] == "[" :
		consume("[")
		Exp(d+1)
		consume("]")
		FRAP_extra(d+1)
	else:
		error()

def ExpList(d):
	global pos
	#print "ExpList called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "nil"  ,"string"  ,"for"  ,"("  ,"-"  ,"break"  ,"while"  ,"let"  ,"integer"  ,"id"  ,"if" ],[ "end"  ,")" ])
		#print output[pos] 
	if output[pos] == "end" or output[pos] == ")" :
		consume("eps")
	elif output[pos] == "nil" or output[pos] == "string" or output[pos] == "for" or output[pos] == "(" or output[pos] == "-" or output[pos] == "break" or output[pos] == "while" or output[pos] == "let" or output[pos] == "integer" or output[pos] == "id" or output[pos] == "if" :
		Exp(d+1)
		EL_extra(d+1)
	else:
		error()

def EL_extra(d):
	global pos
	#print "EL_extra called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ ";" ],[ ")"  ,"end" ])
		#print output[pos] 
	if output[pos] == ")" or output[pos] == "end" :
		consume("eps")
	elif output[pos] == ";" :
		consume(";")
		Exp(d+1)
		EL_extra(d+1)
	else:
		error()

def ArgList(d):
	global pos
	#print "ArgList called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "nil"  ,"string"  ,"for"  ,"("  ,"-"  ,"break"  ,"while"  ,"let"  ,"integer"  ,"id"  ,"if" ],[ ")" ])
		#print output[pos] 
	if output[pos] == ")" :
		consume("eps")
	elif output[pos] == "nil" or output[pos] == "string" or output[pos] == "for" or output[pos] == "(" or output[pos] == "-" or output[pos] == "break" or output[pos] == "while" or output[pos] == "let" or output[pos] == "integer" or output[pos] == "id" or output[pos] == "if" :
		Exp(d+1)
		AL_extra(d+1)
	else:
		error()

def AL_extra(d):
	global pos
	#print "AL_extra called..."
	if output[pos] == "~":
		output[pos] = choose(d, [ "," ],[ ")" ])
		#print output[pos] 
	if output[pos] == ")" :
		consume("eps")
	elif output[pos] == "," :
		consume(",")
		Exp(d+1)
		AL_extra(d+1)
	else:
		error()

def UnaryOp(d):
	global pos
	#print "UnaryOp called..."
	if output[pos] == "~":
		output[pos] = choose(d, [],[ "-" ])
		#print output[pos] 
	if output[pos] == "-" :
		consume("-")
	else:
		error()

def RelationOp(d):
	global pos
	#print "RelationOp called..."
	if output[pos] == "~":
		output[pos] = choose(d, [],[ ">="  ,"!="  ,"<="  ,"="  ,"<"  ,">" ])
		#print output[pos] 
	if output[pos] == "=" :
		consume("=")
	elif output[pos] == "!=" :
		consume("!=")
	elif output[pos] == ">" :
		consume(">")
	elif output[pos] == "<" :
		consume("<")
	elif output[pos] == ">=" :
		consume(">=")
	elif output[pos] == "<=" :
		consume("<=")
	else:
		error()
output.append("~")
Prog(0)
output[len(output)-1] = "$" # this will be arbitrary token which should be the end of input when the parsing stack becomes empty (recursive call returns)
print "output:",output
#parser_main(output)