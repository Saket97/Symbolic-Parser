import subprocess
import sys
import time
from os import mknod,remove,path
def comment_out(output_file,start,end,offset):# lines are numered from 1
	tmp = []
	# print "comment function called..."
	for i in range(start, end+1):
		b_start = offset[i-1]
		output_file.seek(b_start,0)
		line = output_file.readline()
		# print "line: %s length: %d line[0]/: %s"%(line,len(line),line[0])
		# if line[0] == '}' or line[0] == '{':
			# continue
		tmp.append("%s%s"%(line[0],line[1]))
		tmp1 = "//" + line[2:]
		output_file.seek(b_start,0)
		output_file.write(tmp1)
		
		# print "line[2:] ",line[2:]
		# print "line: %d TMP1: %s"%(i,tmp1)
	output_file.flush()
	return tmp
	
def uncomment(output_file,start,end,tmp,offset):
	k = 0
	for i in range(start, end+1):
		b_start = offset[i-1]
		output_file.seek(b_start,0)
		line = output_file.readline()
		# if line[0] == '{' or line[0] == '}':
			# continue
		l = len(tmp[k])
		tmp1 = ""
		for j in range(len(tmp[k])):
			tmp1 += tmp[k][j]
		tmp1 += line[l:]
		output_file.seek(b_start,0)
		output_file.write(tmp1)
		k += 1
	output_file.flush()

def reduce_program(output_file,start,end,offset,output):
	# print "reduce functioin called..."
	if start > end:
		return
	if start == end:
		return
	if start == end:
		tmp = comment_out(output_file,start,end,offset)
		try:
			# print "output3 start=end=%d"%(start)
			output3 = subprocess.check_output(["gcc %s"%("aux.c")],stderr=subprocess.STDOUT,shell = True)
		except subprocess.CalledProcessError as ex:
			output3 = ex.output
			
		# print "output3 == output is %s for line:%d"%(output == output3, start)
		if output3 == output:
			return
		else:
			uncomment(output_file,start,end,tmp,offset)
			return
	
	mid = (start + end)/2
	up_comment = False
	down_comment = False

	tmp = comment_out(output_file,mid+1,end,offset)
	try:
		# print "output2 start:%d end:%d"%(mid+1,end)
		output2 = subprocess.check_output(["gcc %s"%("aux.c")],stderr=subprocess.STDOUT, shell = True)
	except subprocess.CalledProcessError as ex:
		output2 = ex.output
		pass
	print output2
	if output2 == output:
		down_comment = True
	else:
		uncomment(output_file,mid+1,end,tmp,offset)
		down_comment = False

	tmp = comment_out(output_file,start,mid,offset)
	# output_file.flush()
	try:
		# print "output1 start:%d end:%d"%(start,mid)
		output1 = subprocess.check_output(["gcc %s"%("aux.c")],stderr=subprocess.STDOUT,shell = True)
	except subprocess.CalledProcessError as ex:
		output1 = ex.output
		# print "output1: ",output1
		pass
	print output1
	if output1 == output:
		up_comment= True
	else:
		uncomment(output_file,start,mid,tmp,offset)
		up_comment = False

	if up_comment == False:
		reduce_program(output_file,start,mid,offset,output)
	if down_comment == False:
		reduce_program(output_file,mid+1,end,offset,output)
	
def delete_comment(output_file,aux):
	output_file.flush()
	output_file.seek(0,0)
	n_lines = 0
	for line in output_file:
		# print "line:%s line[0]:%s line[1]:%s"%(line,line[0],line[1])
		if line[0] == '/' and line[1] == '/':
			continue
		aux.write(line)
		n_lines += 1
	return n_lines

def main(input_file,output_file,aux,n):
	n_lines = 0 # lines will be numbered starting from 1
	offset = []
	for line in input_file:
		# print "line:%s length: %d line[0]:%s"%(line,len(line),line[0])
		offset.append(output_file.tell())
		for i in range(len(line)-1):
			output_file.write(line[i])
		if len(line) == 1:
			n_lines += 1
			if line[0] == '\n':
				output_file.write("    \n")
			else:
				output_file.write("%s     "%line[0])
			continue
		output_file.write("     \n")
		n_lines += 1
	output_file.flush()

	try:
		output = subprocess.check_output(["gcc %s"%("aux.c")],stderr=subprocess.STDOUT,shell=True)
	except subprocess.CalledProcessError as ex:
		output = ex.output	
	else:
		print "Given file has no compilation error"
		exit()
	# print "output: ",output
	reduce_program(output_file,1,n_lines,offset,output)
	if n == 1:
		aux.seek(0,0)
		aux.truncate()
	n_lines_aux = delete_comment(output_file,aux)
	return n_lines_aux
	# aux.close()
	# output_file.close()

if __name__ == '__main__':
	start_time = time.time()
	input_file_name = sys.argv[1]
	output_file_name = sys.argv[2]
	if path.isfile(output_file_name) == False:
		mknod(output_file_name)
	if path.isfile("aux.c") == False:
		mknod("aux.c")
	input_file = open(input_file_name,'r')
	aux = open(output_file_name,'w+')
	output_file = open("aux.c",'w+')
	prev_nlines = None
	curr_nlines = None
	curr_nlines = main(input_file,output_file,aux,0)
	input_file.close()
	count = 1
	for i in range(10):
		count += 1
		output_file.seek(0,0)
		aux.seek(0,0)
		output_file.truncate()
		prev_nlines = curr_nlines
		curr_nlines = main(aux,output_file,aux,1)
		if prev_nlines == curr_nlines:
			break
	output_file.close()
	aux.close()
	# aux1.close()
	# remove("aux.c")
	print "iterations done: ",count
	print "time_taken: ",(time.time()-start_time)
# mknod("new.txt")
# remove("new.txt")
# 121lines 2.3-2.6
# 176 lines 4.22
# 233 lines 5.62
# check2->check3->check6->check7->check8->