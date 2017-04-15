from input_specs_tiger import *
def get_lookahead():
	if len(string) == 0:
		return 'dol'
	else:
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
	# #print parser
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

def parser(index):
	# global parse
	parse = []
	index_counter = 0
	parse.append(grammar[0][0])
	order1 = []
	ind = 0
	while len(parse) != 0:
		# print "index:%d index_counter:%d"%(index, index_counter)
		if index_counter == index+2:
			return order1,ind
		ontop = parse.pop()
		global order
		order1.append(ontop)
		lookahead = get_lookahead()
		if ontop in terminals:
			if ontop != lookahead:
				#print "parsing error...\nontop: %s but lookahead: %s"%(ontop,lookahead)
				return 0,-1
			#print "consuming token %s"%string[0]
			string.pop(0)
			if index_counter == index:
				ind = len(order1)-1
			index_counter += 1
			lookahead = get_lookahead()
		else:
			parse = expand(lookahead, parse, ontop)
			if parse == -1:
				#print "parse error...\nontop: %s but lookahead: %s"%(ontop,lookahead)
				return order1,ind
	if lookahead == "dol" and len(parse) == 0:
		print "parsed successfully..."
		return order1,ind;


def parser_main(string1, index):
	#print "############## parser called...###########"
	global string
	print "parser called with string: ",string1
	if type(string1)=="string":
		string = string1.split()
	else:
		string = string1
        
	string.append('dol')
	return parser(index)

# string = ['let', 'type', 'id', '=', 'array', 'of', 'id', 'var', 'id', ':', 'id', ':=', 'id', '[', 'integer', ']', 'of', 'integer', 'in', 'id', 'end']
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
parser_main(string, len(string))
# # for i in range(len(grammar)):
# # 	if len(grammar[i]) > maximum:
# # 		maximum = len(grammar[i])
# # #print "size_ruels:",maximum
# # add_eps(grammar)
# # parser_main([])
# #print "Order: ",order1
# rules.sort()
# #print "rules: ",rules