def specs():

	#Space separated (tokenized) strings
	accept_strings = ['d b b e', 'c b e','a c b e b e']
	reject_strings = ['a d b b e']

	config = {
		'num_rules': 6, #Number of rules
		'size_rules' : 3, #Number of symbols in RHS
		'num_nonterms' : 3, #Number of nonterms
		'expansion_constant' : 7, #Determines the max. number of parse actions to take while parsing
		'optimize' : False, # enable optimized mode
		'neg_egs' : True, # consider negative examples 
		'threshold' : 0.2  # number of unsat cores to break
	}

	return accept_strings,reject_strings,config

def find_original_grammar():
	original_grammar = [['S','eps','A','e'],['A','d','B','B'],['A','a','S','B'],['A','eps','c','b'],['B','A','B','c'],['B','eps','eps','b']]
	# return get_original_grammar()
	return original_grammar

def get_parse_table():
	parse_table = [{'non_term':'S' ,'a':1 ,'b':0 ,'c':1 ,'d':1 ,'e':0 ,'$':0},{'non_term':'A' ,'a':3 ,'b':0 ,'c':4 ,'d':2 ,'e':0 ,'$':0},{'non_term':'B' ,'a':5 ,'b':6 ,'c':5 ,'d':5 ,'e':0 ,'$':0}]
	return parse_table

def nums():
	original_grammar = find_original_grammar()
	num_vars = {'num_rules':len(original_grammar), 'size_rules':len(original_grammar[0])-1}
	return num_vars

def get_first_set():
	first_set = [{'non_term': 'S','a':1 ,'b':0 ,'c':1 ,'d':1 ,'e':0 ,'eps':0},{'non_term':'A' ,'a':1 ,'b':0 ,'c':1 ,'d':1 ,'e':0 ,'eps':0},{'non_term':'B' ,'a':1 ,'b':1 ,'c':1 ,'d':1 ,'e':0 ,'eps':0}]
	return first_set

def get_follow_set():
	follow_set = [{'non_term':'S' ,'a':1 ,'b':1 ,'c':1 ,'d':1 ,'e':1 ,'$':1},{'non_term':'A' ,'a':1 ,'b':1 ,'c':1 ,'d':1 ,'e':0 ,'$':0},{'non_term':'B' ,'a':1 ,'b':1 ,'c':1 ,'d':1 ,'e':1 ,'$':0}]
	return follow_set



accept_strings = ['d b b e', 'c b e','a c b e b e']
reject_strings = ['a d b b e']

# S -> A B e
# A -> d B
# A -> a S
# A -> c
# B -> A S
# B -> b