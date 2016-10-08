from __future__ import print_function 
from collections import *
# from os import mknod
def specs():

	#Space separated (tokized) strings
	# accept_strings = ["?", "! ?", "( ?"]
	accept_strings = ["( ? ) ?"]
	reject_strings = [")", ") ("]

	config = {
		'num_rules': 6, #Number of rules
		'size_rules' : 4, #Number of symbols in RHS
		'num_nonterms' : 4, #Number of nonterms
		'expansion_constant' : 6, #Determines the max. number of parse actions to take while parsing
		'optimize' : False, # enable optimized mode
		'neg_egs' : True, # consider negative examples 
		'threshold' : 0.2  # number of unsat cores to break
	}

	return accept_strings,reject_strings,config

def find_original_grammar():
	original_grammar = [['S','eps','eps','F','S'], ['S','eps','eps','eps','Q'], ['S','(','S',')','S'], ['F','eps','eps','!','A'], ['Q','eps','eps','?','A'],['A','eps','eps','eps','eps']]
	return original_grammar
	# original_grammar = [['N1',')','(',')','N2'],['N1','(','?',')','?'],['N4','eps','eps','eps','eps'],['N2','N4','N4','(','N2'],['N3','N4','?','(','('],['N2','eps','N3',')','(']]
	# return original_grammar

def get_parse_table():
	parse_table = [{'non_term':'S' ,'(':3 ,')':0 ,'!':1 ,'?':2 ,'$':0},{'non_term':'F' ,'(':0 ,')':0 ,'!':4 ,'?':0 ,'$':0},{'non_term':'Q' ,'(':0 ,')':0 ,'!':0 ,'?':5 ,'$':0},{'non_term':'A' ,'(':6 ,')':6 ,'!':6 ,'?':6 ,'$':6}]
	# parse_table = [{'non_term':'N1','(':2, '?':0, ')':1, '$':0},{'non_term':'N4','(':3, '?':3, ')':0, '$':0},{'non_term':'N2','(':4, '?':6, ')':0, '$':0},{'non_term':'N3','(':0, '?':5, ')':0, '$':0}]
	return parse_table

def nums():
	original_grammar = find_original_grammar()
	num_vars = {'num_rules':len(original_grammar), 'size_rules':len(original_grammar[0])-1}
	return num_vars

def get_first_set():
	first_set = [{'non_term':'S' ,'(':1 ,')':0 ,'!':1 ,'?':1 ,'eps':0},{'non_term':'F' ,'(':0 ,')':0 ,'!':1 ,'?':0 ,'eps':0},{'non_term':'Q' ,'(':0 ,')':0 ,'!':0 ,'?':1 ,'eps':0},{'non_term':'A' ,'(':0 ,')':0 ,'!':0 ,'?':0 ,'eps':1}]
	return first_set

def get_follow_set():
	follow_set = [{'non_term':'S' ,'(':0 ,')':1 ,'!':0 ,'?':0 ,'$':1},{'non_term':'F' ,'(':1 ,')':0 ,'!':1 ,'?':1 ,'$':0},{'non_term':'Q' ,'(':0 ,')':1 ,'!':0 ,'?':0 ,'$':1},{'non_term':'A' ,'(':1 ,')':1 ,'!':1 ,'?':1 ,'$':1}]
	return follow_set

# accept_strings = ["?", "! ?", "( ?"]
accept_strings = ["( )"]
reject_strings = [")", ") ("]

##	S -> (S)S | eps
##
def convert_grammar(original_grammar):
	tmp1 = []
	for i in range(len(original_grammar)):
		tmp = []
		n = len(original_grammar[i])
		tmp.append(original_grammar[i][0])
		for j in range(1,9-n+1):
			tmp.append("eps")
		for j in range(1,n):
			tmp.append(original_grammar[i][j])
		tmp1.append(tmp)
	# print "tmp1  ",tmp1
	return tmp1

def online_check_hacking(original_grammar):
	tmp = []
	for i in range(len(original_grammar)):
		tmp1 = []
		for j in range(len(original_grammar[i])):
			if j == 1:
				tmp1.append("->")
			if original_grammar[i][j] == "eps":
				tmp1.append("EPSILON")
				continue
			if original_grammar[i][j] == "|":
				tmp1.append("#")
				continue
			tmp1.append(original_grammar[i][j])
		tmp.append(tmp1)
	for  i in range(len(tmp)):
		for j in range(len(tmp[i])):
			if j != len(tmp[i])-1:
				print ("%s"%(tmp[i][j]), end=" ")
			else:
				print ("%s"%(tmp[i][j]))
def online_check_format1(original_grammar):
	# mknod("tiger_grammar.txt")
	# tiger = open("tiger_grammar.txt",'w+')
	tmp = []
	for i in range(len(original_grammar)):
		tmp1 = []
		for j in range(len(original_grammar[i])):
			if original_grammar[i][j] == "eps":
				tmp1.append("''")
				continue
			if original_grammar[i][j] == "|":
				tmp1.append("#")
				continue
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
				print ("%s"%(tmp[i][j]))
		# print ("")
def online_check_format2(original_grammar):
	tmp =[]
	for i in range(len(original_grammar)):
		tmp1 = []
		for j in range(len(original_grammar[i])):
			if original_grammar[i][j] == "eps":
				continue
			if original_grammar[i][j] == "|":
				tmp1.append("#")
				continue
			if original_grammar[i][j] == ".":
				tmp1.append("@")
				continue
			tmp1.append(original_grammar[i][j])
			if j == 0:
				tmp1.append("->")
		if len(tmp1) == 2:
			tmp1.append(" ")
		tmp1.append(".")
		tmp.append(tmp1)
	for i in range(len(tmp)):
		for j in range(len(tmp[i])):
			if j == len(tmp[i])-2:
				print(tmp[i][j],end="")
			else:
				print(tmp[i][j],end=" ")
			if j == len(tmp[i])-1:
				print("")

tmp =[["Prog","Exp"],["Exp","ExpOR","ExpORPr"],["ExpOR","ExpAND","ExpANDPr"],["ExpAND","ArithExp","RelExp"],["ExpORPr","|","Exp"],["ExpORPr","eps"],["ExpANDPr","&",'ExpOR'],['ExpANDPr','eps'],['ArithExp',"Term","TermPr"],["RelExp","RelationOp","ArithExp"],["RelExp","eps"],["Term","Factor","FactorPr"],["TermPr","+","Term","TermPr"],["TermPr","-","Term","TermPr"],["TermPr","eps"],["FactorPr","*","Factor","FactorPr"],["FactorPr","/","Factor","FactorPr"],["FactorPr","eps"],["Factor","nil"],["Factor","integer"],["Factor","string"],["Factor","(","ExpList",")"],["Factor","UnaryOp","Exp"],["Factor","if","Exp","then","Exp","Factor1"],["Factor1","else","Exp"],["Factor1","eps"],["Factor","while","Exp","do","Exp"],["Factor","for","id",":=","Exp","to","Exp","do","Exp"],["Factor","break"],["Factor","let","DecList","in","ExpList","end"],["Factor","LValue"],["Dec1","Dec","Dec1"],["Dec1","eps"],["DecList","Dec1"],["Dec","TyDec"],["Dec","VarDec"],["Dec","FunDec"],["TyDec","type","TypeId","=","Ty"],["Ty","{","FieldList","}"],["Ty","array","of","TypeId"],["Ty","TypeId"],["extra1",",","id",":","TypeId","extra1"],["extra1","eps"],["FieldList","id",":","TypeId","extra1"],["FieldList","eps"],["extra2",",","id","=","Exp","extra2"],["extra2","eps"],["FieldExpList","id","=","Exp","extra2"],["FieldExpList","eps"],["TypeId","id"],["TypeId","string"],["TypeId","int"],["VarDec","var","id","extra3",":=","Exp"],["extra3",":","TypeId"],["extra3","eps"],["FunDec","function","id","(","FieldList",")","extra3","=","Exp"],["LValue","id","extra4"],["extra4","FunctionRecordArray"],["extra4","FunctionRecordArrayPr"],["FunctionRecordArray","(","ArgList",")"],["FunctionRecordArray","{","id","=","Exp","extra2","}"],["FunctionRecordArray","[","Exp","]","extra15"],["extra15","of","Exp"],["extra15","FunctionRecordArrayPr"],["FunctionRecordArrayPr","extra11","extra12","extra13"],["extra11",".","id","extra11"],["extra11","eps"],["extra12","[","Exp","]","extra12"],["extra12","eps"],["extra13","Assign","Exp"],["extra13","eps"],["ExpList","Exp","extra7"],["ExpList","eps"],["extra7",";","Exp","extra7"],["extra7","eps"],["ArgList","Exp","extra6"],["ArgList","eps"],["extra6",",","Exp","extra6"],["extra6","eps"],["UnaryOp","-"],["RelationOp","="],["RelationOp","<>"],["RelationOp",">"],["RelationOp","<"],["RelationOp",">="],["RelationOp","<="]]


online_check_format1(find_original_grammar())
# online_check_hacking(tmp)
# online_check_format1(find_original_grammar())