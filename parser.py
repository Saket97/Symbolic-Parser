from finalTestFilesOOPSLA.input_specs_tiger6 import *
def get_lookahead():
	if len(string) == 0:
		return 'dol'
	else:
		# index_counter += 1
		return string[0]

def expand(lookahead, parser, ontop):
	rule = ptable[ontop][lookahead]
	global rules
	rules.append(rule)
	# #print "rule: ",rule
	if rule == 0:
		return -1
	global order
	order.append((ontop,lookahead))
	for i in range(len(grammar[rule-1])-1,0,-1):
		if grammar[rule-1][i] == "eps":
			continue
		parser.append(grammar[rule-1][i])
	#print parser
	return parser

def discover(original_grammar):
	non_tokens = []
	for string in original_grammar:
		ch = string[0]
		if ch not in non_tokens:
			non_tokens.append(ch)
		else:
			pass
	#print "len(non_tokens):",len(non_tokens)
	return non_tokens

def discover_tokens_from_grammar():
	tokens = []
	original_grammar = grammar
	non_tokens = discover(original_grammar)
	for string in original_grammar:
		for i in range(1,len(string)):
			if string[i] in non_tokens or string[i] == "eps":
				pass
			else:
				if string[i] in tokens:
					pass
				else:
					tokens.append(string[i])
	#print ('tokens',tokens)
	return tokens

['let', 'type', 'id', '=', '{', 'id', ':', 'id', ',', 'id', ':', 'id', '}', 'var', 'id', ':', 'id', ':=', 'id', '{', 'id', '=', 'string', ',', 'id', '=', 'integer', '}', 'in', 'id', '.', 'id', ':=', 'string', ';', 'id', 'end']
['let', 'type', 'id', '=', '{', 'id', ':', 'id', ',', 'id', ':', 'id', '}', 'var', 'id', ':', 'id', ':=', 'id', '{', 'id', '=', 'string', ',', 'id', '=', 'integer', '}', 'in', 'id', '.', 'id', ':=', 'string', ';', 'id', 'end']
def parser(index):
	# global parse
	parse = []
	index_counter = 0
	parse.append(grammar[0][0])
	order1 = []
	ind = 0
	if index == 0:
		return parse,0
	while len(parse) != 0:
		# print "len(parse):",len(parse)
		# print "index:%d index_counter:%d"%(index, index_counter)
		ontop = parse.pop()
		global order
		order1.append(ontop)
		lookahead = get_lookahead()

		if ontop in terminals:
			if ontop != lookahead:
				print "parsing error...\nontop: %s but lookahead: %s"%(ontop,lookahead)
				return 0,-1
			#print "consuming token %s"%string[0]
			string.pop(0)

			index_counter += 1
			if index_counter == index:
				return order1,ind
			lookahead = get_lookahead()
		else:
			parse = expand(lookahead, parse, ontop)
			if parse == -1:
				print "parse error...\nontop: %s but lookahead: %s"%(ontop,lookahead)
				return 0,-1
	if lookahead == "dol" and len(parse) == 0:
		print "parsed successfully..."
		return order1,ind;
	if len(parse) == 0 and len(string) == 0:
		print "parsed successfully..."
		return order1, ind
	print "len(string):",len(string)
	print "len(parse):",len(parse)

def parser_main(string1, index):
	#print "############## parser called...###########"
	global string
	print "parser called with string: ",string1
	print "index:",index
	if type(string1)=="string":
		string = string1.split()
	else:
		string = string1
	# string = ['let', 'type', 'id', '=', 'array', 'of', 'id', 'in', 'id', ':', 'id', ':=', 'id', '[', 'integer', ']', 'of', 'integer', 'in', 'id', 'end']
	#string=['let', 'type', 'id', '=', 'array', 'of', 'id', 'var', 'id', ':', 'id', ':=', 'id', '[', 'integer', ']', 'of', 'integer', 'in', 'id', 'end']
	string.append('dol')
	return parser(index)

#r', 'id', ':', 'id', ':=', 'id', '{', 'id', '=', 'string', ',', 'id', '=', 'integer', '}', 'in', 'id', '.', 'id', ':=', 'string', ';', 'id', 'end']
string = ['let', 'type', 'id', '=', 'array', 'of', 'id', 'var', 'id', ':', 'id', ':=', 'id', '[', 'integer', ']', 'of', 'integer', 'in', 'id', 'end']
string  = []
order = []
grammar = find_original_grammar(eps = False)
ptable = get_parse_table(convert = False)
#print "type(ptable)=",type(ptable)
terminals = discover_tokens_from_grammar()
terminals.append("dol")
fuel = 20

rules = []

maximum = 0
# parser_main(string, 100)
# # for i in range(len(grammar)):
# # 	if len(grammar[i]) > maximum:
# # 		maximum = len(grammar[i])
# # #print "size_ruels:",maximum
# # add_eps(grammar)
# # parser_main([])
# print "Order: ",order
# rules.sort()
# #print "rules: ",rules
#parser_main(string, 100)
