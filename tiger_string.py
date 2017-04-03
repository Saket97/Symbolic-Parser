from input_specs_tiger import *

def discover_non_tokens():
	non_terminals = []
	for rule in grammar:
		if rule[0] not in non_terminals:
			non_terminals.append(rule[0])
	return non_terminals

def discover_tokens():
	tokens = []
	for rule in grammar:
		for elt in rule:
			if elt in non_terminals:
				continue
			if elt in tokens:
				continue
			tokens.append(elt)
	return tokens

# tset is a dictionalry with key as terminal name and value as the rule number
def get_terminal_only_rules(nt, tset):
	rules = []
	# print "tset",tset
	for key in tset:
		#### check if the rule contains no non_terminals ########
		check = False
		for i in range(1,len(grammar[ptable[nt][key]-1])):
			if grammar[ptable[nt][key]-1][i] in non_terminals:
				check = True
				break
		if check == False:
			rules.append(key)
	# print "terminal_only:",rules
	return rules

def align_according_to_rules(tset):
	r = {}
	for key in tset:
		if tset[key] in r:
			r[tset[key]].append(key)
		else:
			r[tset[key]] = [key]
	return r

def write_to_file(output_file):
	for nt in non_terminals:
		tset = {}
		ntdict = ptable[nt]
		for term in ntdict:
			if ntdict[term] != 0:
				tset[term] = ntdict[term]
		tlist = get_terminal_only_rules(nt, tset)
		L1 = []
		L2 = []
		for key in tset:
			if key in tlist:
				L2.append(key)
			else:
				L1.append(key)
		output_file.write("""\ndef %s(d):
	global pos
	#print "%s called..."
	if output[pos] == "~":
		output[pos] = choose(d, ["""%(nt,nt))
		for i in range(len(L1)):
			if i == 0:
				output_file.write(""" "%s" """%L1[i])
			else:
				output_file.write(""" ,"%s" """%L1[i])
		output_file.write("],[")
		for i in range(len(L2)):
			if i == 0:
				output_file.write(""" "%s" """%L2[i])
			else:
				output_file.write(""" ,"%s" """%L2[i])
		output_file.write("""])
		#print output[pos] """)
		r = align_according_to_rules(tset)
		j = 0
		for key in r:
			if j == 0:
				j += 1
				output_file.write("\n")
				output_file.write("""	if """)
			else:
				output_file.write("""	elif """)

			for i in range(len(r[key])):
				if i == 0:
					output_file.write("""output[pos] == "%s" """%r[key][i])
				else:
					output_file.write("""or output[pos] == "%s" """%r[key][i])
			output_file.write(":\n")
			i = 0
			for elt in grammar[key-1]:
				if i == 0:
					i += 1
					continue
				if elt in tokens:
					output_file.write("""		consume("%s")\n"""%elt)
				else:
					output_file.write("""		%s(d+1)\n"""%elt)
		output_file.write("""	else:
		error()\n""")


output_file = open("tiger_string_generator.py", "w+")
output_file.write("""from random import *
from parser_string_generator import parser_main
output = []
pos = 0
Threshold = 5

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

""")
grammar = find_original_grammar(add = False)
ptable = get_parse_table(convert = False)
non_terminals = discover_non_tokens()
tokens = discover_tokens()
write_to_file(output_file)
output_file.write("""output.append("~")
Prog(0)
output[len(output)-1] = "$" # this will be arbitrary token which should be the end of input when the parsing stack becomes empty (recursive call returns)
print "output:",output
#parser_main(output)""")
