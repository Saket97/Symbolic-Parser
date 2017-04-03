import pickle
import random
def flip():
	p = random.random()
	if p < 0.7:
		return 1
	else:
		return 0
def find_ngrams(string, n, table):
	# string = string.split(" ")
	tmp1 = []
	# # print "String: ",string
	# for s in string:
	# 	if s == " " or s == "\n" or s == '\t':
	# 		continue
	# 	tmp1.append(s)
	string = string.split()
	print "string after processing: ",string
	tmp = []
	for j in range(n):
		# if string[j] == " " or string[j] == "\n" or string[j] == '\t':
			# continue
		tmp.append(string[j])
	table[tuple(tmp)] = 1
	for i in range(1,len(string)-n+1):
		tmp.pop(0)
		tmp.append(string[i+n-1])
		if tuple(tmp) in table:
			table[tuple(tmp)] += 1
		else:
			table[tuple(tmp)] = 1
	return table
pkl_file = open("tigerExamplesList1.pkl", "rb")
output = pickle.load(pkl_file)
pkl_file.close()
pkl_file = open("tigerTableUpdated.pkl","rb")
table = pickle.load(pkl_file)
pkl_file.close()

# for i in range(1,50):
# 	data = []
# 	input_file = open("Examples/Processed/test%d_lex.tig"%i)
# 	data = input_file.read()
# 	data = data.split()
# 	input_file.close()
# 	if flip():
# 		find_ngrams(data, 2, table)
for string in output:
    if len(string.split()) >= 3:
        find_ngrams(string, 2, table)
for key in table:
	print "%s   				:    %d"%(key, table[key])
output_file = open("tigerTableUpdated.pkl", "wb")
pickle.dump(table, output_file)
output_file.close()
print "#ngrams:",len(table)
