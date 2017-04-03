from random import *


# E -> T E1
# E1 -> +T E1 | ep
# T -> F T1
# T1 -> * F T1 | ep
# F -> ( E ) | id

output = []
pos = 0
Threshold = 5

def error():
	assert("Unreachable")

def choose(d, L1, L2):
	x = ""
	if d < Threshold or len(L2) == 0:
		x = choice(L1 + L2)
	else:
		x = choice(L2)
	return x

def consume(x):
	global pos
	if (x == "ep"):
		pass
	else:
		output[pos] = x
		output.append("~")
		pos = pos + 1
		assert(pos < 10000)

def E(d):
	global pos
	if output[pos] == "~":
		output[pos] = choose(d, ["id", "("], [])

	if (output[pos] == "id" or output[pos] == "("):
		T(d+1)
		E1(d+1)
	else:
		error()

def E1(d):
	global pos
	if output[pos] == "~":
		output[pos] = choose(d, ["+"], [")"])
#		output[pos] = choose(d, ["+"], [")", "$"])

	if (output[pos] == "+"):
		consume("+")
		T(d+1)
		E1(d+1)
	elif (output[pos] == ")" or output[pos] == "$"):
		consume("ep")
	else:
		error()

def T(d):
	global pos
	if output[pos] == "~":
		output[pos] = choose(d, ["id", "("], [])

	if (output[pos] == "id" or output[pos] == "("):
		F(d+1)
		T1(d+1)
	else:
		error()
	
def T1(d):
	global pos
	if output[pos] == "~":
		output[pos] = choose(d, ["*"], ["+", ")"])
#		output[pos] = choose(d, ["*"], ["+", ")", "$"])

	if output[pos] == "*":
		consume("*")
		F(d+1)
		T1(d+1)
	elif output[pos] == "+" or output[pos] == ")" or output[pos] == "$":
		consume("ep")
	else:
		error()

def F(d):
	global pos
	if output[pos] == "~":
		output[pos] = choose(d, ["("], ["id"])

	if output[pos] == "id":
		consume("id")
	elif output[pos] == "(":
		consume("(")
		E(d+1)
		consume(")")
	else:
		error()

output.append("~")
E(0)
output[len(output)-1] = "$" # this will be arbitrary token which should be the end of input when the parsing stack becomes empty (recursive call returns)
print output

