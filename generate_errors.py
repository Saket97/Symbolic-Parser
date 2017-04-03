import random
import pickle
def flip():
	if random.random() < 0.05:
		return 1
	else:
		return 0

def er_gen():
	global err_examples
	global error_counter
	for i in range(len(examples)):
		string = examples[i]
		# string = string.split()	
		tmp = []
		for i in range(len(string)):
			flag = flip()
			if flag == 0:
				continue
			else:
				k = random.randint(0,len(terminals)-1)
				string[i] = terminals[k]
				tmp.append(i)
		error_counter.append(tmp)
		err_examples.append(string)

def find_errors():
	test_counter = []
	for string in err_examples:
		# string = string.split()
		tmp = []
		for i in range(len(string)):
			if i != 0:
				t1 = (string[i-1],string[i])
				if t1 not in ngrams:
					print t1
					print "Bigram not present..."
					tmp.append(i)
					continue
				f1 = ngrams[t1]
				# print "freq: ",f1
				if f1 < 5:
					print t1
					print "freq: ",f1
					tmp.append(i)
			if i != len(string)-1:
				t1 = (string[i],string[i+1])
				if t1 not in ngrams:
					print t1
					print "Bigram not present..."
					tmp.append(i)
					continue
				f1 = ngrams[t1]
				# print "freq: ",f1
				if f1 < 5:
					print t1
					print "freq: ",f1
					tmp.append(i)

		test_counter.append(tmp)
	return test_counter

def evaluate(error_counter, test_counter):
	flag = []
	t = 0
	assert(len(error_counter) == len(test_counter))
	for i in range(len(test_counter)):
		flag.append(set(error_counter[i]) <= set(test_counter[i]))
		print ("actual is subset of predicted: %s len(string):%d len(error):%d len(predicted):%d"%(flag[i],len(err_examples[i]),len(error_counter[i]),len(test_counter[i])))
		if flag[i] == True:
			t += 1
		else:
			print (set(error_counter[i])-set(test_counter[i]))
	print ("total correct: %d"%t)

N = 2
percent = 20
pkl_file = open("ErrorTestExamples.pkl","rb")
examples = pickle.load(pkl_file)
err_examples = []
pkl_file.close()
pkl_file = open("tigerTableUpdated.pkl","rb")
ngrams = pickle.load(pkl_file)
pkl_file.close()
error_counter = []
terminals = ['|', 'eps', '&', '+', '-', '*', '/', 'nil', 'integer', 'string', '(', ')', 'if', 'then', 'else', 'while', 'do', 'for', 'id', ':=', 'to', 'break', 'let', 'in', 'end', 'type', '=', '{', '}', 'array', 'of', ':', ',', 'var', 'function', '[', ']', '.', ';', '!=', '>', '<', '>=', '<=']
# er_gen()
err_examples = examples
test_counter = find_errors()
# evaluate(error_counter, test_counter)
for i in range(len(test_counter)):
	print "%d. %d %d"%(i,len(test_counter[i]), len(err_examples[i]))
