# from 'game_src/game/views' import * 
from collections import *
def specs():

	#Space separated (tokenized) strings
	accept_strings = ["int", "( int )", "int + int", "int * int"]
	reject_strings = [")", "+ int"]

	config = {
		'num_rules': 7, #Number of rules
		'size_rules' : 3, #Number of symbols in RHS
		'num_nonterms' : 4, #Number of nonterms
		'expansion_constant' : 6, #Determines the max. number of parse actions to take while parsing
		'optimize' : False, # enable optimized mode
		'neg_egs' : True, # consider negative examples 
		'threshold' : 0.2  # number of unsat cores to break
	}

	return accept_strings,reject_strings,config

def find_original_grammar():
	original_grammar = [['E','eps','T','X'],['T','(','E',')'], ['T','eps','int','Y'], ['X','eps','+','E'], ['X','eps','eps','eps'], ['Y','eps','*','T'], ['Y','eps','eps','eps']]
	# return get_original_grammar()
	return original_grammar

def get_parse_table():
	parse_table = [{'non_term':'E' ,'(':1 ,')':0 ,'int':1 ,'+':0 ,'*':0 ,'$':0  }, {'non_term':'T' ,'(':2 ,')':0 ,'int':3 ,'+':0 ,'*':0 ,'$': 0 },{'non_term':'X' ,'(': 0,')':5 ,'int':0 ,'+': 4,'*':0 ,'$':5  },{'non_term':'Y' ,'(':0 ,')':7 ,'int':0 ,'+':7 ,'*':6 ,'$':7 }]
	return parse_table

def nums():
	original_grammar = find_original_grammar()
	num_vars = {'num_rules':len(original_grammar), 'size_rules':len(original_grammar[0])-1}
	return num_vars

def get_first_set():
	first_set = [{'non_term':'E' ,'(':1 ,'int':1 ,')':0 ,'*':0 ,'+':0 ,'eps':0 }, {'non_term':'X' ,'(':0 ,'int':0 ,')':0 ,'*':0 ,'+':1 ,'eps':1 }, {'non_term':'Y' ,'(':0 ,'int':0 ,')':0 ,'*':1 ,'+':0 ,'eps':1 }, {'non_term':'T' ,'(':1 ,'int':1 ,')':0 ,'*':0 ,'+':0 ,'eps':0 }]
	return first_set

def get_follow_set():
	follow_set = [{'non_term':'E' ,'(':0 ,')':1 ,'int':0 ,'+':0 ,'*':0 ,'$':1},{'non_term':'X' ,'(':0 ,')':1 ,'int':0 ,'+':0 ,'*':0 ,'$':1},{'non_term':'Y' ,'(':0 ,')':1 ,'int':0 ,'+':1 ,'*':0 ,'$':1},{'non_term':'T' ,'(':0 ,')':1 ,'int':0 ,'+':1 ,'*':0 ,'$':1}]
	return follow_set

accept_strings = ["int", "( int )", "int + int", "int * int"]
reject_strings = [") ", "+ int"]
##	S -> (S)S | eps
##
