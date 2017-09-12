import random
import pickle
import sys
import numpy as np
def flip():
	x = np.random.multinomial(1,[0.5, 0.5])
	if x[0] == 1:
		return 1
	else:
		return 1
	if x[1] == 1:
		return 1
	if x[2] == 1:
		return 2
def er_gen(data):
	delete = False
	global err_examples
	global counter
	string = data
	print "string:",string
	print len(string)
	ex = []
	# string = string.split()	
	tmp = []
	for i in range(len(string)):
		if i not in er_index:
			ex.append(string[i])
			flag = 10
		else:
			flag = flip()
		if flag == 10:
			continue
		else:
			if flag == 0: # replace
				print "replacement done..."
				k = random.randint(0,len(terminals)-1)
				print "i:",i
				ex.append(terminals[k])
				if delete == True:
					string[i-2] = terminals[k]
				else:
					string[i] = terminals[k]
				tmp.append(i)
				counter.append(i)
			if flag == 1: # insert
				print "insertion done..."
				k = random.randint(0, len(terminals)-1)
				ex.append(terminals[k])
				ex.append(string[i])
				counter.append(i-1)
			if flag == 2: # delete
				# k = random.randint(0, len(terminals)-1)
				if delete == True:
					print "deletion done at %d"%(i-2)
					# string.remove(string[i-1])
					counter.append(i-2)
				else:
					print "deletin done at %d"%(i-1)
					# string.remove(string[i])
					counter.append(i-1)
				delete = True
	err_examples.append(ex)


N = 2
err_examples = []
er_index_counter = []
terminals = ['|', '&', '+', '-', '*', '/', 'nil', 'integer', 'string', '(', ')', 'if', 'then', 'else', 'while', 'do', 'for', 'id', ':=', 'to', 'break', 'let', 'in', 'end', 'type', '=', '{', '}', 'array', 'of', ':', ',', 'var', 'function', '[', ']', '.', ';', '!=', '>', '<', '>=', '<=']
for i in range(1,50):
	for j in range(5):
		counter = []
		er_index = []
		n_error_done=0
		data = []
		input_file = open("Examples/Processed/test%d_lex.tig"%i)
		data = input_file.read()
		data = data.split()
		input_file.close()
		f = len(data)-3
		if f < 5:
			f = len(data)-1
			continue
		tmp = random.randint(2,f)
		while tmp == 0:
			tmp = random.randint(1,f)
		er_index.append(tmp)
		tmp = random.randint(1,f)
		while tmp == er_index[0]:
			tmp = random.randint(1,f)
		#er_index.append(tmp)
		#er_index_counter.append(sorted(counter))
		#er_index_counter.append(sorted([er_index[0],er_index[1]]))
		er_gen(data)
		er_index = sorted(er_index)
		counter = sorted(counter)
		#if abs(counter[0]-er_index[0]) > 2 or abs(er_index[1]-counter[1]) > 2:
		#	print "er_index:",er_index
		#	print "counter:",counter
		#	print "ERROR...."
		#	break
		er_index_counter.append(sorted(counter))

output_file = open("ErrorTestExamples.pkl","wb")
pickle.dump(err_examples, output_file)
output_file.close()
output_file = open("ErrorTestCounter.pkl","wb")
pickle.dump(er_index_counter, output_file)
output_file.close()
print er_index_counter
