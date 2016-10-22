def find_ngrams(string, n, table):
	string = string.split(" ")
	tmp = []
	for j in range(n):
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

table = {}
ngrams = []
n = 3
strings = ["let type id = array of id var id : id := id [ id ] in in integer of id end"]
for string in strings:
	table = find_ngrams(string, n, table)
print table
