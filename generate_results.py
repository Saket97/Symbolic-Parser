import subprocess
tmp = [11,12,17,18,20,21,22]
# tmp = [11]
for j in range(2):	
	for i in tmp:
		init = open("init.py", "r+")
		test = open("test.py", "r+")
		parser = open("parser.py", "r+")
		init.write("from useful.input_final%d"%i)
		test.write("from useful.input_final%d"%i)
		parser.write("from useful.input_final%d"%i)
		init.close()
		test.close()
		parser.close()
		row = [] #len(string), fileno, no of rules 
		for k in range(10):
			try:
				row.append(subprocess.call("python synth.py %d"%j, shell=True, timeout=60))
			except Exception as e:
				continue
			else:
				pass
			finally:
				pass
