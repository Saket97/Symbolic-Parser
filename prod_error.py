import random
import numpy as np
import sys
import subprocess
def flip(p):
	if random.random() < p:
		return 0
	else:
		return 1

def file_copy(aux_file, input_file, output_file, p, p_delete, p_replace, p_insert):
	#### iterate through the aux file and copy on the output_file ###
	col_add = 0
	prev_line = 0
	curr_line = 0
	for line in aux_file:
		### get token,line,col ###
		prev_line = curr_line
		token = 
		curr_line = 
		begin_col =
		end_col = 
		length = end_col - begin_col + 1 
		##########################
		if prev_line != curr_line:
			col_add = 0
		n = flip(p)
		if n == 0:
		### generate error
		x = np.random.multinomial(1,[p_delete,p_replace,p_insert])
		if x[0] == 1:
			#### delete operation
			col_add -= length
			if x[1] == 1:
			#### replace operation
			col_add += new_length - length
			if x[2] == 1:
			#### insert operation
			col_add += new_length
			## select and copy new token
			### copy curr token
		else:
		### copy ## add col_add


	###################################################################

def main():
	input_file_name = sys.argv[1]
	output_file_name = sys.argv[2]
	input_file = open(input_file_name,'r')
	output_file = open(output_file_name,'w')
	### make aux_file ### aux file contains one token in one line along with line and column of starting and ending
	subprocess.call(['java tigerLexer test1.tig aux_file_name'],shell=True)
	#####################
	p_errors = input("Enter the probability of errors you want to introduce ")
	p_delete = input("Enter the probbility of deleing")
	p_replace = input("Enter the probability of replacing")
	p_insert = 1-p_delete-p_replace
	assert(p_insert<=1 and p_insert>=0)
	assert(p_replace<=1 and p_replace>=0)
	assert(p_delete<=1 and p_delete>=0)
	file_copy(aux_file, input_file, output_file,p_errors,p_delete,p_replace,p_insert)
	input_file.close()
	output_file.close()
main()