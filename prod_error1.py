import random
import sys
# from useful.input_final11 import *
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

def discover_tokens_from_grammar(original_grammar):
	tokens = []
	# original_grammar = [['S','f','E','t','S','a','S'],['S','w','E','d','S'],['S','b','S1','e'],['S1','S','c','S1'],['S1','eps'],['E','i']]
	non_tokens = discover(original_grammar)
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

def produce_error(accept_sttring, grammar, delete=False):
	input_string = accept_sttring
	input_string = input_string.split(' ')
	print "input_string: ",input_string
	# grammar = find_original_grammar()
	nerrors = 0

	terminals = discover_tokens_from_grammar(grammar)
	n1 = random.randint(0,len(terminals)-1)
	n4 = random.randint(0,len(terminals)-1)
	while n4 == n1:
		n4 = random.randint(0,len(terminals)-1)
	n2 = random.randint(0,len(input_string)-1)
	n3 = random.randint(0,len(input_string)-1)
	while n3 == n2:
		n3 = random.randint(0,len(input_string)-1)
	print "############# mutation ################\n strpos:%d"%n2
	if delete == False:
	# 	input_string[n2] = terminals[n1]
		input_string[n3] = terminals[n4]
	# a = input_string[0]
	a = ""
	j = 0
	for i in range(0,len(input_string)):
		if delete == True and (i == n2):
			if i == n2:
				r = n1
			else:
				r = n4
			if len(a) == 0:
				a = a + "%s"%terminals[r]
			else:
				a = a + " %s"%terminals[r]
			continue
		if i == n2:
			j += 1
			continue
		if len(a) == 0:
			a = a + "%s"%input_string[j]
		else:
			a = a + " %s"%input_string[j]
		j += 1
	return a