from prod_error1 import *

def find_original_grammar(eps = True):
	# original_grammar = [['S','eps','eps','F','S'], ['S','eps','eps','eps','Q'], ['S','(','S',')','S'], ['F','eps','eps','!','A'], ['Q','eps','eps','?','A'],['A','eps','eps','eps','eps']]
	# return get_original_grammar()
	original_grammar = [['S','a','A',],['S','b','B'],['A','0','C'],['C','A','1'],['C','1'],['B','0','D'],['D','B','1','1'],['D','1','1']]
	if eps == True:
		original_grammar = add_eps(original_grammar)
	print original_grammar
	return original_grammar
	
def specs():

	#Space separated (tokenized) strings
	# accept_strings = ["a 0 1", "b 0 1 1", "a 0 0 1 1", "a 0 0 0 1 1 1", "b 0 0 1 1 1 1", "a 0 0 0 0 1 1 1 1", "b 0 0 0 1 1 1 1 1 1", "a 0 0 0 0 0 1 1 1 1 1", "a 0 0 0 0 0 0 1 1 1 1 1 1", "b 0 0 0 0 1 1 1 1 1 1 1 1", "a 0 0 0 0 0 0 0 1 1 1 1 1 1 1", "b 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1", "a 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1", "b 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1", "a 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1", "a 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1", "b 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1", "b 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1", "b 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1", "b 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1"]
	accept_strings = ["a 0 0 0 0 0 0 0 1 1 1 1 1 1 1", "a 0 0 0 0 1 1 1 1"]
	print "correct string: ",accept_strings[0]
	tmp = produce_error(accept_strings[0], find_original_grammar(eps = False))
	accept_strings[0] = tmp
	print "changed string: ",tmp
	reject_strings = ["0", "1", "a", "b", "0 1", "0 1 1", "1 0"]

	config = {
		'num_rules': 8, #Number of rules
		'size_rules' : 3, #Number of symbols in RHS
		'num_nonterms' : 5, #Number of nonterms
		'expansion_constant' : 5, #Determines the max. number of parse actions to take while parsing
		'optimize' : True, # enable optimized mode
		'neg_egs' : False, # consider negative examples 
		'threshold' : 0.25,  # number of unsat cores to break
		'Use_CFGAnalyzer' : False, # use cfganalyzer
		'orig_grammar_link' : "orig_17.txt", # link to the original grammar 
		'eps_given' : False, # if eps is given for the grammar
		'eps_given_link' : 'eps_given/17.txt', # Where are the eps slots given
		'name':'17.txt'
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
	parse_table =  {'A': {'a': 0, '0': 3, '1': 0, 'b': 0, 'dol': 0}, 'S': {'a': 1, '0': 0, '1': 0, 'b': 2, 'dol': 0}, 'B': {'a': 0, '0': 6, '1': 0, 'b': 0, 'dol': 0}, 'C': {'a': 0, '0': 4, '1': 5, 'b': 0, 'dol': 0}, 'D': {'a': 0, '0': 7, '1': 8, 'b': 0, 'dol': 0}}
	if convert == True:
		parse_table = convert_parse_table(parse_table)
	# print len(parse_table)
	return parse_table

def nums():
	original_grammar = find_original_grammar()
	num_vars = {'num_rules':len(original_grammar), 'size_rules':len(original_grammar[0])-1}
	return num_vars

# S :	"a" A ;
#   :	"b" B ;
# A :	"0" C ;
# C :	A "1" ;
#   :	"1" ;
# B :	"0" D ;
# D :	B "1" "1" ;
#   :	"1" "1" ;
#a00001111; b000111111; a0000011111; b000011111111; a00000001111111
