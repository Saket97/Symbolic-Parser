import pickle
START = 0
END = 97
pkl_file = open("ErrorTestExamples.pkl", "rb")
examples = pickle.load(pkl_file)
pkl_file.close()
pkl_file= open("ErrorTestCounter.pkl","rb")
examples_counter = pickle.load(pkl_file)
assert(len(examples) == len(examples_counter))
pkl_file.close()
string = ""
for i in range(len(examples)):
	string = ""
	for j in range(len(examples[i])):
		string += examples[i][j]
		if j != len(examples[i])-1:
			string += " "
	input_file = open("input_specs_tiger.py")
	output_file = open("finalTestFilesOOPSLA/input_specs_tiger%d.py"%i, "w")
	j = 0
	for line in input_file:
		if j == 4:
			output_file.write("#accept_strings= ")
			lf = open("Examples/Processed/test%d_lex.tig"%(i/5+1))
			l = lf.readlines()
			for term in l:
				term = term.split()
				output_file.write(term[0])
				output_file.write(" ")
			output_file.write("\n")
			j+=1
			continue

		if j == 5:
			output_file.write("	accept_strings = [' ")
			for word in string:
				output_file.write(word)
			output_file.write(" ']")
			output_file.write("\n")
		else:
			output_file.write(line)
		j += 1
	output_file.write("""def find_test_counter():
	return [%d]"""%(examples_counter[i][0]))
