# from 'game_src/game/views' import * 
from collections import *
def specs():

	#Space separated (tokenized) strings
	accept_strings = ["?", "! ?", "( ? ) ?"]
	reject_strings = [")", ") ("]

	config = {
		'num_rules': 6, #Number of rules
		'size_rules' : 4, #Number of symbols in RHS
		'num_nonterms' : 4, #Number of nonterms
		'expansion_constant' : 6, #Determines the max. number of parse actions to take while parsing
		'optimize' : False, # enable optimized mode
		'neg_egs' : True, # consider negative examples 
		'threshold' : 0.2  # number of unsat cores to break
	}

	return accept_strings,reject_strings,config

def find_original_grammar():
	original_grammar = [['S','eps','eps','F','S'], ['S','eps','eps','eps','Q'], ['S','(','S',')','S'], ['F','eps','eps','!','A'], ['Q','eps','eps','?','A'],['A','eps','eps','eps','eps']]
	# return get_original_grammar()
	return original_grammar

def get_parse_table():
	parse_table = [{'non_term':'S' ,'(':3 ,')':0 ,'!':1 ,'?':2 ,'$':0},{'non_term':'F' ,'(':0 ,')':0 ,'!':4 ,'?':0 ,'$':0},{'non_term':'Q' ,'(':0 ,')':0 ,'!':0 ,'?':5 ,'$':0},{'non_term':'A' ,'(':6 ,')':6 ,'!':6 ,'?':6 ,'$':6}]
	return parse_table

def nums():
	original_grammar = find_original_grammar()
	num_vars = {'num_rules':len(original_grammar), 'size_rules':len(original_grammar[0])-1}
	return num_vars

def get_first_set():
	first_set = [{'non_term':'S' ,'(':1 ,')':0 ,'!':1 ,'?':1 ,'eps':0},{'non_term':'F' ,'(':0 ,')':0 ,'!':1 ,'?':0 ,'eps':0},{'non_term':'Q' ,'(':0 ,')':0 ,'!':0 ,'?':1 ,'eps':0},{'non_term':'A' ,'(':0 ,')':0 ,'!':0 ,'?':0 ,'eps':1}]
	return first_set

def get_follow_set():
	follow_set = [{'non_term':'S' ,'(':0 ,')':1 ,'!':0 ,'?':0 ,'$':1},{'non_term':'F' ,'(':1 ,')':0 ,'!':1 ,'?':1 ,'$':0},{'non_term':'Q' ,'(':0 ,')':1 ,'!':0 ,'?':0 ,'$':1},{'non_term':'A' ,'(':1 ,')':1 ,'!':1 ,'?':1 ,'$':1}]
	return follow_set

accept_strings = ["?", "! ?", "( ? ) ?"]
reject_strings = [")", ") ("]

##	S -> (S)S | eps
##

