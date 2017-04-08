from input_specs_tiger import *
def get_lookahead():
	if len(string) == 0:
		return 'dol'
	else:
		return string[0]

def expand(lookahead, parser, ontop):
	rule = ptable[ontop][lookahead]
	if rule == 0:
		return -1
	global order
	order.append((ontop,lookahead))
	for i in range(len(grammar[rule-1])-1,0,-1):
		if grammar[rule-1][i] == "eps":
			continue
		parser.append(grammar[rule-1][i])
	print parser
	return parser

def discover(original_grammar):
	non_tokens = []
	for string in original_grammar:
		ch = string[0]
		if ch not in non_tokens:
			non_tokens.append(ch)
		else:
			pass
	print "len(non_tokens):",len(non_tokens)
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
	print ('tokens',tokens)
	return tokens

def parser():
	global parse
	parse.append(grammar[0][0])
	
	while len(parse) != 0:
		ontop = parse.pop()
		lookahead = get_lookahead()
		if ontop in terminals:
			if ontop != lookahead:
				print "parsing error...\nontop: %s but lookahead: %s"%(ontop,lookahead)
				return 0
			print "consuming token %s"%string[0]
			string.pop(0)
			lookahead = get_lookahead()
		else:
			parse = expand(lookahead, parse, ontop)
			if parse == -1:
				print "parse error...\nontop: %s but lookahead: %s"%(ontop,lookahead)
				return 0
	if lookahead == "dol" and len(parse) == 0:
		print "parsed successfully..."
		return 1;


def parser_main(string1):
	print "############## parser called...###########"
	global string
	print "parser called with string: ",string1
	string = string1
        # string = ['i','+','i']
	# string = ['(', 'end', '<=', 'for', '~', '~', 'for', '~', '~', 'id', '.', '~', '>', 'id', '/', 'break', '|', 'integer', 'do', 'string', 'then', '(', 'end', 'dol', 'nil', 'do', 'nil',]
	return parser()

string = []
grammar = find_original_grammar(eps = False)
ptable = get_parse_table(convert = False)
print "type(ptable)=",type(ptable)
parse = []
terminals = discover_tokens_from_grammar()
terminals.append("dol")
fuel = 20
order = []
# for i in range(len(order)):
# 	print order[i]
	
print "#rules:",len(grammar)
maximum = 0
# for i in range(len(grammar)):
# 	if len(grammar[i]) > maximum:
# 		maximum = len(grammar[i])
# print "size_ruels:",maximum
# add_eps(grammar)
# parser_main([])
