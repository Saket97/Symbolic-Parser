import random
import numpy as np
def flip(p):
	if random.random() < p:
		return 0
	else:
		return 1
def find_token(line,index = False):
	# print "find_token_called index:%s"%index
	a = ""
	for i in range(len(line)):
		# print "i: ",i
		if line[i] == ' ' or line[i] == '\n' or line[i] == '\t':
			if index == True:
				return i
			return a
		a += line[i]
	# print "index: ",index
	if index == True:
		# print "conditional i: ",i
		return i
	return a

def find_begin_line(line,index=False):
	a = ""
	i = find_token(line,index=True)
	j = i
	# print "j: ",j
	while (not(line[j]<='9' and line[j]>='0')):
		j += 1
	while True:
		a = a+line[j]
		j+=1
		if not(line[j]<='9' and line[j]>='0'):
			if index:
				return j
			return int(a)
		
def find_begin_col(line, index = False):
	i = find_begin_line(line, index = True)
	a = ""
	j = i
	while (not(line[j]<='9' and line[j]>='0')):
		j += 1
	while True:
		a = a+line[j]
		j+=1
		if not(line[j]<='9' and line[j]>='0'):
			if index:
				return j
			return int(a)

def find_end_col(line, index = False):
	a = ""
	i = find_begin_col(line, index = True)
	j = i
	# print "j:",j
	while (not(line[j]<='9' and line[j]>='0')):
		j += 1
	while True:
		a = a+line[j]
		j+=1
		if not(line[j]<='9' and line[j]>='0'):
			if index:
				return j
			return int(a)

def file_copy(aux_file, output_file, p, p_delete, p_replace, p_insert):
	#### iterate through the aux file and copy on the output_file ###
	b_start_till_prev_line = 0
	col_add = 0
	prev_line = 1
	curr_line = 1
	end_col = 0

	for line in aux_file:	
		### get token,line,col ###
		prev_line = curr_line
		token = find_token(line)
		curr_line = find_begin_line(line)
		if prev_line != curr_line:
			# b_start_till_prev_line += end_col + col_add + 1
			b_start_till_prev_line = output_file.tell()
			### insert operation at end ####
			n = flip(p)
			if n == 0:
				x = np.random.multinomial(1,[p_delete,p_replace,p_insert])
				if x[2] == 1:
					output_file.seek(b_start_till_prev_line,0)
					output_file.write(" ")
					new_token = "Ankit"
					output_file.write(new_token)
			col_add = 0
			# output_file.write("x")
			print "ftell1: ",output_file.tell()
			print >> output_file,""
			print "ftell2: ",output_file.tell()
			b_start_till_prev_line = output_file.tell()
		begin_col = find_begin_col(line)
		end_col = find_end_col(line)
		length = end_col - begin_col + 1 
		##########################
		
		### print white space ####
		i = output_file.tell()+1
		print "i: ",i
		while i < b_start_till_prev_line + col_add + begin_col:
			i += 1
			output_file.write(" ")
		##########################
		n = flip(p)
		if n == 0:
			x = np.random.multinomial(1,[p_delete,p_replace,p_insert])
			if x[0] == 1:
				#### delete operation
				col_add -= length
			if x[1] == 1:
				#### replace operation
				output_file.seek(b_start_till_prev_line + col_add + begin_col-1,0)
				new_token = "poonam"
				output_file.write(new_token)
				col_add += len(new_token) - length
			if x[2] == 1:
				#### insert operation
				output_file.seek(b_start_till_prev_line + col_add + begin_col-1,0)
				new_token = "sunil"
				print "ftell3: ",output_file.tell()
				col_add += len(new_token) + 1
				output_file.write("%s "%(new_token))
				print "ftell4: ",output_file.tell()
				output_file.write(token)
				print "ftell5: ",output_file.tell()
		else:
			output_file.seek(b_start_till_prev_line + col_add + begin_col-1,0)
			output_file.write(token)


	###################################################################

def main():
	input_file = open("check.txt",'r')
	output_file = open("check_out1.txt",'w')
	file_copy(input_file, output_file,0.8, 0,0,1)
	input_file.close()
	output_file.close()
main()