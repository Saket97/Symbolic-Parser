from prod_error1 import *

def find_original_grammar(eps = True):
	# original_grammar = [['S','eps','eps','F','S'], ['S','eps','eps','eps','Q'], ['S','(','S',')','S'], ['F','eps','eps','!','A'], ['Q','eps','eps','?','A'],['A','eps','eps','eps','eps']]
	# return get_original_grammar()
	original_grammar = [['S','f','E','t','S','a','S'],['S','w','E','d','S'],['S','b','S1','e'],['S1','S','c','S1'],['S1','eps'],['E','i']]
	if eps == True:
		original_grammar = add_eps(original_grammar)
	print original_grammar
	return original_grammar
	
def specs():

	#Space separated (tokenized) strings
	accept_strings = ["b e", "b b e c e", "w i d b e", "b w i d b e c e", "w i d b b e c e", "b b e c b e c e", "f i t b e a b e", "b b b e c e c e", "w i d w i d b e", "w i d w i d b b e c e", "f i t w i d b e a b e", "f i t b e a b b e c e", "w i d f i t b e a b e", "w i d b w i d b e c e", "f i t b e a w i d b e", "b w i d w i d b e c e", "w i d w i d w i d b e", "f i t b b e c e a b e", "b f i t b e a b e c e", "w i d b b e c b e c e"]
	accept_strings = ["f i t w i d b e a b e", "f i t f i t b e a b e a b e"]
	print "correct string: ",accept_strings[0]
	tmp = produce_error(accept_strings[0], find_original_grammar(eps = False))
	accept_strings[0] = tmp
	print "changed string: ",tmp
	reject_strings = ["b","e","f","t","a","w","d","i"]

	config = {
		'num_rules': 6, #Number of rules
		'size_rules' : 6, #Number of symbols in RHS
		'num_nonterms' : 3, #Number of nonterms
		'expansion_constant' : 5, #Determines the max. number of parse actions to take while parsing
		'optimize' : True, # enable optimized mode
		'neg_egs' : True, # consider negative examples 
		'threshold' : 0.5,  # number of unsat cores to break
		'Use_CFGAnalyzer' : False, # use cfganalyzer
		'orig_grammar_link' : "orig_5.txt", # link to the original grammar 
		'eps_given' : False, # if eps is given for the grammar
		'eps_given_link' : 'eps_given/5.txt', # Where are the eps slots given
		'name':'5.txt'
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
	parse_table =  {'S': {'a': 0, 'c': 0, 'b': 3, 'e': 0, 'd': 0, 'dol': 0, 'f': 1, 'i': 0, 't': 0, 'w': 2}, 'E': {'a': 0, 'c': 0, 'b': 0, 'e': 0, 'd': 0, 'dol': 0, 'f': 0, 'i': 6, 't': 0, 'w': 0}, 'S1': {'a': 0, 'c': 0, 'b': 4, 'e': 5, 'd': 0, 'dol': 0, 'f': 4, 'i': 0, 't': 0, 'w': 4}}
	if convert == True:
		parse_table = convert_parse_table(parse_table)
	# print len(parse_table)
	return parse_table

def nums():
	original_grammar = find_original_grammar()
	num_vars = {'num_rules':len(original_grammar), 'size_rules':len(original_grammar[0])-1}
	return num_vars
# S	: "f" E "t" S "a" S
# 	| "w" E "d" S
# 	| "b" S1 "e";
# S1	: S "c" S1
# 	| ;
# E	: "i";
#fitbeabe; fitwidbeabe; fitfitbeabeabe


