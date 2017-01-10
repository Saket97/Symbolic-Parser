def find_ngrams(string, n, table):
	# string = string.split(" ")
	tmp1 = []
	print "String: ",string
	for s in string:
		if s == " " or s == "\n" or s == '\t':
			continue
		tmp1.append(s)
	string = tmp1
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

# def delete_comment(file_name):
# 	f = open(file_name, 'r+')
# 	lines = f.readlines()
# 	i = 0
# 	while True and i <= 5:
# 		if lines[i][-2] == '/' and lines[i][-3] == '*':
# 			return i,lines
# 		else:
# 			i += 1
# 	print "some bug..."

def prepare_string(file_name):
	# start,line_list = delete_comment(file_name)
	f = open(file_name, 'r')
	line_list = f.readlines()
	f.close()
	string = []
	i = 0
	for line in line_list:
		tmp = ""
		for word in line:
			if word == " " or word == "\t" or word == "\n":
				continue
			tmp += word
		string.append(tmp)
	return string

table = {}
ngrams = []
n = 3
strings = []
for i in range(1,5):
	string = prepare_string("Examples/Processed/test%d_lex.tig"%i)
	strings.append(string)
# strings = ["let type id = array of id var id : id := id [ id ] in in integer of id end"]
for string in strings:
	table = find_ngrams(string, n, table)
print table