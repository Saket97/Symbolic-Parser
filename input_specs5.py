def specs():

	#Space separated (tokenized) strings
	accept_strings = ["b", "a a b c c","a a b b c c","b b b"]
	reject_strings = ["c","b a","b a a b"]

	config = {
		'num_rules': 5, #Number of rules
		'size_rules' : 3, #Number of symbols in RHS
		'num_nonterms' : 3, #Number of nonterms
		'expansion_constant' : 4, #Determines the max. number of parse actions to take while parsing
		'optimize' : True, # enable optimized mode
		'neg_egs' : True, # consider negative examples 
		'threshold' : 1  # number of unsat cores to break
	}

	return accept_strings,reject_strings,config

def find_original_grammar():
	original_grammar = [['T*','eps','eps','T'],['T','eps','eps','R'],['T','a','T','c'],['R','eps','eps','eps'],['R','eps','b','R']]
	# return get_original_grammar()
	return original_grammar

def get_parse_table():
	parse_table = [{'non_term':'T*' ,'a':1 ,'b':1 ,'c':0 ,'$':1},{'non_term':'T' ,'a':3 ,'b':2 ,'c':2 ,'$':2},{'non_term':'R' ,'a':0 ,'b':5 ,'c':4 ,'$':4}]
	return parse_table

def nums():
	original_grammar = find_original_grammar()
	num_vars = {'num_rules':len(original_grammar), 'size_rules':len(original_grammar[0])-1}
	return num_vars

def get_first_set():
	first_set = [{'non_term':'T*' ,'a':1 ,'b':1 ,'c':0 ,'eps':1},{'non_term':'T' ,'a':1 ,'b':1 ,'c':0 ,'eps':1},{'non_term':'R' ,'a':0 ,'b':1 ,'c':0 ,'eps':1}]
	return first_set

def get_follow_set():
	follow_set = [{'non_term':'T*' ,'a':0 ,'b':0 ,'c':0 ,'$':1},{'non_term':'T' ,'a':0 ,'b':0 ,'c':1 ,'$':1},{'non_term':'R' ,'a':0 ,'b':0 ,'c':1 ,'$':1}]
	return follow_set
accept_strings = ["b", "a a b c c","a a b b c c","b b b"]
reject_strings = ["c","b a","b a a b"]


# T' -> T
# T -> R
# T -> a T c
# R -> eps
# R -> b R