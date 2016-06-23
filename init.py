from input_specs7 import *
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

def list_from_strings(in_strings):
	in_terms = [in_strings[i].split(' ') for i in range(len(in_strings))]
	accept_list = []
	for j in range(len(in_terms)):
		tmp = []
		for i in in_terms[j]:
			if i not in tokens:
				print "This string is not accepted."
				global to_proceed

				to_proceed = False
				print "to_proceed: ",to_proceed
				return
				print "saket"
			tmp.append("t%s"%(tokens.index(i)+1))
		accept_list.append(tmp)
	return accept_list

	# return [["t%s"%(tokens.index(i)+1) for i in in_terms[j]] for j in range(len(in_terms))]

######################################################

# SYNTHESIZER SPECS

######################################################

accept_strings,reject_strings,config = specs()

######################################################

# PROCESS STRINGS

######################################################
def verify():
	string = "s a k e t"
	global accept_strings
	accept_strings.append(string)

# verify()
non_tokens = discover(find_original_grammar())
tokens = discover_tokens_from_grammar()
config.update({'num_terms':len(tokens)})
assert(config['size_rules']>=2)
# verify()
to_proceed = True
accept_list = list_from_strings(accept_strings)
reject_list = list_from_strings(reject_strings)
print "Accept_list",accept_list
print "type accept_list", type(accept_list)
