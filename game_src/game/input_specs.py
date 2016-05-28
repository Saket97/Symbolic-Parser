# from 'game_src/game/views' import * 
def specs():

	#Space separated (tokenized) strings
	# accept_strings = ["( )","( ) ( )", "( ( ) )","( ) ( ( ) )"]
	# reject_strings = ["(",")","( ) ("]

	config = {
		'num_rules': 2, #Number of rules
		'size_rules' : 4, #Number of symbols in RHS
		'num_nonterms' : 1, #Number of nonterms
		'expansion_constant' : 4, #Determines the max. number of parse actions to take while parsing
		'optimize' : False, # enable optimized mode
		'neg_egs' : True, # consider negative examples 
		'threshold' : 0.2,  # number of unsat cores to break
		'num_terms':2
	}

	# return accept_strings,reject_strings,config
	return config

def find_original_grammar():
	original_grammar = [['S', '(', ')', '(', '('], ['S', 'eps', 'eps', 'eps', 'eps']]
	# return get_original_grammar()
	return original_grammar
def nums():
	num_vars = {'num_rules':2, 'size_rules':4}
	return num_vars
def get_parse_table():
	parse_table = {'S':{'(':1,')':2,'dol':2}}

	return parse_table

config = specs()
tokens = ['(',')']
# accept_strings = ["( )","( ) ( )", "( ( ) )","( ) ( ( ) )"]
# reject_strings = ["(",")","( ) ("]

##	S -> (S)S | eps
##
