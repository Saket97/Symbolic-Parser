from collections import *

def specs():

	#Space separated (tokenized) strings
	accept_strings = ["a","a b","a b c","a b c a"]
	reject_strings = ["a c","b","c","a c b"]

	config = {
		'num_rules': 6, #Number of rules
		'size_rules' : 2, #Number of symbols in RHS
		'num_nonterms' : 3, #Number of nonterms
		'expansion_constant' : 6, #Determines the max. number of parse actions to take while parsing
		'optimize' : False, # enable optimized mode
		'neg_egs' : False, # consider negative examples 
		'threshold' : 1,  # number of unsat cores to break
		'num_terms' : 3
	}

	return accept_strings,reject_strings,config



def find_original_grammar():
	original_grammar = [['S', 'a', 'B'], ['S', 'eps', 'eps'], ['B', 'b', 'C'], ['B', 'eps', 'eps'], ['C', 'c', 'S'], ['C', 'eps', 'eps']]
	# return get_original_grammar()
	return original_grammar
def nums():
	num_vars = {'num_rules':6, 'size_rules':2}
	return num_vars
def get_parse_table():
	# parse_table = {'S':{'a': 2, 'b':0, 'c':0 , 'dol':2}, 'B':{'a':0 , 'b':3 , 'c':0 ,'dol':4}, 'C':{'a':0 , 'b':0 , 'c': 5, 'dol':6}}
	parse_table = [{'non_term':'S','a':2,'b':0 ,'c':0, 'dol':2}, {'non_term':'B', 'a':0, 'b':3, 'c':0, 'dol':4}, {'non_term':'C', 'a':0, 'b':0, 'c':5, 'dol':6}]
	return parse_table
	
# config = specs()
# tokens = ['a', 'b', 'c']

accept_strings = ["a","a b","a b c","a b c a"]
reject_strings = ["a c","b","c","a c b"]
# S-> aB
# S-> eps
# B-> bC
# B-> eps
# C-> cS
# C-> eps
