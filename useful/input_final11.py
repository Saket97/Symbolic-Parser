from prod_error1 import *

def find_original_grammar(eps = True):
	# original_grammar = [['S','eps','eps','F','S'], ['S','eps','eps','eps','Q'], ['S','(','S',')','S'], ['F','eps','eps','!','A'], ['Q','eps','eps','?','A'],['A','eps','eps','eps','eps']]
	# return get_original_grammar()
	original_grammar = [['S','A','S1'],['S1','o','A','S1'],['S1','eps'],['A','B','A1'],['A1','a','B','A1'],['A1','eps'],['B','n','B'],['B','(','S',')'],['B','1'],['B','0']]
	if eps == True:
		original_grammar = add_eps(original_grammar)
	print original_grammar
	return original_grammar

def specs():

	#Space separated (tokenized) strings
	# accept_strings = ["0", "1", "n 0", "n 1", "0 o 0", "0 a 0", "0 a 1", "( 0 )", "n n 1", "1 a 0", "n n 0", "1 a 1", "n 0 a 0", "1 a n 1", "n 0 a 1", "1 a n 0", "n 1 a 0", "0 a n 1", "n 1 a 1", "0 a n 0", "n n n 1", "n n n 0"]
	accept_strings = ["n n n ( n n n n n n n 1 )", "( 0 o ( n n 0 ) o 1 )"]
	print "correct string: ",accept_strings[0]
	tmp = produce_error(accept_strings[0], find_original_grammar(eps = False))
	accept_strings[0] = tmp
	print "changed string: ",tmp
	reject_strings = ["n", "a", "0 a", "1 a", "a 0", "a 1", "1 n", "0 n"]

	config = {
		'num_rules': 10, #Number of rules
		'size_rules' : 3, #Number of symbols in RHS
		'num_nonterms' : 5, #Number of nonterms
		'expansion_constant' : 5, #Determines the max. number of parse actions to take while parsing
		'optimize' : True, # enable optimized mode
		'neg_egs' : False, # consider negative examples 
		'threshold' : 0.25,  # number of unsat cores to break
		'Use_CFGAnalyzer' : False, # use cfganalyzer
		'orig_grammar_link' : "orig_11.txt", # link to the original grammar 
		'eps_given' : False, # if eps is given for the grammar
		'eps_given_link' : 'eps_given/11.txt', # Where are the eps slots given
		'name':'11.txt'
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

def find_original_grammar(eps = True):
	# original_grammar = [['S','eps','eps','F','S'], ['S','eps','eps','eps','Q'], ['S','(','S',')','S'], ['F','eps','eps','!','A'], ['Q','eps','eps','?','A'],['A','eps','eps','eps','eps']]
	# return get_original_grammar()
	original_grammar = [['S','A','S1'],['S1','o','A','S1'],['S1','eps'],['A','B','A1'],['A1','a','B','A1'],['A1','eps'],['B','n','B'],['B','(','S',')'],['B','1'],['B','0']]
	if eps == True:
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

def get_parse_table(convert = True):
	parse_table =  {'A': {'a': 0, 'dol': 0, ')': 0, '(': 4, 'o': 0, 'n': 4, '1': 4, '0': 4}, 'A1': {'a': 5, 'dol': 6, ')': 6, '(': 0, 'o': 6, 'n': 0, '1': 0, '0': 0}, 'S': {'a': 0, 'dol': 0, ')': 0, '(': 1, 'o': 0, 'n': 1, '1': 1, '0': 1}, 'B': {'a': 0, 'dol': 0, ')': 0, '(': 8, 'o': 0, 'n': 7, '1': 9, '0': 10}, 'S1': {'a': 0, 'dol': 3, ')': 3, '(': 0, 'o': 2, 'n': 0, '1': 0, '0': 0}}
	if convert == True:
		parse_table = convert_parse_table(parse_table)
	# print len(parse_table)
	return parse_table

def nums():
	original_grammar = find_original_grammar()
	num_vars = {'num_rules':len(original_grammar), 'size_rules':len(original_grammar[0])-1}
	return num_vars

# accept_strings = ["n ( n n n 0 a 0 )"]

# S  : A S1 ;
# S1 : "o" A S1 ;
#    : ;
# A  : B A1 ;
# A1 : "a" B A1 ;
#    : ;
# B  : "n" B ;
#    : "(" S ")" ;
#    : "1" ;
#    :  "0" ;
#n(nnn0a0); (0on0a0o0); (0o(nn0)o1); n0onnn0on0a0; nnn(nnnnnnn1); 
