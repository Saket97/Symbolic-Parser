# from 'game_src/game/views' import * 
from collections import *
def specs():

	#Space separated (tokenized) strings
	accept_strings = ["a b", "b a","b c a b a"]
	reject_strings = ["a b b","c a","c b"]

	config = {
		'num_rules': 4, #Number of rules
		'size_rules' : 3, #Number of symbols in RHS
		'num_nonterms' : 2, #Number of nonterms
		'expansion_constant' : 7, #Determines the max. number of parse actions to take while parsing
		'optimize' : False, # enable optimized mode
		'neg_egs' : True, # consider negative examples 
		'threshold' : 0.2  # number of unsat cores to break
	}

	return accept_strings,reject_strings,config

def find_original_grammar():
	original_grammar = [['S','a','A','b'], ['S','b','A','a'],['A','eps','c','S'],['A','eps','eps','eps']]
	# return get_original_grammar()
	return original_grammar

def get_parse_table():
	parse_table = [{'non_term':'S' ,'a':1 ,'b':2 ,'c':0 ,'$':0}, {'non_term':'A' ,'a':4 ,'b':4 ,'c':3 ,'$':0}]
	return parse_table

def nums():
	original_grammar = find_original_grammar()
	num_vars = {'num_rules':len(original_grammar), 'size_rules':len(original_grammar[0])-1}
	return num_vars

def get_first_set():
	first_set = [{'non_term':'S' ,'a':1 ,'b':1 ,'c':0 ,'eps':0 },{'non_term':'A' ,'a':0 ,'b':0 ,'c':1 ,'eps':1 }]
	return first_set

def get_follow_set():
	follow_set = [{'non_term':'S' ,'a':1 ,'b':1 ,'c':0 ,'$':1},{'non_term':'A' ,'a':1 ,'b':1 ,'c':0 ,'$':0}]
	return follow_set

accept_strings = ["a b", "b a","b c a b a"]
reject_strings = ["a b b","c a","c b"]

# S -> a A b
# S -> b A a
# A -> c S
# A -> eps
