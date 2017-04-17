import subprocess
import pickle
#tmp = [11,12,17,18,20,21,22]
START = 0
End = 9
for j in range(1):	
	for i in range(START, END+1):
		init = open("init.py", "r+")
		test = open("test.py", "r+")
		parser = open("parser.py", "r+")
		init.write("from finalTestFilesOOPSLA.input_specs_tiger%d"%i)
		test.write("from finalTestFilesOOPSLA.input_specs_tiger%d"%i)
		parser.write("from finalTestFilesOOPSLA.input_specs_tiger%d"%i)
		init.close()
		test.close()
		parser.close()
		row = [] #len(string), fileno, no of rules 
		for k in range(1):
			try:
				row.append(subprocess.call("python synth.py %d %d"%(j,i), shell=True, timeout=180))
			except Exception as e:
				print ("Exception:",e)
				results = open("results_file_rebuttal.csv","a+")
				results.write("input, specs,tiger, %d, timeout\n"%(i))
				results.close()
				continue
			else:
				pass
			finally:
				pass
#vsahil@subhajit1.cse.iitk.ac.in
#vsahil123
