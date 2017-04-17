import pickle
def write_to(example,output_file):

	input_file = open("input_specs_tiger.py","r")
	lines = input_file.readlines()
	for j in range(len(lines)):
		if j == 5:
			output_file.write("""	accept_strings = [""")
			for i in range(len(example)):
				if i != len(example)-1:
					output_file.write("'%s',"%example[i])
				else:
					output_file.write("'%s'"%example[i])
			output_file.write("]\n")

		else:
			output_file.write(lines[j])

pkl_file = open("ErrorTestExamples.pkl","rb")
examples = pickle.load(pkl_file)
for i in range(len(examples)):
	print "writing file %d"%i
	output_file = open("finalTestFilesOOPSLA/input_specs_tiger%d.py"%i,'w+')
	write_to(examples[i],output_file)