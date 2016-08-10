from input_specs8 import *
from z3 import *
import sys
# from test import discover_tokens_from_grammar
def discover_tokens(strings):
	tokens = []
	for s in strings:
		l = s.split(' ')
		for t in l:
			if t not in tokens:
				tokens.append(t)
	print('tokens',tokens)
	return tokens

def discover_tokens_from_grammar():
	tokens = []
	original_grammar = find_original_grammar()
	for string in original_grammar:
		for i in range(1,len(string)):
			if string[i] in non_tokens or string[i] == "eps":
				pass
			else:
				if string[i] in tokens:
					pass
				else:
					tokens.append(string[i])
	print ('tokens',tokens)
	return tokens

def discover(original_grammar):
	non_tokens = []
	for string in original_grammar:
		ch = string[0]
		if ch not in non_tokens:
			non_tokens.append(ch)
		else:
			pass
	return non_tokens


######################################################

# SYNTHESIZER SPECS

######################################################

accept_strings,reject_strings,config = specs()

######################################################

# PROCESS STRINGS

######################################################
def list_from_strings1(in_strings):
	in_terms = [in_strings[i].split(' ') for i in range(len(in_strings))]
	return [["t%s"%(tokens.index(i)+1) for i in in_terms[j]] for j in range(len(in_terms))]

if sys.argv[1] == 'mode2' or True:
	non_tokens = discover(find_original_grammar())
	tokens = discover_tokens_from_grammar()
else:
	tokens = discover_tokens(accept_strings)

config.update({'num_terms':len(tokens)})
assert(config['size_rules']>=2)
reject_list = list_from_strings1(reject_strings)
accept_list = list_from_strings1(accept_strings)

