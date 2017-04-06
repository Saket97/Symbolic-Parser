from input_specs_tiger import *

def discover_non_tokens():
	tmp = []
	for rule in original_grammar:
		if rule[0] not in tmp:
			tmp.append(rule[0])
	return tmp

def discover_tokens():
	tmp = []
	for rule in original_grammar:
		for t in rule:
			if t not in non_terms:
				if t not in tmp:
					tmp.append(t)
	return tmp

def write_input():
	hardcode = []
	input_file = open("hardcode.txt", "w+")
	for i in range(len(original_grammar)):
		string = ',And (rn == vars["rule%d"],'%(i+1)
		input_file.write(',And (rn == vars["rule%d"],'%(i+1))
		string += 'functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, '
		input_file.write( 'functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, ')
		for j in range(len(original_grammar[i])):
			if j == 0:
				string += 'functions["symbolAt"](strNum, X%d) == vars[view_assign["%s"]], X1 == X0+1, '%(0,original_grammar[i][j])
				input_file.write( 'functions["symbolAt"](strNum, X%d) == vars[view_assign["%s"]], X1 == X0+1, '%(0,original_grammar[i][j]))
				continue
			if original_grammar[i][j] == "eps":
				string += "X%d == X%d "%(j,j+1)
				input_file.write("X%d == X%d "%(j,j+1))
				if j != 5:
					string += ','
					input_file.write( ',')
			else:
				if original_grammar[i][j] in term:
					string += 'X%d == X%d+1, functions["end"](strNum, X%d) == X%d, functions["symbolAt"](strNum, X%d) == vars[view_assign["%s"]] '%(j+1,j,j,j+1,j,original_grammar[i][j])
					input_file.write( 'X%d == X%d+1, functions["end"](strNum, X%d) == X%d, functions["symbolAt"](strNum, X%d) == vars[view_assign["%s"]] '%(j+1,j,j,j+1,j,original_grammar[i][j]))
					if j != 5:
						string += ','
						input_file.write( ',')
				else:
					string += 'functions["end"](strNum, X%d) == X%d, functions["symbolAt"](strNum, X%d) == vars[view_assign[%s]] '%(j, j+1, j, original_grammar[i][j])
					input_file.write('functions["end"](strNum, X%d) == X%d, functions["symbolAt"](strNum, X%d) == vars[view_assign["%s"]] '%(j, j+1, j, original_grammar[i][j]))
					if j != 5:
						string += ','
						input_file.write( ',')
		string += ')'
		input_file.write( ')')
		hardcode.append(string)
	return hardcode

original_grammar = find_original_grammar(eps=True)
non_terms = discover_non_tokens()
term = discover_tokens()
hardcode = write_input()
h = []
for constraint in hardcode:
	p = constraint[0:len(constraint)-3]
	p += ')'
	h.append(p)
# print h