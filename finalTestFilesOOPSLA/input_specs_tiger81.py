#relop, integer = string, * = /
def specs():

	#Space separated (tokized) strings
	# accept_strings = [let type id = array of id var id : id := id [ integer ] of integer in id end]
	accept_strings = [ ' let type { id : id , id : id } var id : id := integer type id = { id : id , id : id } in id end ' ]
	reject_strings = ["let"]

	config = {
		'num_rules': 91, #Number of rules
		'size_rules' : 5, #Number of symbols in RHS
		'num_nonterms' : 44, #Number of nonterms
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
	original_grammar = [['Prog1','Prog','dol'],['Prog','Exp'],['Exp','ExpOR','ExpORPr'],['ExpOR','ExpAND','ExpANDPr'],

['ExpORPr','|','Exp'],['ExpORPr','eps'],['ExpANDPr','&','ExpOR'],

['ExpANDPr','eps'],['ExpAND','ArithExp','RelationExp'],['ArithExp','Term','TermPr'],

['RelationExp','RelationOp','ArithExp'],['RelationExp','eps'],['Term','Factor','FactorPr'],

['TermPr','+','Term','TermPr'],['TermPr','-','Term','TermPr'],

['TermPr','eps'],['FactorPr','*','Factor','FactorPr'],['FactorPr','/','Factor','FactorPr'],

['FactorPr','eps'],['Factor','nil'],['Factor','integer'],['Factor','string'],

['Factor','(','ExpList',')'],['Factor','UnaryOp','Exp'],['Factor','if','Exp','then','Exp','IF_extra'],['IF_extra','else','Exp'],['IF_extra','eps'],

['Factor','while','Exp','do','Exp'],['Factor','for','id',':=','Exp','F1'],['F1' ,'to','Exp','do','Exp'],['Factor','break'],['Factor','let','DecList','in','ExpList','end'],

['Factor','LValue'],['DecList','DL_extra'],['DL_extra','Dec','DL_extra'],['DL_extra','eps'],

['Dec','TyDec'],['Dec','VarDec'],['Dec','FunDec'],['TyDec','type','TypeId','=','Ty'],['Ty','{','FieldList','}'],['Ty','array','of','TypeId'],['Ty','TypeId'],

['FieldList','eps'],['FieldList','id',':','TypeId','FL_extra'],['FL_extra',',','id',':','TypeId','FL_extra'],['FL_extra','eps'],['FieldExpList','eps'],

['FieldExpList','id','=','Exp','FEL_extra'],['FEL_extra',',','id','=','Exp','FEL_extra'],['FEL_extra','eps'],

['TypeId','id'],['TypeId','integer'],['TypeId','string'],['VD_extra','eps'],['VD_extra',':','TypeId'],['VarDec','var','id','VD_extra',':=','Exp'],

['FunDec','function','id','(','FieldList','F2'],['F2' ,')','VD_extra','=','Exp'],

['LValue','id','LD_extra'],['LD_extra','FunctionRecordArrayPr'],['LD_extra','FunctionRecordArray'],['FunctionRecordArray','(','ArgList',')'],

['FunctionRecordArray','{','id','=','Exp','F3'],['F3','FRA_extra','}'],['FRA_extra',',','id','=','Exp','FRA_extra'],['FRA_extra','eps'],

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
	parse_table =   {'IF_extra': {'>=': 27, 'do': 27, '<=': 27, ':=': 0, 'in': 27, 'array': 0, '!=': 27, 'id': 0, 'if': 0, 'end': 27, 'for': 0, '&': 27, ')': 27, '(': 0, '+': 27, '*': 27, '-': 27, ',': 27, '/': 27, '.': 0, 'to': 27, 'var': 27, ';': 27, ':': 0, 'type': 27, '<': 27, '>': 27, 'function': 27, 'then': 27, 'string': 0, 'nil': 0, 'else': 26, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 27, 'dol': 27, '=': 27, 'while': 0, 'of': 0, '{': 0, '}': 27, '|': 27}, 'VarDec': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 57, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'ExpOR': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 4, 'if': 4, 'end': 0, 'for': 4, '&': 0, ')': 0, '(': 4, '+': 0, '*': 0, '-': 4, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 4, 'nil': 4, 'else': 0, 'break': 4, 'let': 4, 'integer': 4, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 4, 'of': 0, '{': 0, '}': 0, '|': 0}, 'EL_extra': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 79, 'for': 0, '&': 0, ')': 79, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 80, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'FRA_extra1': {'>=': 69, 'do': 69, '<=': 69, ':=': 69, 'in': 69, 'array': 0, '!=': 69, 'id': 0, 'if': 0, 'end': 69, 'for': 0, '&': 69, ')': 69, '(': 0, '+': 69, '*': 69, '-': 69, ',': 69, '/': 69, '.': 69, 'to': 69, 'var': 69, ';': 69, ':': 0, 'type': 69, '<': 69, '>': 69, 'function': 69, 'then': 69, 'string': 0, 'nil': 0, 'else': 69, 'break': 0, 'let': 0, 'integer': 0, '[': 69, ']': 69, 'dol': 69, '=': 69, 'while': 0, 'of': 70, '{': 0, '}': 69, '|': 69}, 'FRAP_extra1': {'>=': 72, 'do': 72, '<=': 72, ':=': 71, 'in': 72, 'array': 0, '!=': 72, 'id': 0, 'if': 0, 'end': 72, 'for': 0, '&': 72, ')': 72, '(': 0, '+': 72, '*': 72, '-': 72, ',': 72, '/': 72, '.': 0, 'to': 72, 'var': 72, ';': 72, ':': 0, 'type': 72, '<': 72, '>': 72, 'function': 72, 'then': 72, 'string': 0, 'nil': 0, 'else': 72, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 72, 'dol': 72, '=': 72, 'while': 0, 'of': 0, '{': 0, '}': 72, '|': 72}, 'RelationOp': {'>=': 90, 'do': 0, '<=': 91, ':=': 0, 'in': 0, 'array': 0, '!=': 87, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 89, '>': 88, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 86, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'AL_extra': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 84, '(': 0, '+': 0, '*': 0, '-': 0, ',': 83, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'FunctionRecordArrayPr': {'>=': 73, 'do': 73, '<=': 73, ':=': 73, 'in': 73, 'array': 0, '!=': 73, 'id': 0, 'if': 0, 'end': 73, 'for': 0, '&': 73, ')': 73, '(': 0, '+': 73, '*': 73, '-': 73, ',': 73, '/': 73, '.': 73, 'to': 73, 'var': 73, ';': 73, ':': 0, 'type': 73, '<': 73, '>': 73, 'function': 73, 'then': 73, 'string': 0, 'nil': 0, 'else': 73, 'break': 0, 'let': 0, 'integer': 0, '[': 73, ']': 73, 'dol': 73, '=': 73, 'while': 0, 'of': 0, '{': 0, '}': 73, '|': 73}, 'DL_extra': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 36, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 35, ';': 0, ':': 0, 'type': 35, '<': 0, '>': 0, 'function': 35, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'Factor': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 33, 'if': 25, 'end': 0, 'for': 29, '&': 0, ')': 0, '(': 23, '+': 0, '*': 0, '-': 24, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 22, 'nil': 20, 'else': 0, 'break': 31, 'let': 32, 'integer': 21, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 28, 'of': 0, '{': 0, '}': 0, '|': 0}, 'Prog': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 2, 'if': 2, 'end': 0, 'for': 2, '&': 0, ')': 0, '(': 2, '+': 0, '*': 0, '-': 2, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 2, 'nil': 2, 'else': 0, 'break': 2, 'let': 2, 'integer': 2, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 2, 'of': 0, '{': 0, '}': 0, '|': 0}, 'FRAP_extra': {'>=': 76, 'do': 76, '<=': 76, ':=': 76, 'in': 76, 'array': 0, '!=': 76, 'id': 0, 'if': 0, 'end': 76, 'for': 0, '&': 76, ')': 76, '(': 0, '+': 76, '*': 76, '-': 76, ',': 76, '/': 76, '.': 74, 'to': 76, 'var': 76, ';': 76, ':': 0, 'type': 76, '<': 76, '>': 76, 'function': 76, 'then': 76, 'string': 0, 'nil': 0, 'else': 76, 'break': 0, 'let': 0, 'integer': 0, '[': 75, ']': 76, 'dol': 76, '=': 76, 'while': 0, 'of': 0, '{': 0, '}': 76, '|': 76}, 'FRA_extra': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 66, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 67, '|': 0}, 'TypeId': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 52, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 54, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 53, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'ArgList': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 82, 'if': 82, 'end': 0, 'for': 82, '&': 0, ')': 81, '(': 82, '+': 0, '*': 0, '-': 82, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 82, 'nil': 82, 'else': 0, 'break': 82, 'let': 82, 'integer': 82, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 82, 'of': 0, '{': 0, '}': 0, '|': 0}, 'FL_extra': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 47, '(': 0, '+': 0, '*': 0, '-': 0, ',': 46, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 47, '|': 0}, 'Ty': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 42, '!=': 0, 'id': 43, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 43, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 43, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 41, '}': 0, '|': 0}, 'ExpANDPr': {'>=': 8, 'do': 8, '<=': 8, ':=': 0, 'in': 8, 'array': 0, '!=': 8, 'id': 0, 'if': 0, 'end': 8, 'for': 0, '&': 7, ')': 8, '(': 0, '+': 8, '*': 8, '-': 8, ',': 8, '/': 8, '.': 0, 'to': 8, 'var': 8, ';': 8, ':': 0, 'type': 8, '<': 8, '>': 8, 'function': 8, 'then': 8, 'string': 0, 'nil': 0, 'else': 8, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 8, 'dol': 8, '=': 8, 'while': 0, 'of': 0, '{': 0, '}': 8, '|': 8}, 'FieldList': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 45, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 44, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 44, '|': 0}, 'RelationExp': {'>=': 11, 'do': 12, '<=': 11, ':=': 0, 'in': 12, 'array': 0, '!=': 11, 'id': 0, 'if': 0, 'end': 12, 'for': 0, '&': 12, ')': 12, '(': 0, '+': 12, '*': 12, '-': 12, ',': 12, '/': 12, '.': 0, 'to': 12, 'var': 12, ';': 12, ':': 0, 'type': 12, '<': 11, '>': 11, 'function': 12, 'then': 12, 'string': 0, 'nil': 0, 'else': 12, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 12, 'dol': 12, '=': 11, 'while': 0, 'of': 0, '{': 0, '}': 12, '|': 12}, 'UnaryOp': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 85, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'FunDec': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 58, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'Term': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 13, 'if': 13, 'end': 0, 'for': 13, '&': 0, ')': 0, '(': 13, '+': 0, '*': 0, '-': 13, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 13, 'nil': 13, 'else': 0, 'break': 13, 'let': 13, 'integer': 13, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 13, 'of': 0, '{': 0, '}': 0, '|': 0}, 'VD_extra': {'>=': 0, 'do': 0, '<=': 0, ':=': 55, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 56, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 55, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'FactorPr': {'>=': 19, 'do': 19, '<=': 19, ':=': 0, 'in': 19, 'array': 0, '!=': 19, 'id': 0, 'if': 0, 'end': 19, 'for': 0, '&': 19, ')': 19, '(': 0, '+': 19, '*': 17, '-': 19, ',': 19, '/': 18, '.': 0, 'to': 19, 'var': 19, ';': 19, ':': 0, 'type': 19, '<': 19, '>': 19, 'function': 19, 'then': 19, 'string': 0, 'nil': 0, 'else': 19, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 19, 'dol': 19, '=': 19, 'while': 0, 'of': 0, '{': 0, '}': 19, '|': 19}, 'Exp': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 3, 'if': 3, 'end': 0, 'for': 3, '&': 0, ')': 0, '(': 3, '+': 0, '*': 0, '-': 3, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 3, 'nil': 3, 'else': 0, 'break': 3, 'let': 3, 'integer': 3, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 3, 'of': 0, '{': 0, '}': 0, '|': 0}, 'ExpList': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 78, 'if': 78, 'end': 77, 'for': 78, '&': 0, ')': 77, '(': 78, '+': 0, '*': 0, '-': 78, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 78, 'nil': 78, 'else': 0, 'break': 78, 'let': 78, 'integer': 78, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 78, 'of': 0, '{': 0, '}': 0, '|': 0}, 'Dec': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 38, ';': 0, ':': 0, 'type': 37, '<': 0, '>': 0, 'function': 39, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'FieldExpList': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 49, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'ExpAND': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 9, 'if': 9, 'end': 0, 'for': 9, '&': 0, ')': 0, '(': 9, '+': 0, '*': 0, '-': 9, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 9, 'nil': 9, 'else': 0, 'break': 9, 'let': 9, 'integer': 9, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 9, 'of': 0, '{': 0, '}': 0, '|': 0}, 'Prog1': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 1, 'if': 1, 'end': 0, 'for': 1, '&': 0, ')': 0, '(': 1, '+': 0, '*': 0, '-': 1, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 1, 'nil': 1, 'else': 0, 'break': 1, 'let': 1, 'integer': 1, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 1, 'of': 0, '{': 0, '}': 0, '|': 0}, 'F1': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 30, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'F2': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 59, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'F3': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 65, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 65, '|': 0}, 'DecList': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 34, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 34, ';': 0, ':': 0, 'type': 34, '<': 0, '>': 0, 'function': 34, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'TyDec': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 40, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'FEL_extra': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 50, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'ArithExp': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 10, 'if': 10, 'end': 0, 'for': 10, '&': 0, ')': 0, '(': 10, '+': 0, '*': 0, '-': 10, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 10, 'nil': 10, 'else': 0, 'break': 10, 'let': 10, 'integer': 10, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 10, 'of': 0, '{': 0, '}': 0, '|': 0}, 'LValue': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 60, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 0, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 0, '}': 0, '|': 0}, 'TermPr': {'>=': 16, 'do': 16, '<=': 16, ':=': 0, 'in': 16, 'array': 0, '!=': 16, 'id': 0, 'if': 0, 'end': 16, 'for': 0, '&': 16, ')': 16, '(': 0, '+': 14, '*': 16, '-': 15, ',': 16, '/': 16, '.': 0, 'to': 16, 'var': 16, ';': 16, ':': 0, 'type': 16, '<': 16, '>': 16, 'function': 16, 'then': 16, 'string': 0, 'nil': 0, 'else': 16, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 16, 'dol': 16, '=': 16, 'while': 0, 'of': 0, '{': 0, '}': 16, '|': 16}, 'LD_extra': {'>=': 61, 'do': 61, '<=': 61, ':=': 61, 'in': 61, 'array': 0, '!=': 61, 'id': 0, 'if': 0, 'end': 61, 'for': 0, '&': 61, ')': 61, '(': 62, '+': 61, '*': 61, '-': 61, ',': 61, '/': 61, '.': 61, 'to': 61, 'var': 61, ';': 61, ':': 0, 'type': 61, '<': 61, '>': 61, 'function': 61, 'then': 61, 'string': 0, 'nil': 0, 'else': 61, 'break': 0, 'let': 0, 'integer': 0, '[': 61, ']': 61, 'dol': 61, '=': 61, 'while': 0, 'of': 0, '{': 62, '}': 61, '|': 61}, 'ExpORPr': {'>=': 6, 'do': 6, '<=': 6, ':=': 0, 'in': 6, 'array': 0, '!=': 6, 'id': 0, 'if': 0, 'end': 6, 'for': 0, '&': 6, ')': 6, '(': 0, '+': 6, '*': 6, '-': 6, ',': 6, '/': 6, '.': 0, 'to': 6, 'var': 6, ';': 6, ':': 0, 'type': 6, '<': 6, '>': 6, 'function': 6, 'then': 6, 'string': 0, 'nil': 0, 'else': 6, 'break': 0, 'let': 0, 'integer': 0, '[': 0, ']': 6, 'dol': 6, '=': 6, 'while': 0, 'of': 0, '{': 0, '}': 6, '|': 5}, 'FunctionRecordArray': {'>=': 0, 'do': 0, '<=': 0, ':=': 0, 'in': 0, 'array': 0, '!=': 0, 'id': 0, 'if': 0, 'end': 0, 'for': 0, '&': 0, ')': 0, '(': 63, '+': 0, '*': 0, '-': 0, ',': 0, '/': 0, '.': 0, 'to': 0, 'var': 0, ';': 0, ':': 0, 'type': 0, '<': 0, '>': 0, 'function': 0, 'then': 0, 'string': 0, 'nil': 0, 'else': 0, 'break': 0, 'let': 0, 'integer': 0, '[': 68, ']': 0, 'dol': 0, '=': 0, 'while': 0, 'of': 0, '{': 64, '}': 0, '|': 0}}
	parse_table['LD_extra']['[']= 62
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
