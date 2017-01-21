#relop, integer = string, * = /
def specs():

	#Space separated (tokized) strings
	# accept_strings = ["?", "! ?", "( ?"]
	accept_strings = ["let type of = array of id var id : id := id [ integer ] of integer in id end"]
	reject_strings = ["let"]

	config = {
		'num_rules': 79, #Number of rules
		'size_rules' : 8, #Number of symbols in RHS
		'num_nonterms' : 40, #Number of nonterms
		'expansion_constant' : 10, #Determines the max. number of parse actions to take while parsing
		'optimize' : False, # enable optimized mode
		'neg_egs' : False, # consider negative examples 
		'threshold' : 0.2  # number of unsat cores to break
	}

	return accept_strings,reject_strings,config

def add_eps(original_grammar):
	grammar = []
	for i in range(len(original_grammar)):
		tmp = []
		t = len(original_grammar[i])
		tmp.append(original_grammar[i][0])
		for j in range(9-t):
			tmp.append("eps")
		for j in range(1,len(original_grammar[i])):
			tmp.append(original_grammar[i][j])
		grammar.append(tmp)
	return grammar

def find_original_grammar():
	# original_grammar = [['S','eps','eps','F','S'], ['S','eps','eps','eps','Q'], ['S','(','S',')','S'], ['F','eps','eps','!','A'], ['Q','eps','eps','?','A'],['A','eps','eps','eps','eps']]
	# return get_original_grammar()
	original_grammar = [['Prog','Exp'],['Exp','ExpOR','ExpORPr'],['ExpOR','ExpAND','ExpANDPr'],

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
	original_grammar = add_eps(original_grammar)
	return original_grammar

def convert_parse_table(ptable):
	parse_table = []
	for key in ptable:
		tmp = ptable[key]
		tmp['non_term'] = key
		parse_table.append(tmp)
	print "len(parse_table):",len(parse_table)
	# print parse_table
	return parse_table

def get_parse_table():
	parse_table =  {'IF_extra': {'do': 24, ':=': 0, 'in': 24, 'array': 0, 'id': 0, 'if': 0, 'end': 24, 'for': 0, '&': 24, ')': 24, '(': 0, '+': 24, '*': 24, '-': 24, ',': 24, '.': 0, 'to': 24, 'var': 24, ';': 24, ':': 0, 'type': 24, 'function': 24, 'then': 24, 'nil': 0, 'else': 23, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 24, 'relop': 24, 'dol': 24, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 24, '|': 24}, 'VarDec': {'do': 0, ':=': 0, 'in': 0, 'array': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '.': 0, 'to': 0, 'var': 52, ';': 0, ':': 0, 'type': 0, 'function': 0, 'then': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'ExpOR': {'do': 0, ':=': 0, 'in': 0, 'array': 0, 'id': 3, 'if': 3, 'end': 0, 'for': 3, '&': 0, ')': 0, '(': 3, '+': 0, '*': 0, '-': 3, ',': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, 'function': 0, 'then': 0, 'nil': 3, 'else': 0, 'break': 3, 'let': 3, 'integer': 3, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 3, 'of': 0, '{': 0, '}': 0, '|': 0}, 'EL_extra': {'do': 0, ':=': 0, 'in': 0, 'array': 0, 'id': 0, 'if': 0, 'end': 72, 'for': 0, '&': 0, ')': 72, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '.': 0, 'to': 0, 'var': 0, ';': 73, ':': 0, 'type': 0, 'function': 0, 'then': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'FRA_extra1': {'do': 62, ':=': 62, 'in': 62, 'array': 0, 'id': 0, 'if': 0, 'end': 62, 'for': 0, '&': 62, ')': 62, '(': 0, '+': 62, '*': 62, '-': 62, ',': 62, '.': 62, 'to': 62, 'var': 62, ';': 62, ':': 0, 'type': 62, 'function': 62, 'then': 62, 'nil': 0, 'else': 62, 'break': 0, 'let': 0, 'integer': 0, '[': 62, ']': 62, 'relop': 62, 'dol': 62, '=': 0, 'while': 0, 'of': 63, '{': 0, '}': 62, '|': 62}, 'FRAP_extra1': {'do': 65, ':=': 64, 'in': 65, 'array': 0, 'id': 0, 'if': 0, 'end': 65, 'for': 0, '&': 65, ')': 65, '(': 0, '+': 65, '*': 65, '-': 65, ',': 65, '.': 0, 'to': 65, 'var': 65, ';': 65, ':': 0, 'type': 65, 'function': 65, 'then': 65, 'nil': 0, 'else': 65, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 65, 'relop': 65, 'dol': 65, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 65, '|': 65}, 'RelationOp': {'do': 0, ':=': 0, 'in': 0, 'array': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, 'function': 0, 'then': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'relop': 79, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'AL_extra': {'do': 0, ':=': 0, 'in': 0, 'array': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 77, '(': 0, '+': 0, '*': 0, '-': 0, ',': 76, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, 'function': 0, 'then': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'FunctionRecordArrayPr': {'do': 66, ':=': 66, 'in': 66, 'array': 0, 'id': 0, 'if': 0, 'end': 66, 'for': 0, '&': 66, ')': 66, '(': 0, '+': 66, '*': 66, '-': 66, ',': 66, '.': 66, 'to': 66, 'var': 66, ';': 66, ':': 0, 'type': 66, 'function': 66, 'then': 66, 'nil': 0, 'else': 66, 'break': 0, 'let': 0, 'integer': 0, '[': 66, ']': 66, 'relop': 66, 'dol': 66, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 66, '|': 66}, 'DL_extra': {'do': 0, ':=': 0, 'in': 32, 'array': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '.': 0, 'to': 0, 'var': 31, ';': 0, ':': 0, 'type': 31, 'function': 31, 'then': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'Factor': {'do': 0, ':=': 0, 'in': 0, 'array': 0, 'id': 29, 'if': 22, 'end': 0, 'for': 26, '&': 0, ')': 0, '(': 20, '+': 0, '*': 0, '-': 21, ',': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, 'function': 0, 'then': 0, 'nil': 18, 'else': 0, 'break': 27, 'let': 28, 'integer': 19, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 25, 'of': 0, '{': 0, '}': 0, '|': 0}, 'Prog': {'do': 0, ':=': 0, 'in': 0, 'array': 0, 'id': 1, 'if': 1, 'end': 0, 'for': 1, '&': 0, ')': 0, '(': 1, '+': 0, '*': 0, '-': 1, ',': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, 'function': 0, 'then': 0, 'nil': 1, 'else': 0, 'break': 1, 'let': 1, 'integer': 1, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 1, 'of': 0, '{': 0, '}': 0, '|': 0}, 'FRAP_extra': {'do': 69, ':=': 69, 'in': 69, 'array': 0, 'id': 0, 'if': 0, 'end': 69, 'for': 0, '&': 69, ')': 69, '(': 0, '+': 69, '*': 69, '-': 69, ',': 69, '.': 67, 'to': 69, 'var': 69, ';': 69, ':': 0, 'type': 69, 'function': 69, 'then': 69, 'nil': 0, 'else': 69, 'break': 0, 'let': 0, 'integer': 0, '[': 68, ']': 69, 'relop': 69, 'dol': 69, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 69, '|': 69}, 'FRA_extra': {'do': 0, ':=': 0, 'in': 0, 'array': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 59, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, 'function': 0, 'then': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 60, '|': 0}, 'TypeId': {'do': 0, ':=': 0, 'in': 0, 'array': 0, 'id': 48, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, 'function': 0, 'then': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 49, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'ArgList': {'do': 0, ':=': 0, 'in': 0, 'array': 0, 'id': 75, 'if': 75, 'end': 0, 'for': 75, '&': 0, ')': 74, '(': 75, '+': 0, '*': 0, '-': 75, ',': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, 'function': 0, 'then': 0, 'nil': 75, 'else': 0, 'break': 75, 'let': 75, 'integer': 75, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 75, 'of': 0, '{': 0, '}': 0, '|': 0}, 'FL_extra': {'do': 0, ':=': 0, 'in': 0, 'array': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 43, '(': 0, '+': 0, '*': 0, '-': 0, ',': 42, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, 'function': 0, 'then': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 43, '|': 0}, 'Ty': {'do': 0, ':=': 0, 'in': 0, 'array': 38, 'id': 39, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, 'function': 0, 'then': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 39, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 37, '}': 0, '|': 0}, 'ExpANDPr': {'do': 7, ':=': 0, 'in': 7, 'array': 0, 'id': 0, 'if': 0, 'end': 7, 'for': 0, '&': 6, ')': 7, '(': 0, '+': 7, '*': 7, '-': 7, ',': 7, '.': 0, 'to': 7, 'var': 7, ';': 7, ':': 0, 'type': 7, 'function': 7, 'then': 7, 'nil': 0, 'else': 7, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 7, 'relop': 7, 'dol': 7, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 7, '|': 7}, 'FieldList': {'do': 0, ':=': 0, 'in': 0, 'array': 0, 'id': 41, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 40, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, 'function': 0, 'then': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 40, '|': 0}, 'RelationExp': {'do': 11, ':=': 0, 'in': 11, 'array': 0, 'id': 0, 'if': 0, 'end': 11, 'for': 0, '&': 11, ')': 11, '(': 0, '+': 11, '*': 11, '-': 11, ',': 11, '.': 0, 'to': 11, 'var': 11, ';': 11, ':': 0, 'type': 11, 'function': 11, 'then': 11, 'nil': 0, 'else': 11, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 11, 'relop': 10, 'dol': 11, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 11, '|': 11}, 'UnaryOp': {'do': 0, ':=': 0, 'in': 0, 'array': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 78, ',': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, 'function': 0, 'then': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'FunDec': {'do': 0, ':=': 0, 'in': 0, 'array': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, 'function': 53, 'then': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'Term': {'do': 0, ':=': 0, 'in': 0, 'array': 0, 'id': 12, 'if': 12, 'end': 0, 'for': 12, '&': 0, ')': 0, '(': 12, '+': 0, '*': 0, '-': 12, ',': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, 'function': 0, 'then': 0, 'nil': 12, 'else': 0, 'break': 12, 'let': 12, 'integer': 12, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 12, 'of': 0, '{': 0, '}': 0, '|': 0}, 'FactorPr': {'do': 17, ':=': 0, 'in': 17, 'array': 0, 'id': 0, 'if': 0, 'end': 17, 'for': 0, '&': 17, ')': 17, '(': 0, '+': 17, '*': 16, '-': 17, ',': 17, '.': 0, 'to': 17, 'var': 17, ';': 17, ':': 0, 'type': 17, 'function': 17, 'then': 17, 'nil': 0, 'else': 17, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 17, 'relop': 17, 'dol': 17, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 17, '|': 17}, 'Exp': {'do': 0, ':=': 0, 'in': 0, 'array': 0, 'id': 2, 'if': 2, 'end': 0, 'for': 2, '&': 0, ')': 0, '(': 2, '+': 0, '*': 0, '-': 2, ',': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, 'function': 0, 'then': 0, 'nil': 2, 'else': 0, 'break': 2, 'let': 2, 'integer': 2, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 2, 'of': 0, '{': 0, '}': 0, '|': 0}, 'ExpList': {'do': 0, ':=': 0, 'in': 0, 'array': 0, 'id': 71, 'if': 71, 'end': 70, 'for': 71, '&': 0, ')': 70, '(': 71, '+': 0, '*': 0, '-': 71, ',': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, 'function': 0, 'then': 0, 'nil': 71, 'else': 0, 'break': 71, 'let': 71, 'integer': 71, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 71, 'of': 0, '{': 0, '}': 0, '|': 0}, 'Dec': {'do': 0, ':=': 0, 'in': 0, 'array': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '.': 0, 'to': 0, 'var': 34, ';': 0, ':': 0, 'type': 33, 'function': 35, 'then': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'FieldExpList': {'do': 0, ':=': 0, 'in': 0, 'array': 0, 'id': 45, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, 'function': 0, 'then': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'ExpAND': {'do': 0, ':=': 0, 'in': 0, 'array': 0, 'id': 8, 'if': 8, 'end': 0, 'for': 8, '&': 0, ')': 0, '(': 8, '+': 0, '*': 0, '-': 8, ',': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, 'function': 0, 'then': 0, 'nil': 8, 'else': 0, 'break': 8, 'let': 8, 'integer': 8, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 8, 'of': 0, '{': 0, '}': 0, '|': 0}, 'VD_extra': {'do': 0, ':=': 50, 'in': 0, 'array': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 51, 'type': 0, 'function': 0, 'then': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 50, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'LValue': {'do': 0, ':=': 0, 'in': 0, 'array': 0, 'id': 54, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, 'function': 0, 'then': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'FEL_extra': {'do': 0, ':=': 0, 'in': 0, 'array': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 46, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, 'function': 0, 'then': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'TyDec': {'do': 0, ':=': 0, 'in': 0, 'array': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 36, 'function': 0, 'then': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'DecList': {'do': 0, ':=': 0, 'in': 30, 'array': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '.': 0, 'to': 0, 'var': 30, ';': 0, ':': 0, 'type': 30, 'function': 30, 'then': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'ArithExp': {'do': 0, ':=': 0, 'in': 0, 'array': 0, 'id': 9, 'if': 9, 'end': 0, 'for': 9, '&': 0, ')': 0, '(': 9, '+': 0, '*': 0, '-': 9, ',': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, 'function': 0, 'then': 0, 'nil': 9, 'else': 0, 'break': 9, 'let': 9, 'integer': 9, '[': 0, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 9, 'of': 0, '{': 0, '}': 0, '|': 0}, 'TermPr': {'do': 15, ':=': 0, 'in': 15, 'array': 0, 'id': 0, 'if': 0, 'end': 15, 'for': 0, '&': 15, ')': 15, '(': 0, '+': 13, '*': 15, '-': 14, ',': 15, '.': 0, 'to': 15, 'var': 15, ';': 15, ':': 0, 'type': 15, 'function': 15, 'then': 15, 'nil': 0, 'else': 15, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 15, 'relop': 15, 'dol': 15, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 15, '|': 15}, 'LD_extra': {'do': 55, ':=': 55, 'in': 55, 'array': 0, 'id': 0, 'if': 0, 'end': 55, 'for': 0, '&': 55, ')': 55, '(': 56, '+': 55, '*': 55, '-': 55, ',': 55, '.': 55, 'to': 55, 'var': 55, ';': 55, ':': 0, 'type': 55, 'function': 55, 'then': 55, 'nil': 0, 'else': 55, 'break': 0, 'let': 0, 'integer': 0, '[': 55, ']': 55, 'relop': 55, 'dol': 55, '=': 0, 'while': 0, 'of': 0, '{': 56, '}': 55, '|': 55}, 'ExpORPr': {'do': 5, ':=': 0, 'in': 5, 'array': 0, 'id': 0, 'if': 0, 'end': 5, 'for': 0, '&': 5, ')': 5, '(': 0, '+': 5, '*': 5, '-': 5, ',': 5, '.': 0, 'to': 5, 'var': 5, ';': 5, ':': 0, 'type': 5, 'function': 5, 'then': 5, 'nil': 0, 'else': 5, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 5, 'relop': 5, 'dol': 5, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 5, '|': 4}, 'FunctionRecordArray': {'do': 0, ':=': 0, 'in': 0, 'array': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 57, '+': 0, '*': 0, '-': 0, ',': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, 'function': 0, 'then': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 61, ']': 0, 'relop': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 58, '}': 0, '|': 0}}
	parse_table['LD_extra']['[']= 56
	parse_table = convert_parse_table(parse_table)
	# print len(parse_table)
	return parse_table

def nums():
	original_grammar = find_original_grammar()
	num_vars = {'num_rules':len(original_grammar), 'size_rules':len(original_grammar[0])-1}
	return num_vars

# accept_strings = [") )"]
# reject_strings = [")", ") ("]
accept_strings = ["let type of = array of id var id : id := id [ integer ] of integer in id end"]
get_parse_table()
