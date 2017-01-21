def discvover_non_terminals(grammar):
	non_terminals = []
	for i in range(len(grammar)):
		if grammar[i][0] not in non_terminals:
			non_terminals.append(grammar[i][0])
	return non_terminals

def discover_terminals(grammar):
	tokens = []
	for i in non_terminals:
		rule_contri_first[i] = {"complete":0}
		rule_contri_follow[i] = {"complete":0}
	for i in range(len(grammar)):
		rule_contri_first[grammar[i][0]][i] = 0
		for j in range(1,len(grammar[i])):
			if grammar[i][j] not in non_terminals:
				if grammar[i][j] not in tokens:
					tokens.append(grammar[i][j])
			else:
				rule_contri_follow[grammar[i][j]][i] = 0
	for i in tokens:
		rule_contri_first[i] = {"complete":1}
		rule_contri_follow[i] = {"complete":1}		
	return tokens

def first_set_util(nt,first_set):
	for rule in rule_contri_first[nt]:
		if rule == "complete":
			continue
		rule = int(rule)
		whole_rule_eps = True
		if rule_contri_first[nt][rule] == 1:
			continue
		for i in range(1,len(grammar[rule])):
			if not rule_contri_first[grammar[rule][i]]["complete"] == 1:
				first_set_util(grammar[rule][i],first_set)
			
			is_eps = False
			for j in first_set[grammar[rule][i]]:
				if j == "eps":
					is_eps = True
					continue
				if j not in first_set[nt]:
					first_set[nt].append(j)
			if is_eps == False:
				whole_rule_eps = False
				break
		if whole_rule_eps:
			first_set[nt].append("eps")
		rule_contri_first[nt][rule] = 1
						
def cal_first_set(grammar):
	first_set = {}
	for i in range(len(tokens)):
		first_set[tokens[i]] = [tokens[i]]
	first_set["eps"] = ["eps"]
	for nt in non_terminals:
		first_set[nt] = []
	for i in range(len(non_terminals)):
		first_set_util(non_terminals[i],first_set)
		com = 1
		for j in rule_contri_first[non_terminals[i]]:
			if j == "complete":
				continue
			if rule_contri_first[non_terminals[i]][j] == 0:
				com = 0
				print "nt:%s rule:%s not completed"%(non_terminals[i],j)
				break
		if com:
			rule_contri_first[non_terminals[i]]["complete"] = 1
	return first_set

def follow_set_util(nt,follow_set,parent):
	print "follow_set_util:%s"%nt
	for rule in rule_contri_follow[nt]:
		if rule == "complete":
			continue
		print "	rule:%s"%rule
		print "	follow_set:,",follow_set
		rule = int(rule)
		if rule_contri_follow[nt][rule] == 1:
			continue
		for i in range(1,len(grammar[rule])):
			if grammar[rule][i] != nt:
				continue
			if i != len(grammar[rule])-1:
				for k in range(i+1,len(grammar[rule])):
					eps_present = False
					for j in first_set[grammar[rule][k]]:
						if j != "eps":
							if j not in follow_set[nt]:
								follow_set[nt].append(j)
						else:
							eps_present = True
					if eps_present == False:
						break
					else:
						if k == len(grammar[rule])-1:
							if grammar[rule][0] == nt:
								continue
							follow_superset[nt].append(grammar[rule][0])
							follow_subset[grammar[rule][0]].append(nt)
			else:
				if grammar[rule][0] == nt:
					continue
				follow_subset[grammar[rule][0]].append(nt)
				follow_superset[nt].append(grammar[rule][0])
		rule_contri_follow[nt][rule] = 1

def add_to_supersets(nt,follow_set):
	for supernt in follow_subset[nt]:
		for j in follow_set[nt]:
			if j not in follow_set[supernt]:
				follow_set[supernt].append(j)
				follow_changed[supernt] = True
	follow_changed[nt] = False

def final_addition(follow_set):
	changed = True
	while changed:
		changed = False
		for nt in non_terminals:
			if follow_changed[nt] == True:
				add_to_supersets(nt,follow_set)
				changed = True

def cal_follow_set(grammar):
	follow_set = {}
	for i in tokens:
		follow_set[i] = [i]
	follow_set['dol'] = ['dol']
	for nt in non_terminals:
		follow_set[nt] = []
	follow_set[grammar[0][0]].append('dol')
	for nt in non_terminals:
		if rule_contri_follow[nt]["complete"] == 1:
			continue
		follow_set_util(nt,follow_set,[])
		com = 1
		for i in rule_contri_follow[nt]:
			if rule_contri_follow[nt][i] == 0:
				if i == "complete":
					continue
				com = 0
				print "nt:%s rule:%s follow not completed."%(nt,i)
		if com == 1:
			rule_contri_follow[nt]["complete"] = 1
	final_addition(follow_set)
	return follow_set

def parse_table():
	ptable = {}
	for nt in non_terminals:
		ptable[nt] = {}
		for t in tokens+['dol']:
			if t == 'eps':
				continue
			ptable[nt][t] = 0
	for nt in non_terminals:
		for t in tokens+['dol']:
			if t == "eps":
				continue
			if t in first_set[nt]:
				for rule in rule_contri_first[nt]:
					if rule == "complete":
						continue
					rule = int(rule)
					if t in first_set[grammar[rule][1]]:
						ptable[nt][t] = rule+1
						break
					else:
						for k in range(1,len(grammar[rule])-1):
							if 'eps' in first_set[grammar[rule][k]]:
								if t in first_set[grammar[rule][k+1]]:
									ptable[nt][t] = rule+1
							else:
								break
			else:
				if t in follow_set[nt]:
					for rule in rule_contri_first[nt]:
						if rule == "complete":
							continue
						rule = int(rule)
						if grammar[rule][1] == "eps":
							ptable[nt][t] = rule+1
						if "eps" in first_set[nt]:
							if "eps" in first_set[grammar[rule][1]]:
								ptable[nt][t] = rule+1

	return ptable

def convert_ptable(ptable):
	table = []
	for nt in non_terminals:
		tmp = {'non_term':"%s"%nt}
		tmp.update(ptable[nt])
		table.append(tmp)
	print table
def print_non_zero(ptable):
	for nt in non_terminals:
		print "%s"%nt
		for t in tokens+['dol']:
			if t == "eps":
				continue
			if ptable[nt][t] != 0:
				print "		%s rule "%(t),grammar[ptable[nt][t]-1]
"""grammar = [['Prog','Exp'],['Exp','ExpOR','ExpORPr'],['ExpOR','ExpAND','ExpANDPr'],

['ExpORPr','|','Exp'],['ExpORPr','eps'],['ExpANDPr','&','ExpOR'],

['ExpANDPr','eps'],['ExpAND','ArithExp','RelationExp'],['ArithExp','Term','TermPr'],

['RelationExp','RelationOp','ArithExp'],['RelationExp','eps'],['Term','Factor','FactorPr'],

['TermPr','+','Term','TermPr'],['TermPr','-','Term','TermPr'],

['TermPr','eps'],['FactorPr','*','Factor','FactorPr'],

['FactorPr','eps'],['Factor','nil'],['Factor','integer'],

['Factor','(','ExpList',')'],['Factor','UnaryOp','Exp'],['Factor','if','Exp','then','Exp','IF_extra'],['IF_extra','else','Exp'],['IF_extra','eps'],

['Factor','while','Exp','do','Exp'],['Factor','for','id',':=','Exp','to','Exp','do','Exp'],['Factor','break'],['Factor','let','DecList','in','ExpList','end'],

['Factor','LValue'],['DecList','DL_extra'],['DL_extra','Dec','DL_extra'],['DL_extra','eps'],

['Dec','TyDec'],['Dec','VarDec'],['Dec','FunDec'],['TyDec','type','TypeId','=','Ty'],['Ty','{','FieldList','}'],['Ty','array','of','TypeId'],['Ty','TypeId'],

['FieldList','eps'],['FieldList','id',':','TypeId','FL_extra'],['FL_extra',',','id',':','TypeId','FL_extra'],['FL_extra','eps'],['FieldExpList','eps'],

['FieldExpList','id','=','Exp','FEL_extra'],['FEL_extra',',','id','=','Exp','FEL_extra'],['FEL_extra','eps'],

['TypeId','id'],['TypeId','integer'],['VD_extra','eps'],['VD_extra',':','TypeId'],['VarDec','var','id','VD_extra',':=','Exp'],

['FunDec','function','id','(','FieldList',')','VD_extra','=','Exp'],

['LValue','id','LD_extra'],['LD_extra','FunctionRecordArrayPr'],['LD_extra','FunctionRecordArray'],['FunctionRecordArray','(','ArgList',')'],

['FunctionRecordArray','{','id','=','Exp','FRA_extra','}'],['FRA_extra',',','id','=','Exp','FRA_extra'],['FRA_extra','eps'],

['FunctionRecordArray','[','Exp',']','FRA_extra1'],['FRA_extra1','FunctionRecordArrayPr'],['FRA_extra1','of','Exp'],

['FRAP_extra1',':=','Exp'],['FRAP_extra1','eps'],['FunctionRecordArrayPr','FRAP_extra','FRAP_extra1'], ['FRAP_extra','.','id','FRAP_extra'], ['FRAP_extra','[','Exp',']','FRAP_extra'], ['FRAP_extra','eps'],

['ExpList','eps'],['ExpList','Exp','EL_extra'],['EL_extra','eps'],['EL_extra',';','Exp','EL_extra'],

['ArgList','eps'],['ArgList','Exp','AL_extra'],['AL_extra',',','Exp','AL_extra'],['AL_extra','eps'],

['UnaryOp','-'],['RelationOp','relop']]
grammar1 = [['E','T','E`'],['E`','+','T','E`'],['E`','eps'],['T','F','T`'],['T`','*','F','T`'],['T`','eps'],['F','(','E',')'],['F','id']]
grammar2 = [['S','A','B','e'],['A','d','B'],['A','a','S'],['A','c'],['B','A','S'],['B','b']]
# E : T R ;
# R : "+" T R ;
#   : "-" T R ;
#   : ;                               
# T : "i";

"""
grammar = [['E','T','X'],['X','+','E'],['X','eps'],['T','(','E',')'],['T','i','Y'],['Y','*','T'],['Y','eps']]
rule_contri_first = {}
rule_contri_follow = {}
non_terminals = discvover_non_terminals(grammar)
tokens = discover_terminals(grammar)
# print "non_terminals:\n",non_terminals
first_set = cal_first_set(grammar)
# print "first set:\n",first_set
follow_subset = {}
follow_superset = {}
follow_changed = {}
for nt in non_terminals:
	follow_subset[nt] = []
	follow_superset[nt] = []
	follow_changed[nt] = True
follow_set = cal_follow_set(grammar)
# print "follow set:\n",follow_set
# print "follow_subset:",follow_subset
# print "follow_superser:",follow_superset
ptable = parse_table()
print "parse_table: ",ptable
print "#non_terminals:",len(non_terminals)
print "%terminals:",len(tokens)
print "#rules:",len(grammar)
convert_ptable(ptable)
# print "Non-terminals:",non_terminals
# print_non_zero(ptable)
# print "Changes: "
# print "LD_extra: '[': 58 change to 59..."
# print "terminals=",tokens