from __future__ import print_function
def online_check_format1(original_grammar):
	# mknod("tiger_grammar.txt")
	# tiger = open("tiger_grammar.txt",'w+')
	tmp = []
	prev = None
	for i in range(len(original_grammar)):
		tmp1 = []
		for j in range(len(original_grammar[i])):
			if original_grammar[i][j] == "eps":
				tmp1.append("''")
				continue
			if original_grammar[i][j] == "|":
				tmp1.append("#")
				continue
			if j == 0:
				if prev == original_grammar[i][j]:
					tmp1.append("")
				else:
					tmp1.append(original_grammar[i][j])
					prev = original_grammar[i][j]
			else:
				tmp1.append(original_grammar[i][j])
			if j == 0:
				tmp1.append('->')
		# tmp1.append(".")
		tmp.append(tmp1)
	for  i in range(len(tmp)):
		for j in range(len(tmp[i])):
			if j != len(tmp[i])-1:
				# tiger.write("%s  "%(tmp[i][j]))
				print ("%s"%(tmp[i][j]), end=" ")
			else:
				# tiger.write("%s\n"%(tmp[i][j]))
				print ("%s;"%(tmp[i][j]))
		# print ("saket")


a = [['Prog','Exp'],['Exp','ExpOR','ExpORPr'],['ExpOR','ExpAND','ExpANDPr'],

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
online_check_format1(a)