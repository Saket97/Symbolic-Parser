from finalTestFilesOOPSLA.input_specs_tiger0 import *
import sys

def discover(original_grammar):
	non_tokens = []
	for string in original_grammar:
		ch = string[0]
		if ch not in non_tokens:
			non_tokens.append(ch)
		else:
			pass
	print "len(non_tokens):",len(non_tokens)
	return non_tokens
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

def list_from_strings(in_strings):
	in_terms = [in_strings[i].split() for i in range(len(in_strings))]
	return [["t%s"%(tokens.index(i)+1) for i in in_terms[j]] for j in range(len(in_terms))]

######################################################

# SYNTHESIZER SPECS

######################################################

accept_strings,reject_strings,config = specs()

######################################################

# PROCESS STRINGS

######################################################

if  True or sys.argv[1] == 'mode2':
	non_tokens = discover(find_original_grammar())
	tokens = discover_tokens_from_grammar()
	tokens.remove('dol')
else:
	tokens = discover_tokens(accept_strings)
	
# tokens = discover_tokens(accept_strings)
config.update({'num_terms':len(tokens)})
assert(config['size_rules']>=2)

accept_list = list_from_strings(accept_strings)
reject_list = list_from_strings(reject_strings)
