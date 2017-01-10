from input_specs import *

def discover_tokens(strings):
	tokens = []
	for s in strings:
		l = s.split(' ')
		for t in l:
			if t not in tokens:
				tokens.append(t)
	print('tokens',tokens)
	

	return tokens

def list_from_strings(in_strings):
	in_terms = [in_strings[i].split(' ') for i in range(len(in_strings))]
	return [["t%s"%(tokens.index(i)+1) for i in in_terms[j]] for j in range(len(in_terms))]

######################################################

# SYNTHESIZER SPECS

######################################################

accept_strings,reject_strings,config = specs()

######################################################

# PROCESS STRINGS

######################################################

tokens = discover_tokens(accept_strings)
config.update({'num_terms':len(tokens)})
assert(config['size_rules']>=2)

accept_list = list_from_strings(accept_strings)
reject_list = list_from_strings(reject_strings)
