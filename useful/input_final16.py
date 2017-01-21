def specs():

	#Space separated (tokenized) strings
	accept_strings = ["a", "b", "a b", "a a", "b a", "a a b", "a b a", "a a a", "b a a", "a a b a", "a a a b", "a b a a", "a a a a", "b a a a", "b a a a a", "a b a a a", "a a b a a", "a a a b a", "a a a a b"]
	reject_strings = ["b b", "b a b", "b b a", "a b b"]

	config = {
		'num_rules': 5, #Number of rules
		'size_rules' : 2, #Number of symbols in RHS
		'num_nonterms' : 3, #Number of nonterms
		'expansion_constant' : 5, #Determines the max. number of parse actions to take while parsing
		'optimize' : True, # enable optimized mode
		'neg_egs' : True, # consider negative examples 
		'threshold' : 0.25,  # number of unsat cores to break
		'Use_CFGAnalyzer' : False, # use cfganalyzer
		'orig_grammar_link' : "orig_16.txt", # link to the original grammar 
		'eps_given' : False, # if eps is given for the grammar
		'eps_given_link' : 'eps_given/16.txt', # Where are the eps slots given
		'name':'16.txt'
	}

	return accept_strings,reject_strings,config

# S : A B ;
# A : "a" A ;
#   : ;
# B : "b" A ;
#   : ;
#aaaaaaaa; aaaaaaaaa; aaaaaaaaaaa; aaaaaaaaaaaaa; aaaaaaaaaaaaaaa
