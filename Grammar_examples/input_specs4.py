def specs():

	#Space separated (tokenized) strings
	accept_strings = ["id","- id",". id", "- id . id -","- id . id - - -"]
	reject_strings = ["- - -"]

	config = {
		'num_rules': 7, #Number of rules
		'size_rules' : 3, #Number of symbols in RHS
		'num_nonterms' : 4, #Number of nonterms
		'expansion_constant' : 4, #Determines the max. number of parse actions to take while parsing
		'optimize' : True, # enable optimized mode
		'neg_egs' : True, # consider negative examples 
		'threshold' : 1  # number of unsat cores to break
	}

	return accept_strings,reject_strings,config

def find_original_grammar():
	print "This is incorrect grammar. this is not even LL1."
	original_grammar = [['S','eps','eps','A'], ['A','-','A','B'],['A','eps','id','C'],['B','eps','-','B'],['B','eps','eps','eps'],['C','eps','eps','eps'],['C','eps','.','id']]
	# return get_original_grammar()
	return original_grammar

def get_parse_table():
	parse_table = [{'non_term':'A' ,'-':2 ,'.':0 ,'$':0,'id':3 },{'non_term':'B' ,'-':4 ,'.':0 ,'$':5,'id':0 },{'non_term':'C' ,'-':6 ,'.':07 ,'$':6,'id':0 },{'non_term':'S' ,'-':1 ,'.':0 ,'$':0,'id':01 }]
	return parse_table

def nums():
	original_grammar = find_original_grammar()
	num_vars = {'num_rules':len(original_grammar), 'size_rules':len(original_grammar[0])-1}
	return num_vars

def get_first_set():
	first_set = [{'non_term':'A' ,'-':1 ,'.':0,'id':1 ,'eps':0 },{'non_term':'B' ,'-':1 ,'.':0 ,'eps':1,'id':0 },{'non_term':'C' ,'-':0 ,'.':1 ,'eps':1, 'id':0 },{'non_term':'S' ,'-':1 ,'.':1 ,'eps':0,'id':0 }]
	return first_set

def get_follow_set():
	follow_set = [{'non_term':'A' ,'-':1 ,'.':0 ,'$':1,'id':0 },{'non_term':'B' ,'-':1 ,'.':0 ,'$':1,'id':0 },{'non_term':'C' ,'-':1 ,'.':0 ,'$':1,'id':0 },{'non_term':'S' ,'-':0 ,'.':0 ,'$':1,'id':0 }]
	return follow_set

accept_strings = ["id","- id",". id", "- id . id -","- id . id - - -"]
reject_strings = ["- - -"]

# S -> A
# A -> - A B
# A -> id C
# B -> - B
# B -> eps
# C -> eps
# C -> . id