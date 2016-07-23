import subprocess
import sys
import time
def comment_out(output_file,start,end):# lines are numered from 1
	tmp = []
	for i in range(start, end+1):
		b_start = offset[i-1]
		output_file.seek(b_start,0)
		line = output_file.readline()
		tmp.append("%s%s"%(line[0],line[1]))
		tmp1 = "//" + line[2:]
		output_file.seek(b_start,0)
		output_file.write(tmp1)
		# print "line: ",line
		# print "line[2:] ",line[2:]
		# print "line: %d TMP1: %s"%(i,tmp1)
	output_file.flush()
	return tmp
	
def uncomment(output_file,start,end,tmp):
	k = 0
	for i in range(start, end+1):
		b_start = offset[i-1]
		output_file.seek(b_start,0)
		line = output_file.readline()
		l = len(tmp[k])
		tmp1 = ""
		for j in range(len(tmp[k])):
			tmp1 += tmp[k][j]
		tmp1 += line[l:]
		output_file.seek(b_start,0)
		output_file.write(tmp1)
		k += 1
	output_file.flush()

def reduce(output_file,start,end):
	if start > end:
		return
	if start == end:
		return
	if start == end:
		tmp = comment_out(output_file,start,end)
		try:
			# print "output3 start=end=%d"%(start)
			output3 = subprocess.check_output(["gcc %s"%(output_file_name)],stderr=subprocess.STDOUT,shell = True)
		except subprocess.CalledProcessError as ex:
			output3 = ex.output
			
		print output3
		if output3 == output:
			return
		else:
			uncomment(output_file,start,end,tmp)
			return
	
	mid = (start + end)/2
	tmp = comment_out(output_file,start,mid)
	# output_file.flush()
	up_comment = False
	down_comment = False
	try:
		# print "output1 start:%d end:%d"%(start,mid)
		output1 = subprocess.check_output(["gcc %s"%(output_file_name)],stderr=subprocess.STDOUT,shell = True)
	except subprocess.CalledProcessError as ex:
		output1 = ex.output
		# print "output1: ",output1
		pass
	print output1
	if output1 == output:
		up_comment= True
	else:
		uncomment(output_file,start,mid,tmp)
		up_comment = False

	tmp = comment_out(output_file,mid+1,end)
	try:
		# print "output2 start:%d end:%d"%(mid+1,end)
		output2 = subprocess.check_output(["gcc %s"%(output_file_name)],stderr=subprocess.STDOUT, shell = True)
	except subprocess.CalledProcessError as ex:
		output2 = ex.output
		pass
	print output2
	if output2 == output:
		down_comment = True
	else:
		uncomment(output_file,mid+1,end,tmp)
		down_comment = False

	if up_comment == False:
		reduce(output_file,start,mid)
	if down_comment == False:
		reduce(output_file,mid+1,end)
	# if start == mid and start == 6:
	# 	print "up_comment ",up_comment
	# 	print "down_comment ",down_comment
	# if mid+1 == end and end == 6:
	# 	print "up_comment ",up_comment
	# 	print "down_comment ",down_comment

start_time = time.time()
input_file_name = sys.argv[1]
output_file_name = sys.argv[2]
input_file = open(input_file_name,'r')
output_file = open(output_file_name,'r+')


n_lines = 0 # lines will be numbered starting from 1
offset = []
for line in input_file:
	offset.append(output_file.tell())
	for i in range(len(line)-1):
		output_file.write(line[i])
	if len(line) == 1:
		output_file.write(line[0])
	output_file.write("   \n")
	# output_file.write(line)
	n_lines += 1
# print "offset: ",offset
output_file.flush()
try:
	output = subprocess.check_output(["gcc %s"%(output_file_name)],stderr=subprocess.STDOUT,shell=True)
except subprocess.CalledProcessError as ex:
	output = ex.output	
else:
	print "Given file has no compilation error"
	exit()
# print "output: ",output
input_file.close()

reduce(output_file,1,n_lines)
output_file.close()
print "time_taken: ",(time.time()-start_time)