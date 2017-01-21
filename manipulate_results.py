import csv
import numpy as np
r_file = open("results_file1.csv")
r_file_r = csv.reader(r_file)
r_file_data = list(r_file_r)
output_file = open("results_file2.csv",'w+')
start = False
tmp = []
prev = None
print "n_rows = ",len(r_file_data)
for i in range(len(r_file_data)):
	if r_file_data[i][1] == '':
		print "1row no.:",i
		if i == 0:
			continue
		a = np.array(tmp)
		print "data1:",tmp
		output_file.write("%s,%s,%f,%f,%s\n"%(r_file_data[i-2][0],r_file_data[i-2][1],np.mean(a, axis=0),np.std(a, axis=0),r_file_data[i-2][4]))
		start = False
		tmp = []
		continue
	if start == False:
		print "2row no.:",i
		tmp1 = r_file_data[i][2].split(':')
		tmp.append(int(tmp1[1])*60+int(tmp1[2]))
		start = True
		continue
	if start == True:
		if r_file_data[i][1] == r_file_data[i-1][1]:
			print "3row no.:",i
			tmp1 = r_file_data[i][2].split(':')
			tmp.append(int(tmp1[1])*60+int(tmp1[2]))
		else:
			print "4row no.:",i
			a = np.array(tmp)
			print "data:",tmp
			output_file.write("%s,%s,%f,%f,%s\n"%(r_file_data[i-1][0],r_file_data[i-1][1],np.mean(a, axis=0),np.std(a, axis=0),r_file_data[i-1][4]))
			start = False
			tmp = []
			tmp1 = r_file_data[i][2].split(':')
			tmp.append(int(tmp1[1])*60+int(tmp1[2]))
r_file.close()
output_file.close()