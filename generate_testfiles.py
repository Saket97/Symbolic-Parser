import random
import pickle
import sys
import numpy as np
def flip():
	x = np.random.multinomial(1,[0.5, 0.5])
	if x[0] == 1:
		return 0
	else:
		return 2
	# if x[1] == 1:
	# 	return 1
	# if x[2] == 1:
	# 	return 2
def er_gen(data):
	delete = False
	global err_examples
	string = data
	print "string:",string
	print len(string)
	# string = string.split()	
	tmp = []
	for i in range(len(string)):
		if i not in er_index:
			flag = 10
		else:
			flag = flip()
		if flag == 10:
			continue
		else:
			if flag == 0: # replace
				k = random.randint(0,len(terminals)-1)
				print "i:",i
				if delete == True:
					string[i-2] = terminals[k]
				else:
					string[i] = terminals[k]
				tmp.append(i)
			if flag == 1: # insert
				k = random.randint(0, len(terminals)-1)
				string.insert(i, terminals[k])
			if flag == 2: # delete
				# k = random.randint(0, len(terminals)-1)
				if delete == True:
					string.remove(string[i-1])
				else:
					string.remove(string[i])
				delete = True
	err_examples.append(string)


N = 2
err_examples = []
# er_index = []
terminals = ['|', 'eps', '&', '+', '-', '*', '/', 'nil', 'integer', 'string', '(', ')', 'if', 'then', 'else', 'while', 'do', 'for', 'id', ':=', 'to', 'break', 'let', 'in', 'end', 'type', '=', '{', '}', 'array', 'of', ':', ',', 'var', 'function', '[', ']', '.', ';', '!=', '>', '<', '>=', '<=']
for i in range(1,50):
	for j in range(5):
		er_index = []
		n_error_done=0
		data = []
		input_file = open("Examples/Processed/test%d_lex.tig"%i)
		data = input_file.read()
		data = data.split()
		input_file.close()
		er_index.append(random.randint(0,len(data)-1))
		er_index.append(random.randint(0,len(data)-1))
		er_gen(data)

output_file = open("ErrorTestExamples.pkl","wb")
pickle.dump(err_examples, output_file)
