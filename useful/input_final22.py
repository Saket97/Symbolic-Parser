from prod_error1 import *

def find_original_grammar(eps = True):
	# original_grammar = [['S','eps','eps','F','S'], ['S','eps','eps','eps','Q'], ['S','(','S',')','S'], ['F','eps','eps','!','A'], ['Q','eps','eps','?','A'],['A','eps','eps','eps','eps']]
	# return get_original_grammar()
	original_grammar = [['E','T','X'],['X','+','E'],['X','eps'],['T','(','E',')'],['T','i','Y'],['Y','*','T'],['Y','eps']]
	if eps == True:
		original_grammar = add_eps(original_grammar)
	print original_grammar
	return original_grammar
def specs():

	#Space separated (tokenized) strings
	accept_strings = ["i", "( i )", "i + i", "i * i", "i * i + i", "( ( i ) )", "i + i * i", "( i ) + i", "i * ( i )", "( i + i )", "( i * i )", "i + ( i )", "i * i * i", "( i * i * i )", "i * ( i * i )", "i * i * i * i", "i * i * ( i )", "i + i * i * i", "i * i + i * i", "i * i * i * i * i"]
	accept_strings = ["( ( ( ( i ) ) ) )", "( ( ( ( ( ( ( i ) ) ) ) ) ) )"]
	print "correct string: ",accept_strings[0]
	tmp = produce_error(accept_strings[0], find_original_grammar(eps = False))
	accept_strings[0] = tmp
	print "changed string: ",tmp
	reject_strings = ["(", ")", "+", "*", "( i", "i )", "i +", "i *", "+ i", "* i"]

	config = {
		'num_rules': 7, #Number of rules
		'size_rules' : 3, #Number of symbols in RHS
		'num_nonterms' : 4, #Number of nonterms
		'expansion_constant' : 5, #Determines the max. number of parse actions to take while parsing
		'optimize' : True, # enable optimized mode
		'neg_egs' : True, # consider negative examples 
		'threshold' : 0.25,  # number of unsat cores to break
		'Use_CFGAnalyzer' : False, # use cfganalyzer
		'orig_grammar_link' : "orig_8.txt", # link to the original grammar 
		'eps_given' : False, # if eps is given for the grammar
		'eps_given_link' : 'eps_given/8.txt', # Where are the eps slots given
		'name':'8.txt'
	}

	return accept_strings,reject_strings,config

def add_eps(original_grammar):
	grammar = []
	maxsize = 0
	for i in range(len(original_grammar)):
		if len(original_grammar[i]) > maxsize:
			maxsize = len(original_grammar[i])
	for i in range(len(original_grammar)):
		tmp = []
		t = len(original_grammar[i])
		tmp.append(original_grammar[i][0])
		for j in range(maxsize-t):
			tmp.append("eps")
		for j in range(1,len(original_grammar[i])):
			tmp.append(original_grammar[i][j])
		grammar.append(tmp)
	return grammar

def convert_parse_table(ptable):
	parse_table = []
	for key in ptable:
		tmp = ptable[key]
		tmp['non_term'] = key
		parse_table.append(tmp)
	print "len(parse_table):",len(parse_table)
	# print parse_table
	return parse_table

def get_parse_table(convert = True):
	parse_table =  {'Y': {'dol': 7, ')': 7, '(': 0, '+': 7, '*': 6, 'i': 0}, 'X': {'dol': 3, ')': 3, '(': 0, '+': 2, '*': 0, 'i': 0}, 'E': {'dol': 0, ')': 0, '(': 1, '+': 0, '*': 0, 'i': 1}, 'T': {'dol': 0, ')': 0, '(': 4, '+': 0, '*': 0, 'i': 5}}
	if convert == True:
		parse_table = convert_parse_table(parse_table)
	# print len(parse_table)
	return parse_table

def nums():
	original_grammar = find_original_grammar()
	num_vars = {'num_rules':len(original_grammar), 'size_rules':len(original_grammar[0])-1}
	return num_vars

# # E : T X ;
# # X : "+" E 
# 	| ;
# # T : "(" E ")" 
# 	| "i" Y;
# # Y : "*" T 
# 	| ;
#((((i)))); (((((i))))); ((((((i)))))); (((((((i)))))))
