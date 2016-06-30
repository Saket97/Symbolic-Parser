from input_specs8 import *
from z3 import *
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

def list_from_strings(in_strings, solver):
	s = solver["constraints"]
	vars = solver["vars"]
	in_terms = [in_strings[i].split(' ') for i in range(len(in_strings))]
	#### in_terms consist of the list of strings in this way [['s','a','k','e','t'],['c','s','e']]
	#### doubling the length of the string 
	tmp = []
	for string in in_terms:
		tmp1 = []
		for i in range(len(string)):
			tmp1.append(string[i])
			tmp1.append('t1000')
		tmp.append(tmp1)
	in_terms = tmp
	print "in_terms: ",in_terms
	
	accept_list = []
	for j in range(len(in_terms)):
		# tmp = []
		tmp1 = []		
		for i in range(len(in_terms[j])):
			tmp1.append('a%d_%d'%(j,i))
			vars['a%d_%d'%(j,i)] = Int('a%d_%d'%(j,i))
		accept_list.append(tmp1)
		
		for i in range(len(in_terms[j])):
			if in_terms[j][i] == 't1000':
				s.assert_and_track(vars['a%d_%d'%(j,i)] == vars["t1000"], 'adding_terminal_at_%d_to_str_%d'%(i,j))
				continue

			if in_terms[j][i] not in tokens:
				print "this string is not accepted."
				global to_proceed
				to_proceed = False
				return
			s.assert_and_track(vars['a%d_%d'%(j,i)] == vars["t%s"%(tokens.index(in_terms[j][i])+1)], 'adding_terminal_at_%d_to_str_%d'%(i,j))
	
	return accept_list

	# return [["t%s"%(tokens.index(i)+1) for i in in_terms[j]] for j in range(len(in_terms))]

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

def list_from_strings2(in_strings):
	in_terms = [in_strings[i].split(' ') for i in range(len(in_strings))]
	tmp = []
	# print "in_terms: ",in_terms
	for string in in_terms:
		# tmp1 = []
		for j in range(len(string)):
			# if j == 0:
			# 	tmp1.append("t1000")
			# 	tmp1.append("t2")
			tmp1.append("t%s"%(tokens.index(string[j])+1))
			tmp1.append('t1000')
		tmp.append(tmp1)
	return tmp

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
reject_list = list_from_strings1(reject_strings)
accept_list = list_from_strings1(accept_strings)
# reject_list = list_from_strings(reject_strings)
# print "Accept_list",accept_list
# print "type accept_list", type(accept_list)

