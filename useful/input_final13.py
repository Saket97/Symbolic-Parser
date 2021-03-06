from prod_error1 import *
def specs():

	#Space separated (tokenized) strings
	# accept_strings = ["b", "a a b", "a b b a b", "a a a a b", "a a a b b a b", "a b b b b a b", "a b b a a a b", "a b a a b a b", "a a a a a a b", "a b b b b a a a b", "a b a a b a a a b", "a a a b b a a a b", "a a a a a b b a b", "a b b a a a a a b", "a b b a a b b a b", "a a a a a a a a b", "a a a b b b b a b", "a b b b b b b a b", "a b a a b b b a b", "a a a b a a b a b"]
	accept_strings = ["a a a a b b a a a a a a a a b"]
	# print "correct string: ",accept_strings[0]
	# tmp = produce_error(accept_strings[0])
	# accept_strings[0] = tmp
	# print "changed string: ",tmp
	reject_strings = ["a", "b b", "b b b", "a b", "a b b"]

	config = {
		'num_rules': 4, #Number of rules
		'size_rules' : 3, #Number of symbols in RHS
		'num_nonterms' : 2, #Number of nonterms
		'expansion_constant' : 5, #Determines the max. number of parse actions to take while parsing
		'optimize' : True, # enable optimized mode
		'neg_egs' : False, # consider negative examples 
		'threshold' : 0.25,  # number of unsat cores to break
		'Use_CFGAnalyzer' : False, # use cfganalyzer
		'orig_grammar_link' : "orig_13.txt", # link to the original grammar 
		'eps_given' : False, # if eps is given for the grammar
		'eps_given_link' : 'eps_given/13.txt', # Where are the eps slots given
		'name':'13.txt'
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

def find_original_grammar():
	# original_grammar = [['S','eps','eps','F','S'], ['S','eps','eps','eps','Q'], ['S','(','S',')','S'], ['F','eps','eps','!','A'], ['Q','eps','eps','?','A'],['A','eps','eps','eps','eps']]
	# return get_original_grammar()
	original_grammar = [['S','a','A','S'],['S','b'],['A','b','S','A'],['A','a']]
	original_grammar = add_eps(original_grammar)
	print original_grammar
	return original_grammar

def convert_parse_table(ptable):
	parse_table = []
	for key in ptable:
		tmp = ptable[key]
		tmp['non_term'] = key
		parse_table.append(tmp)
	print "len(parse_table):",len(parse_table)
	# print parse_table
	return parse_table

def get_parse_table():
	parse_table =  {'A': {'a': 4, 'b': 3, 'dol': 0}, 'S': {'a': 1, 'b': 2, 'dol': 0}}
	parse_table = convert_parse_table(parse_table)
	# print len(parse_table)
	return parse_table

def nums():
	original_grammar = find_original_grammar()
	num_vars = {'num_rules':len(original_grammar), 'size_rules':len(original_grammar[0])-1}
	return num_vars

# S : "a" A S ;
#   : "b" ;
# A : "b" S A ;
#   : "a" ;
#aaaaaaaab; aaaaaaaaaab; aaaaaaaaaaaaaab;aaaaaaaaaaaab
