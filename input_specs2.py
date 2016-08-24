def specs():

	#Space separated (tokenized) strings
	accept_strings = ["a b","a a c c b","a a a c c b b c b","a a c b c b"]
	reject_strings = ["a c","a b","a a c c c b"]

	config = {
		'num_rules': 5, #Number of rules
		'size_rules' : 4, #Number of symbols in RHS
		'num_nonterms' : 3, #Number of nonterms
		'expansion_constant' : 9, #Determines the max. number of parse actions to take while parsing
		'optimize' : True, # enable optimized mode
		'neg_egs' : True, # consider negative examples 
		'threshold' : 1  # number of unsat cores to break
	}

	return accept_strings,reject_strings,config

def find_original_grammar():
	original_grammar = [['S','a','A','B','b'],['A','eps','a','A','c'],['A','eps','eps','eps','eps'],['B','eps','eps','b','B'],['B','eps','eps','eps','c']]
	# return get_original_grammar()
	return original_grammar

def get_parse_table():
	parse_table = [{'non_term':'S' ,'a':1 ,'b':0 ,'c':0 ,'$':0},{'non_term':'A' ,'a':2 ,'b':3 ,'c':3 ,'$':0},{'non_term':'B' ,'a':0 ,'b':4 ,'c':5 ,'$':0}]
	return parse_table

def nums():
	original_grammar = find_original_grammar()
	num_vars = {'num_rules':len(original_grammar), 'size_rules':len(original_grammar[0])-1}
	return num_vars

def get_first_set():
	first_set = [{'non_term':'S' ,'a':1 ,'b':0 ,'c':0,'eps': 0},{'non_term':'A' ,'a':1 ,'b':0,'c':0 ,'eps':1 },{'non_term':'B' ,'a':0 ,'b':1,'c':1 ,'eps':0 }]
	return first_set

def get_follow_set():
	follow_set = [{'non_term':'S' ,'a':0 ,'b':0 ,'c':0 ,'$':1},{'non_term':'A' ,'a':0 ,'b': 1,'c':1 ,'$':0},{'non_term':'B' ,'a':0 ,'b':1 ,'c': 0,'$':0}]
	return follow_set

accept_strings = ["a c b","a a c c b","a a a c c b b c b","a a c b c b"]
reject_strings = ["a c","a b","a a c c c b"]
#S -> a A B b
#A -> a A c
#A -> eps
#B -> b B
#B -> c

