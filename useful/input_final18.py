from prod_error1 import *

def find_original_grammar(eps = True):
	# original_grammar = [['S','eps','eps','F','S'], ['S','eps','eps','eps','Q'], ['S','(','S',')','S'], ['F','eps','eps','!','A'], ['Q','eps','eps','?','A'],['A','eps','eps','eps','eps']]
	# return get_original_grammar()
	original_grammar = [['S','a','S','b','S','c'],['S','1','S','2','S','3'],['S','d'],['S','4']]
	if eps == True:
		original_grammar = add_eps(original_grammar)
	print original_grammar
	return original_grammar
	
def specs():

	#Space separated (tokenized) strings
	# accept_strings = ["4", "d", "a 4 b 4 c", "1 d 2 d 3", "1 d 2 4 3", "a 4 b d c", "1 4 2 d 3", "a d b 4 c", "1 4 2 4 3", "a d b d c", "a d b 1 d 2 d 3 c", "a d b a 4 b 4 c c", "a d b 1 d 2 4 3 c", "a d b a 4 b d c c", "a d b 1 4 2 d 3 c", "a d b a d b 4 c c", "a d b 1 4 2 4 3 c", "a d b a d b d c c", "a 4 b a d b d c c", "a 4 b a d b 4 c c"]
	accept_strings = ["a 4 b 1 a d b 4 c 2 4 3 c", "a a d b d c b 4 c"]
	print "correct string: ",accept_strings[0]
	tmp = produce_error(accept_strings[0], find_original_grammar())
	accept_strings[0] = tmp
	print "changed string: ",tmp
	reject_strings = ["1", "2", "3", "a", "b", "c"]

	config = {
		'num_rules': 4, #Number of rules
		'size_rules' : 5, #Number of symbols in RHS
		'num_nonterms' : 1, #Number of nonterms
		'expansion_constant' : 5, #Determines the max. number of parse actions to take while parsing
		'optimize' : True, # enable optimized mode
		'neg_egs' : False, # consider negative examples 
		'threshold' : 0.25,  # number of unsat cores to break
		'Use_CFGAnalyzer' : False, # use cfganalyzer
		'orig_grammar_link' : "orig_18.txt", # link to the original grammar 
		'eps_given' : False, # if eps is given for the grammar
		'eps_given_link' : 'eps_given/18.txt', # Where are the eps slots given
		'name':'18.txt'
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
	parse_table =  {'S': {'a': 1, 'c': 0, 'b': 0, 'd': 3, 'dol': 0, '1': 2, '3': 0, '2': 0, '4': 4}}
	if convert == True:
		parse_table = convert_parse_table(parse_table)
	# print len(parse_table)
	return parse_table

def nums():
	original_grammar = find_original_grammar()
	num_vars = {'num_rules':len(original_grammar), 'size_rules':len(original_grammar[0])-1}
	return num_vars
# S : "a" S "b" S "c" ;
#   :  "1" S "2" S "3" ;
#   : "d" ;
#   : "4" ;
#aadbdcb4c; a4b1adb4c243c; 
