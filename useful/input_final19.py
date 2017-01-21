def specs():

	#Space separated (tokenized) strings
	accept_strings = ["( )","( ( ) )","( ) ( )","( ) ( ( ) )","( ( ) ( ) )","( ( ) ) ( )","( ( ( ) ) )","( ) ( ) ( )","( ( ) ( ) ) ( )","( ( ( ) ) ) ( )","( ) ( ( ) ) ( )","( ) ( ) ( ( ) )","( ( ) ) ( ) ( )","( ( ) ) ( ( ) )","( ) ( ) ( ) ( )","( ) ( ( ) ( ) )","( ( ) ( ) ( ) )","( ( ( ) ) ( ) )","( ) ( ( ( ) ) )"]
	reject_strings = ["(", ")", "( ( )"]

	config = {
		'num_rules': 2, #Number of rules
		'size_rules' : 4, #Number of symbols in RHS
		'num_nonterms' : 1, #Number of nonterms
		'expansion_constant' : 5, #Determines the max. number of parse actions to take while parsing
		'optimize' : True, # enable optimized mode
		'neg_egs' : True, # consider negative examples 
		'threshold' : 0.5,  # number of unsat cores to break
		'Use_CFGAnalyzer' : False, # use cfganalyzer
		'orig_grammar_link' : "orig_3.txt", # link to the original grammar 
		'eps_given' : False, # if eps is given for the grammar
		'eps_given_link' : 'eps_given/3.txt', # Where are the eps slots given
		'name':'3.txt'
	}

	return accept_strings,reject_strings,config


# S	: "(" S ")" S
# 	| ;
#()()()()(); ()()()()()(); ()()()()()()()

 
