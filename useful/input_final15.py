def specs():

	#Space separated (tokenized) strings
	accept_strings = ["e", "b e", "b b e", "a b e", "b a b e", "a b b e", "b b b e", "a a b e", "b a a b e", "a b a b e", "a b b b e", "a a b b e", "b a b b e", "a a a b e", "b b a b e", "a a a b b e", "a a a a b e", "a a b a b e", "a b a a b e", "b a a a b e"]
	reject_strings = ["a", "b", "a b", "a e", "a a", "b b", "b a", "e a", "e b", "e e"]

	config = {
		'num_rules': 4, #Number of rules
		'size_rules' : 2, #Number of symbols in RHS
		'num_nonterms' : 2, #Number of nonterms
		'expansion_constant' : 5, #Determines the max. number of parse actions to take while parsing
		'optimize' : True, # enable optimized mode
		'neg_egs' : True, # consider negative examples 
		'threshold' : 0.25,  # number of unsat cores to break
		'Use_CFGAnalyzer' : False, # use cfganalyzer
		'orig_grammar_link' : "orig_15.txt", # link to the original grammar 
		'eps_given' : False, # if eps is given for the grammar
		'eps_given_link' : 'eps_given/15.txt', # Where are the eps slots given
		'name':'15.txt'
	}

	return accept_strings,reject_strings,config

# S :  A S ;
#   : "e" ;
# A :  "a" A ;
#   : "b" ;
#bbbbbbbbbe; bbbbbbbbbbe; bbbbbbbbbbbe; bbbbbbbbbbbbe; bbbbbbbbbbbbbe; #bbbbbbbbbbbbbbe


