#relop, integer = string, * = /
def specs():

	#Space separated (tokized) strings
	# accept_strings = [let type id = array of id var id : id := id [ integer ] of integer in id end]
	accept_string = [ ' let var id := ( ) in array id in integer end ' ]
	reject_strings = ["let"]

	config = {
		'num_rules': 87, #Number of rules
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
	maxsize = 0
	for i in range(len(original_grammar)):
		if len(original_grammar[i]) > maxsize:
			maxsize = len(original_grammar[i])
	for i in range(len(original_grammar)):
		tmp = []
		t = len(original_grammar[i])
		tmp.append(original_grammar[i][0])
		for j in range(maxsize-t):
			tmp.append("eps")
		for j in range(1,len(original_grammar[i])):
			tmp.append(original_grammar[i][j])
		grammar.append(tmp)
	return grammar

def find_original_grammar(eps=True):
	# original_grammar = [['S','eps','eps','F','S'], ['S','eps','eps','eps','Q'], ['S','(','S',')','S'], ['F','eps','eps','!','A'], ['Q','eps','eps','?','A'],['A','eps','eps','eps','eps']]
	# return get_original_grammar()
	original_grammar = [['Prog','Exp'],['Exp','ExpOR','ExpORPr'],['ExpOR','ExpAND','ExpANDPr'],

['ExpORPr','|','Exp'],['ExpORPr','eps'],['ExpANDPr','&','ExpOR'],

['ExpANDPr','eps'],['ExpAND','ArithExp','RelationExp'],['ArithExp','Term','TermPr'],

['RelationExp','RelationOp','ArithExp'],['RelationExp','eps'],['Term','Factor','FactorPr'],

['TermPr','+','Term','TermPr'],['TermPr','-','Term','TermPr'],

['TermPr','eps'],['FactorPr','*','Factor','FactorPr'],['FactorPr','/','Factor','FactorPr'],

['FactorPr','eps'],['Factor','nil'],['Factor','integer'],['Factor','string'],

['Factor','(','ExpList',')'],['Factor','UnaryOp','Exp'],['Factor','if','Exp','then','Exp','IF_extra'],['IF_extra','else','Exp'],['IF_extra','eps'],

['Factor','while','Exp','do','Exp'],['Factor','for','id',':=','Exp','to','Exp','do','Exp'],['Factor','break'],['Factor','let','DecList','in','ExpList','end'],

['Factor','LValue'],['DecList','DL_extra'],['DL_extra','Dec','DL_extra'],['DL_extra','eps'],

['Dec','TyDec'],['Dec','VarDec'],['Dec','FunDec'],['TyDec','type','TypeId','=','Ty'],['Ty','{','FieldList','}'],['Ty','array','of','TypeId'],['Ty','TypeId'],

['FieldList','eps'],['FieldList','id',':','TypeId','FL_extra'],['FL_extra',',','id',':','TypeId','FL_extra'],['FL_extra','eps'],['FieldExpList','eps'],

['FieldExpList','id','=','Exp','FEL_extra'],['FEL_extra',',','id','=','Exp','FEL_extra'],['FEL_extra','eps'],

['TypeId','id'],['TypeId','integer'],['TypeId','string'],['VD_extra','eps'],['VD_extra',':','TypeId'],['VarDec','var','id','VD_extra',':=','Exp'],

['FunDec','function','id','(','FieldList',')','VD_extra','=','Exp'],

['LValue','id','LD_extra'],['LD_extra','FunctionRecordArrayPr'],['LD_extra','FunctionRecordArray'],['FunctionRecordArray','(','ArgList',')'],

['FunctionRecordArray','{','id','=','Exp','FRA_extra','}'],['FRA_extra',',','id','=','Exp','FRA_extra'],['FRA_extra','eps'],

['FunctionRecordArray','[','Exp',']','FRA_extra1'],['FRA_extra1','FunctionRecordArrayPr'],['FRA_extra1','of','Exp'],

['FRAP_extra1',':=','Exp'],['FRAP_extra1','eps'],['FunctionRecordArrayPr','FRAP_extra','FRAP_extra1'], ['FRAP_extra','.','id','FRAP_extra'], ['FRAP_extra','[','Exp',']','FRAP_extra'], ['FRAP_extra','eps'],

['ExpList','eps'],['ExpList','Exp','EL_extra'],['EL_extra','eps'],['EL_extra',';','Exp','EL_extra'],

['ArgList','eps'],['ArgList','Exp','AL_extra'],['AL_extra',',','Exp','AL_extra'],['AL_extra','eps'],

['UnaryOp','-'],['RelationOp','='],['RelationOp','!='],['RelationOp','>'],['RelationOp','<'],['RelationOp','>='],['RelationOp','<=']]
	
	print "len(original_grammar) before:",len(original_grammar)
	if eps == True:
		original_grammar = add_eps(original_grammar)
	print "len(original_grammar) after:",len(original_grammar)
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

def get_parse_table(convert=True):
	parse_table =  {'IF_extra': {'>=': 26, 'do': 26, '<=': 26, ':=': 0, 'in': 26, 'array': 0, '!=': 26, 'id': 0, 'if': 0, 'end': 26, 'for': 0, '&': 26, ')': 26, '(': 0, '+': 26, '*': 26, '-': 26, ',': 26, '/': 26, '.': 0, 'to': 26, 'var': 26, ';': 26, ':': 0, 'type': 26, '<': 26, '>': 26, 'function': 26, 'then': 26, 'string': 0, 'nil': 0, 'else': 25, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 26, 'dol': 26, '=': 26, 'while': 0, 'of': 0, '{': 0, '}': 26, '|': 26}, 'VarDec': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 55, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'ExpOR': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 3, 'if': 3, 'end': 0, 'for': 3, '&': 0, ')': 0, '(': 3, '+': 0, '*': 0, '-': 3, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 3, 'nil': 3, 'else': 0, 'break': 3, 'let': 3, 'integer': 3, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 3, 'of': 0, '{': 0, '}': 0, '|': 0}, 'EL_extra': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 75, 'for': 0, '&': 0, ')': 75, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 76, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'FRA_extra1': {'>=': 65, 'do': 65, '<=': 65, ':=': 65, 'in': 65, 'array': 0, '!=': 65, 'id': 0, 'if': 0, 'end': 65, 'for': 0, '&': 65, ')': 65, '(': 0, '+': 65, '*': 65, '-': 65, ',': 65, '/': 65, '.': 65, 'to': 65, 'var': 65, ';': 65, ':': 0, 'type': 65, '<': 65, '>': 65, 'function': 65, 'then': 65, 'string': 0, 'nil': 0, 'else': 65, 'break': 0, 'let': 0, 'integer': 0, '[': 65, ']': 65, 'dol': 65, '=': 65, 'while': 0, 'of': 66, '{': 0, '}': 65, '|': 65}, 'FRAP_extra1': {'>=': 68, 'do': 68, '<=': 68, ':=': 67, 'in': 68, 'array': 0, '!=': 68, 'id': 0, 'if': 0, 'end': 68, 'for': 0, '&': 68, ')': 68, '(': 0, '+': 68, '*': 68, '-': 68, ',': 68, '/': 68, '.': 0, 'to': 68, 'var': 68, ';': 68, ':': 0, 'type': 68, '<': 68, '>': 68, 'function': 68, 'then': 68, 'string': 0, 'nil': 0, 'else': 68, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 68, 'dol': 68, '=': 68, 'while': 0, 'of': 0, '{': 0, '}': 68, '|': 68}, 'RelationOp': {'>=': 86, 'do': 0, '<=': 87, ':=': 0, 'in': 0, 'array': 0, '!=': 83, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 85, '>': 84, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 82, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'AL_extra': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 80, '(': 0, '+': 0, '*': 0, '-': 0, ',': 79, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'FunctionRecordArrayPr': {'>=': 69, 'do': 69, '<=': 69, ':=': 69, 'in': 69, 'array': 0, '!=': 69, 'id': 0, 'if': 0, 'end': 69, 'for': 0, '&': 69, ')': 69, '(': 0, '+': 69, '*': 69, '-': 69, ',': 69, '/': 69, '.': 69, 'to': 69, 'var': 69, ';': 69, ':': 0, 'type': 69, '<': 69, '>': 69, 'function': 69, 'then': 69, 'string': 0, 'nil': 0, 'else': 69, 'break': 0, 'let': 0, 'integer': 0, '[': 69, ']': 69, 'dol': 69, '=': 69, 'while': 0, 'of': 0, '{': 0, '}': 69, '|': 69}, 'DL_extra': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 34, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 33, ';': 0, ':': 0, 'type': 33, '<': 0, '>': 0, 'function': 33, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'Factor': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 31, 'if': 24, 'end': 0, 'for': 28, '&': 0, ')': 0, '(': 22, '+': 0, '*': 0, '-': 23, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 21, 'nil': 19, 'else': 0, 'break': 29, 'let': 30, 'integer': 20, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 27, 'of': 0, '{': 0, '}': 0, '|': 0}, 'Prog': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 1, 'if': 1, 'end': 0, 'for': 1, '&': 0, ')': 0, '(': 1, '+': 0, '*': 0, '-': 1, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 1, 'nil': 1, 'else': 0, 'break': 1, 'let': 1, 'integer': 1, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 1, 'of': 0, '{': 0, '}': 0, '|': 0}, 'FRAP_extra': {'>=': 72, 'do': 72, '<=': 72, ':=': 72, 'in': 72, 'array': 0, '!=': 72, 'id': 0, 'if': 0, 'end': 72, 'for': 0, '&': 72, ')': 72, '(': 0, '+': 72, '*': 72, '-': 72, ',': 72, '/': 72, '.': 70, 'to': 72, 'var': 72, ';': 72, ':': 0, 'type': 72, '<': 72, '>': 72, 'function': 72, 'then': 72, 'string': 0, 'nil': 0, 'else': 72, 'break': 0, 'let': 0, 'integer': 0, '[': 71, ']': 72, 'dol': 72, '=': 72, 'while': 0, 'of': 0, '{': 0, '}': 72, '|': 72}, 'FRA_extra': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 62, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 63, '|': 0}, 'TypeId': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 50, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 52, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 51, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'ArgList': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 78, 'if': 78, 'end': 0, 'for': 78, '&': 0, ')': 77, '(': 78, '+': 0, '*': 0, '-': 78, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 78, 'nil': 78, 'else': 0, 'break': 78, 'let': 78, 'integer': 78, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 78, 'of': 0, '{': 0, '}': 0, '|': 0}, 'FL_extra': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 45, '(': 0, '+': 0, '*': 0, '-': 0, ',': 44, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 45, '|': 0}, 'Ty': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 40, '!=': 0, 'id': 41, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 41, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 41, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 39, '}': 0, '|': 0}, 'ExpANDPr': {'>=': 7, 'do': 7, '<=': 7, ':=': 0, 'in': 7, 'array': 0, '!=': 7, 'id': 0, 'if': 0, 'end': 7, 'for': 0, '&': 6, ')': 7, '(': 0, '+': 7, '*': 7, '-': 7, ',': 7, '/': 7, '.': 0, 'to': 7, 'var': 7, ';': 7, ':': 0, 'type': 7, '<': 7, '>': 7, 'function': 7, 'then': 7, 'string': 0, 'nil': 0, 'else': 7, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 7, 'dol': 7, '=': 7, 'while': 0, 'of': 0, '{': 0, '}': 7, '|': 7}, 'FieldList': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 43, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 42, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 42, '|': 0}, 'RelationExp': {'>=': 10, 'do': 11, '<=': 10, ':=': 0, 'in': 11, 'array': 0, '!=': 10, 'id': 0, 'if': 0, 'end': 11, 'for': 0, '&': 11, ')': 11, '(': 0, '+': 11, '*': 11, '-': 11, ',': 11, '/': 11, '.': 0, 'to': 11, 'var': 11, ';': 11, ':': 0, 'type': 11, '<': 10, '>': 10, 'function': 11, 'then': 11, 'string': 0, 'nil': 0, 'else': 11, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 11, 'dol': 11, '=': 10, 'while': 0, 'of': 0, '{': 0, '}': 11, '|': 11}, 'UnaryOp': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 81, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'FunDec': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 56, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'Term': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 12, 'if': 12, 'end': 0, 'for': 12, '&': 0, ')': 0, '(': 12, '+': 0, '*': 0, '-': 12, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 12, 'nil': 12, 'else': 0, 'break': 12, 'let': 12, 'integer': 12, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 12, 'of': 0, '{': 0, '}': 0, '|': 0}, 'FactorPr': {'>=': 18, 'do': 18, '<=': 18, ':=': 0, 'in': 18, 'array': 0, '!=': 18, 'id': 0, 'if': 0, 'end': 18, 'for': 0, '&': 18, ')': 18, '(': 0, '+': 18, '*': 16, '-': 18, ',': 18, '/': 17, '.': 0, 'to': 18, 'var': 18, ';': 18, ':': 0, 'type': 18, '<': 18, '>': 18, 'function': 18, 'then': 18, 'string': 0, 'nil': 0, 'else': 18, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 18, 'dol': 18, '=': 18, 'while': 0, 'of': 0, '{': 0, '}': 18, '|': 18}, 'Exp': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 2, 'if': 2, 'end': 0, 'for': 2, '&': 0, ')': 0, '(': 2, '+': 0, '*': 0, '-': 2, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 2, 'nil': 2, 'else': 0, 'break': 2, 'let': 2, 'integer': 2, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 2, 'of': 0, '{': 0, '}': 0, '|': 0}, 'ExpList': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 74, 'if': 74, 'end': 73, 'for': 74, '&': 0, ')': 73, '(': 74, '+': 0, '*': 0, '-': 74, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 74, 'nil': 74, 'else': 0, 'break': 74, 'let': 74, 'integer': 74, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 74, 'of': 0, '{': 0, '}': 0, '|': 0}, 'Dec': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 36, ';': 0, ':': 0, 'type': 35, '<': 0, '>': 0, 'function': 37, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'FieldExpList': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 47, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'ExpAND': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 8, 'if': 8, 'end': 0, 'for': 8, '&': 0, ')': 0, '(': 8, '+': 0, '*': 0, '-': 8, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 8, 'nil': 8, 'else': 0, 'break': 8, 'let': 8, 'integer': 8, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 8, 'of': 0, '{': 0, '}': 0, '|': 0}, 'VD_extra': {'>=': 0, 'do': 0, '<=': 0, ':=': 53, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 54, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 53, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'LValue': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 57, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'FEL_extra': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 48, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'TyDec': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 38, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'DecList': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 32, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 32, ';': 0, ':': 0, 'type': 32, '<': 0, '>': 0, 'function': 32, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'ArithExp': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 9, 'if': 9, 'end': 0, 'for': 9, '&': 0, ')': 0, '(': 9, '+': 0, '*': 0, '-': 9, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 9, 'nil': 9, 'else': 0, 'break': 9, 'let': 9, 'integer': 9, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 9, 'of': 0, '{': 0, '}': 0, '|': 0}, 'TermPr': {'>=': 15, 'do': 15, '<=': 15, ':=': 0, 'in': 15, 'array': 0, '!=': 15, 'id': 0, 'if': 0, 'end': 15, 'for': 0, '&': 15, ')': 15, '(': 0, '+': 13, '*': 15, '-': 14, ',': 15, '/': 15, '.': 0, 'to': 15, 'var': 15, ';': 15, ':': 0, 'type': 15, '<': 15, '>': 15, 'function': 15, 'then': 15, 'string': 0, 'nil': 0, 'else': 15, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 15, 'dol': 15, '=': 15, 'while': 0, 'of': 0, '{': 0, '}': 15, '|': 15}, 'LD_extra': {'>=': 58, 'do': 58, '<=': 58, ':=': 58, 'in': 58, 'array': 0, '!=': 58, 'id': 0, 'if': 0, 'end': 58, 'for': 0, '&': 58, ')': 58, '(': 59, '+': 58, '*': 58, '-': 58, ',': 58, '/': 58, '.': 58, 'to': 58, 'var': 58, ';': 58, ':': 0, 'type': 58, '<': 58, '>': 58, 'function': 58, 'then': 58, 'string': 0, 'nil': 0, 'else': 58, 'break': 0, 'let': 0, 'integer': 0, '[': 58, ']': 58, 'dol': 58, '=': 58, 'while': 0, 'of': 0, '{': 59, '}': 58, '|': 58}, 'ExpORPr': {'>=': 5, 'do': 5, '<=': 5, ':=': 0, 'in': 5, 'array': 0, '!=': 5, 'id': 0, 'if': 0, 'end': 5, 'for': 0, '&': 5, ')': 5, '(': 0, '+': 5, '*': 5, '-': 5, ',': 5, '/': 5, '.': 0, 'to': 5, 'var': 5, ';': 5, ':': 0, 'type': 5, '<': 5, '>': 5, 'function': 5, 'then': 5, 'string': 0, 'nil': 0, 'else': 5, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 5, 'dol': 5, '=': 5, 'while': 0, 'of': 0, '{': 0, '}': 5, '|': 4}, 'FunctionRecordArray': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 60, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 64, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 61, '}': 0, '|': 0}}
	parse_table['LD_extra']['[']= 59
	if convert == True:
		parse_table = convert_parse_table(parse_table)
	# print len(parse_table)
	return parse_table

def nums():
	original_grammar = find_original_grammar()
	num_vars = {'num_rules':len(original_grammar), 'size_rules':len(original_grammar[0])-1}
	return num_vars

# accept_strings = [") )"]
# reject_strings = [")", ") ("]
# accept_strings = ["let type of = array of id var id : id := id [ integer ] of integer in id end"]
# get_parse_table()
