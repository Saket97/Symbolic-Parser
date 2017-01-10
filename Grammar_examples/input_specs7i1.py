# from 'game_src/game/views' import * 
from collections import *
def specs():

	#Space separated (tokenized) strings
	accept_strings = ["b a", "b a c a", "b d a"]
	reject_strings = ["b c"]

	config = {
		'num_rules': 5, #Number of rules
		'size_rules' : 4, #Number of symbols in RHS
		'num_nonterms' : 3, #Number of nonterms
		'expansion_constant' : 6, #Determines the max. number of parse actions to take while parsing
		'optimize' : False, # enable optimized mode
		'neg_egs' : True, # consider negative examples 
		'threshold' : 0.2  # number of unsat cores to break
	}

	return accept_strings,reject_strings,config

def find_original_grammar():

	original_grammar = [['S','eps','b','A','a'], ['A','eps','a','A','c'], ['A','eps','eps','eps','d'], ['B','eps','eps','b','B'],['A','eps','eps','eps','eps']]
	# return get_original_grammar()
	return original_grammar

def get_parse_table():
	parse_table = [{'non_term':'S' ,'a':0 ,'b':1 ,'c': 0,'d':0 ,'$':0 },{'non_term':'A' ,'a':2 ,'b':0 ,'c':5 ,'d':3 ,'$':0 },{'non_term':'B' ,'a':0 ,'b':4 ,'c':0 ,'d':0 ,'$':0 }]
	return parse_table

def nums():
	original_grammar = find_original_grammar()
	num_vars = {'num_rules':len(original_grammar), 'size_rules':len(original_grammar[0])-1}
	return num_vars

def get_first_set():
	first_set = [{'non_term':'S' ,'a':0 ,'b':1 ,'c':0 ,'d':0 ,'eps':0},{'non_term':'A' ,'a':1 ,'b':0 ,'c': 0,'d':1 ,'eps':1},{'non_term':'B' ,'a':0 ,'b':1 ,'c':0 ,'d':0 ,'eps':0}]
	return first_set

def get_follow_set():
	follow_set = [{'non_term':'S' ,'a':0 ,'b':0 ,'c':0 ,'d':0 ,'$':1},{'non_term':'A' ,'a':1 ,'b':0 ,'c':1 ,'d':0 ,'$':0},{'non_term':'B' ,'a':0 ,'b':0 ,'c':0 ,'d':0 ,'$':0}]
	return follow_set

accept_strings = ["b a","b a c a", "b d a"]
reject_strings = ["b c", "c d"]
##	S -> (S)S | eps
##
