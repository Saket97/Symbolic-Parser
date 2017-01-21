from prod_error1 import *

def find_original_grammar(eps=True):
	# original_grammar = [['S','eps','eps','F','S'], ['S','eps','eps','eps','Q'], ['S','(','S',')','S'], ['F','eps','eps','!','A'], ['Q','eps','eps','?','A'],['A','eps','eps','eps','eps']]
	# return get_original_grammar()
	original_grammar = [['E','T','R'], ['R','+','T','R'],['R','-','T','R'],['R','eps'],['T','i']]
	if eps == True:
		original_grammar = add_eps(original_grammar)
	print original_grammar
	return original_grammar

def specs():

	#Space separated (tokenized) strings
	# accept_strings = ["i", "i - i", "i + i", "i - i + i", "i + i - i", "i - i - i", "i + i + i", "i - i + i + i", "i + i - i - i", "i - i + i - i", "i + i - i + i", "i - i - i + i", "i + i + i - i", "i - i - i - i", "i + i + i + i", "i + i + i + i + i", "i + i + i + i - i", "i + i + i - i + i", "i + i + i - i - i", "i + i - i + i + i"]
	accept_strings = ["i + i - i + i + i"]
	print "correct string: ",accept_strings[0]
	tmp = produce_error(accept_strings[0], find_original_grammar(eps = False),delete=True)
	accept_strings[0] = tmp
	print "changed string: ",tmp
	reject_strings = ["+", "-", "+ i", "- i", "i +", "i -", "i i"]

	config = {
		'num_rules': 5, #Number of rules
		'size_rules' : 3, #Number of symbols in RHS
		'num_nonterms' : 3, #Number of nonterms
		'expansion_constant' : 5, #Determines the max. number of parse actions to take while parsing
		'optimize' : True, # enable optimized mode
		'neg_egs' : False, # consider negative examples 
		'threshold' : 0.25,  # number of unsat cores to break
		'Use_CFGAnalyzer' : False, # use cfganalyzer
		'orig_grammar_link' : "orig_10.txt", # link to the original grammar 
		'eps_given' : False, # if eps is given for the grammar
		'eps_given_link' : 'eps_given/10.txt', # Where are the eps slots given
		'name':'10.txt'
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

def get_parse_table(convert=True):
	parse_table =  {'R': {'i': 0, '+': 2, '-': 3, 'dol': 4}, 'E': {'i': 1, '+': 0, '-': 0, 'dol': 0}, 'T': {'i': 5, '+': 0, '-': 0, 'dol': 0}}
	if convert == True:
		parse_table = convert_parse_table(parse_table)
	# print len(parse_table)
	return parse_table

def nums():
	original_grammar = find_original_grammar()
	num_vars = {'num_rules':len(original_grammar), 'size_rules':len(original_grammar[0])-1}
	return num_vars

# accept_strings = ["i", "i - i", "i + i", "i - i + i", "i + i - i", "i - i - i", "i + i + i", "i - i + i + i", "i + i - i - i", "i - i + i - i", "i + i - i + i", "i - i - i + i", "i + i + i - i", "i - i - i - i", "i + i + i + i", "i + i + i + i + i", "i + i + i + i - i", "i + i + i - i + i", "i + i + i - i - i", "i + i - i + i + i"]
accept_strings = ["i + i - i + i + i"]
# E : T R ;
# R : "+" T R ;
#   : "-" T R ;
#   : ;                               
# T : "i";
