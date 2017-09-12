from z3 import *
from solver import *
from init import *
from itertools import *
from input_specs_tiger import specs
from parser import parser_main
from parser_verify import parser_main1
from copy import deepcopy
import pickle
from msat import *
import subprocess as sbp
import calendar
import time
import datetime
def dumpSMT(f):
	v = (Ast * 0)()
	a = f.assertions()
	f = And(*a)
	return Z3_benchmark_to_smtlib_string(f.ctx_ref(), "","", "","",0,v,f.as_ast())

def print_grammar(solver):

	m = solver["model"]
	m_vars = solver["vars"]
	m_funs = solver["functions"]

	num_rules = config['num_rules']
	num_nonterms = config['num_nonterms']
	num_terms = config['num_terms']
	size_rules = config['size_rules']

	rules = req_rules(solver)

	for i in range(num_rules):
		if rules[i]:
			symbolValue = int(str(m.evaluate(m_funs["symbolInLHS"](i+1))))
			print "N%d\t->\t"%(symbolValue+1),
			for j in range(size_rules):
				symbolValue = int(str(m.evaluate(m_funs["symbolInRHS"](i+1,j+1))))
				if symbolValue < num_nonterms:
					print "N%d\t"%(symbolValue+1),
				elif symbolValue < num_nonterms + num_terms:
					print "%s\t"%(tokens[symbolValue-num_nonterms]),
				elif symbolValue == num_nonterms + num_terms:
					print "dol\t",
				elif symbolValue == num_nonterms + num_terms + 1:
					print "eps\t",
			print ""

	if solver["comment_out"] == True:
		accept_list = solver["accept_list"]
		print "accept_list ",accept_list
		i = -1
		# while i < len(accept_list[0]):
		print "corrected string saket: "
		tmp = []
		while True:
			symbolValue = int(str(m.evaluate(m_funs["ip_str1"](1, m_funs["succ"](1,i)))))
			if symbolValue >= solver["term_end"]:
				# parser.parser_main(tmp)
				return tmp
			print "%s "%(tokens[symbolValue-num_nonterms]),
			tmp.append("%s"%(tokens[symbolValue-num_nonterms]))
			# print "tmp:",tmp
			i = int(str(m.evaluate(m_funs["succ"](1,i))))
		print ""

def final_string(test_counter, accept_string, suspicious_locations, view_assign_t):
	print "Accept string in final string initially:",accept_string
	first = test_counter[0]
############### For 2 errors ###########################################################
#	second = test_counter[1]
#	flag = 0
#	for i in range(len(accept_string)):
#		accept_string[i] = view_assign_t[accept_string[i]]
#	for i in range(len(suspicious_locations[first])):
#		for j in range(len(suspicious_locations[second])):
#			accept_string[first] = view_assign_t[suspicious_locations[first][i]]
#			accept_string[second] = view_assign_t[suspicious_locations[second][j]]
#			tmp = deepcopy(accept_string)
#			flag = parser_main1(tmp)
#			if flag == 1:
#				return 1
#	return 0
############### For 1 error ############################################################
	for i in range(len(accept_string)):
		accept_string[i] = view_assign_t[accept_string[i]]
	for i in range(len(suspicious_locations[first])):
		print "calling the parser iteration:",i
		tmp =  view_assign_t[suspicious_locations[first][i]]
		correct_string = []
		for k in range(len(accept_string)):
			if k == first:
				correct_string.append(accept_string[k])
				correct_string.append(tmp)
				continue
			correct_string.append(accept_string[k])
		tmp = []
		for i in range(len(correct_string)):
			tmp.append(correct_string[i])
		flag = parser_main1(tmp)
		if flag == 1:
			print "parsed successfully"
			print "returning string",accept_string
			return 1
	print "parse error:",accept_string
	return 0

def find_errors(solver, accept_string):
	############################################
	pkl_file = open("tigerTableUpdated1.pkl","rb")
	ngrams = pickle.load(pkl_file)
	pkl_file.close()

	############################################
	# string = string.split()
	string = accept_strings[0]
        print "String in helpers:", string
        i = open("ex_file.tig","w")
        i.write(string)
        i.close()
	string = string.split()
	print "STRING :", string
	tmp = []
	for i in range(len(string)):
		if i != 0:
			t1 = (string[i-1],string[i])
			if t1 == ("let","type") or t1 == ("let","var"):
				continue
			if t1 not in ngrams:
				tmp.append(i)
				continue
			f1 = ngrams[t1]
			if f1 < 10:
				tmp.append(i)
		if i != len(string)-1:
			t1 = (string[i],string[i+1])
			if t1 == ("let","type") or t1 == ("let","var"):
				continue
			if t1 not in ngrams:
				tmp.append(i)
				continue
			f1 = ngrams[t1]
			if f1 < 10:
				tmp.append(i)
	tmp = find_final_errors(solver, tmp, accept_string)
	return [tmp]

def find_errors_compiler(solver, accept_string):
        string = solver["A_string"][0]
        i = open("ex_file.tig","w")
        i.write(string)
        i.close()
        sbp.call("java TigerParser ex_file.tig > out.txt", shell=True)
        k = 0
        out = open("out.txt")
        prev = None
        curr = None
        for line in out:
            prev = curr
            curr = line
            k += 1
        print("prev:",prev)
        print("curr:", curr)
        if k != 2:
            error = prev.split()
            error = int(error[0])
        er = []
        error -= 1
        solver["compiler_returned_error_location"] = error
        for j in range(error-3,error+3):
            if j >= 0 and j < len(accept_string):
                er.append(j)
        print("Error:",error)
        #er = find_final_errors(solver, er, accept_string)
        print "er:",er
        solver["vtime"] = 0
        return [error]

def parse_output(ka,n,p):

	output_file = open("model.txt")
	lines = output_file.readlines()
	if lines[1] == "unsat\n":
		return -1
	cp = []
	for i in range(n):
		tmp = lines[2+i].split(")")
		cp.append(int(tmp[1]))
	for i in range(n):
		#print lines[2+n+i].split()
		#if(lines[2+n+i].split()[1]
		cp.append(int(lines[2+n+i].split()[1].split(")")[0]))
	# cp.append(int(lines[5].split()[1].split(")")[0]))
	for i in range(10*p):
		tmp = lines[2+2*n+i].split(")")
		cp.append(int(tmp[1]))
	return cp

def add_accept_string(solver,accept_string):

	s = solver["constraints"]
	vars = solver["vars"]
	functions = solver["functions"]
	terms = solver["terms"]
	if "type" in solver:
		assert(solver["type"]=="accept")
		if "num_strings" not in solver:
			solver["num_strings"] = 1
		else:
			solver["num_strings"] += 1
	else:
		solver["type"]="accept"
		assert("num_strings" not in solver)
		solver["num_strings"] = 1

	expansion_constant = config['expansion_constant']  #Determines the max. number of parse actions to take while parsing

	strNum = solver["num_strings"]
	view_assign = solver["view_assign"]
	view_assign_t = solver["view_assign_t"]

	###################################################################################################
	rn = Int('rn')
	x,X0,X1,X2,X3,X4,X5,X6 = Ints('x X0 X1 X2 X3 X4 X5 X6')
	vars["xn"] = x
	vars["X1"],vars["X2"],vars["X3"],vars["X4"],vars["X5"],vars["X6"],vars["rn"] = X1,X2,X3,X4,X5,X6,rn
	lim = expansion_constant*len(accept_string)
	s.add(ForAll([rn,X0,X1,X2,X3,X4,X5,X6],Implies( And(0<=X0,X0<=X1,X1<=X2,X2<=X3,X3<=X4,X4<=X5,X5<=X6,X6<=lim),functions["hardcode"](rn,X0,X1,X2,X3,X4,X5,X6) == Or(And (rn == vars["rule1"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Prog1"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Prog"]] ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["dol"]] ),And (rn == vars["rule2"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Prog"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["Exp"]] ),And (rn == vars["rule3"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Exp"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["ExpOR"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["ExpORPr"]] ),And (rn == vars["rule4"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["ExpOR"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["ExpAND"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["ExpANDPr"]] ),And (rn == vars["rule5"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["ExpORPr"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["|"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["Exp"]] ),And (rn == vars["rule6"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["ExpORPr"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule7"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["ExpANDPr"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["&"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["ExpOR"]] ),And (rn == vars["rule8"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["ExpANDPr"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule9"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["ExpAND"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["ArithExp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["RelationExp"]] ),And (rn == vars["rule10"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["ArithExp"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Term"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["TermPr"]] ),And (rn == vars["rule11"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["RelationExp"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["RelationOp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["ArithExp"]] ),And (rn == vars["rule12"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["RelationExp"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule13"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Term"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Factor"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FactorPr"]] ),And (rn == vars["rule14"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["TermPr"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["+"]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Term"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["TermPr"]] ),And (rn == vars["rule15"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["TermPr"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["-"]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Term"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["TermPr"]] ),And (rn == vars["rule16"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["TermPr"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule17"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FactorPr"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["*"]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Factor"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FactorPr"]] ),And (rn == vars["rule18"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FactorPr"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["/"]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Factor"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FactorPr"]] ),And (rn == vars["rule19"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FactorPr"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule20"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Factor"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["nil"]] ),And (rn == vars["rule21"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Factor"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["integer"]] ),And (rn == vars["rule22"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Factor"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["string"]] ),And (rn == vars["rule23"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Factor"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["("]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["ExpList"]] ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign[")"]] ),And (rn == vars["rule24"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Factor"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["UnaryOp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["Exp"]] ),And (rn == vars["rule25"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Factor"]], X1 == X0+1, X2 == X1+1, functions["end"](strNum, X1) == X1, functions["symbolAt"](strNum, X1) == vars[view_assign["if"]] ,functions["end"](strNum, X2)+1 == X3, functions["symbolAt"](strNum, X2) == vars[view_assign["Exp"]] ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["then"]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Exp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["IF_extra"]] ),And (rn == vars["rule26"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["IF_extra"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["else"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["Exp"]] ),And (rn == vars["rule27"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["IF_extra"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule28"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Factor"]], X1 == X0+1, X1 == X2 ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["while"]] ,functions["end"](strNum, X3)+1 == X4, functions["symbolAt"](strNum, X3) == vars[view_assign["Exp"]] ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["do"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["Exp"]] ),And (rn == vars["rule29"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Factor"]], X1 == X0+1, X2 == X1+1, functions["end"](strNum, X1) == X1, functions["symbolAt"](strNum, X1) == vars[view_assign["for"]] ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["id"]] ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign[":="]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Exp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["F1"]] ),And (rn == vars["rule30"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["F1"]], X1 == X0+1, X1 == X2 ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["to"]] ,functions["end"](strNum, X3)+1 == X4, functions["symbolAt"](strNum, X3) == vars[view_assign["Exp"]] ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["do"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["Exp"]] ),And (rn == vars["rule31"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Factor"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["break"]] ),And (rn == vars["rule32"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Factor"]], X1 == X0+1, X2 == X1+1, functions["end"](strNum, X1) == X1, functions["symbolAt"](strNum, X1) == vars[view_assign["let"]] ,functions["end"](strNum, X2)+1 == X3, functions["symbolAt"](strNum, X2) == vars[view_assign["DecList"]] ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["in"]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["ExpList"]] ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["end"]] ),And (rn == vars["rule33"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Factor"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["LValue"]] ),And (rn == vars["rule34"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["DecList"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["DL_extra"]] ),And (rn == vars["rule35"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["DL_extra"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Dec"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["DL_extra"]] ),And (rn == vars["rule36"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["DL_extra"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule37"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Dec"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["TyDec"]] ),And (rn == vars["rule38"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Dec"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["VarDec"]] ),And (rn == vars["rule39"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Dec"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FunDec"]] ),And (rn == vars["rule40"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["TyDec"]], X1 == X0+1, X1 == X2 ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["type"]] ,functions["end"](strNum, X3)+1 == X4, functions["symbolAt"](strNum, X3) == vars[view_assign["TypeId"]] ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["="]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["Ty"]] ), \
		And (rn == vars["rule41"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Ty"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["{"]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["FieldList"]] ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["}"]] ),And (rn == vars["rule42"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Ty"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["array"]] ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["of"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["TypeId"]] ),And (rn == vars["rule43"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Ty"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["TypeId"]] ),And (rn == vars["rule44"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FieldList"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule45"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FieldList"]], X1 == X0+1, X1 == X2 ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["id"]] ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign[":"]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["TypeId"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FL_extra"]] ),And (rn == vars["rule46"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FL_extra"]], X1 == X0+1, X2 == X1+1, functions["end"](strNum, X1) == X1, functions["symbolAt"](strNum, X1) == vars[view_assign[","]] ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["id"]] ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign[":"]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["TypeId"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FL_extra"]] ),And (rn == vars["rule47"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FL_extra"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ), \
		And (rn == vars["rule48"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FieldExpList"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule49"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FieldExpList"]], X1 == X0+1, X1 == X2 ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["id"]] ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["="]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Exp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FEL_extra"]] ),And (rn == vars["rule50"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FEL_extra"]], X1 == X0+1, X2 == X1+1, functions["end"](strNum, X1) == X1, functions["symbolAt"](strNum, X1) == vars[view_assign[","]] ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["id"]] ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["="]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Exp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FEL_extra"]] ),And (rn == vars["rule51"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FEL_extra"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule52"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["TypeId"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["id"]] ),And (rn == vars["rule53"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["TypeId"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["integer"]] ),And (rn == vars["rule54"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["TypeId"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["string"]] ),And (rn == vars["rule55"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["VD_extra"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule56"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["VD_extra"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign[":"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["TypeId"]] ),And (rn == vars["rule57"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["VarDec"]], X1 == X0+1, X2 == X1+1, functions["end"](strNum, X1) == X1, functions["symbolAt"](strNum, X1) == vars[view_assign["var"]] ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["id"]] ,functions["end"](strNum, X3)+1 == X4, functions["symbolAt"](strNum, X3) == vars[view_assign["VD_extra"]] ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign[":="]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["Exp"]] ),And (rn == vars["rule58"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FunDec"]], X1 == X0+1, X2 == X1+1, functions["end"](strNum, X1) == X1, functions["symbolAt"](strNum, X1) == vars[view_assign["function"]] ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["id"]] ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["("]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["FieldList"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["F2"]] ),And (rn == vars["rule59"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["F2"]], X1 == X0+1, X1 == X2 ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign[")"]] ,functions["end"](strNum, X3)+1 == X4, functions["symbolAt"](strNum, X3) == vars[view_assign["VD_extra"]] ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["="]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["Exp"]] ),And (rn == vars["rule60"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["LValue"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["id"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["LD_extra"]] ),And (rn == vars["rule61"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["LD_extra"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FunctionRecordArrayPr"]] ),And (rn == vars["rule62"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["LD_extra"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FunctionRecordArray"]] ),And (rn == vars["rule63"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FunctionRecordArray"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["("]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["ArgList"]] ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign[")"]] ),And (rn == vars["rule64"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FunctionRecordArray"]], X1 == X0+1, X2 == X1+1, functions["end"](strNum, X1) == X1, functions["symbolAt"](strNum, X1) == vars[view_assign["{"]] ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["id"]] ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["="]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Exp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["F3"]] ),And (rn == vars["rule65"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["F3"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["FRA_extra"]] ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["}"]] ),And (rn == vars["rule66"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FRA_extra"]], X1 == X0+1, X2 == X1+1, functions["end"](strNum, X1) == X1, functions["symbolAt"](strNum, X1) == vars[view_assign[","]] ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["id"]] ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["="]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Exp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FRA_extra"]] ), \
		And (rn == vars["rule67"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FRA_extra"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule68"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FunctionRecordArray"]], X1 == X0+1, X1 == X2 ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["["]] ,functions["end"](strNum, X3)+1 == X4, functions["symbolAt"](strNum, X3) == vars[view_assign["Exp"]] ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["]"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FRA_extra1"]] ),And (rn == vars["rule69"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FRA_extra1"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FunctionRecordArrayPr"]] ),And (rn == vars["rule70"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FRA_extra1"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["of"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["Exp"]] ),And (rn == vars["rule71"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FRAP_extra1"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign[":="]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["Exp"]] ),And (rn == vars["rule72"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FRAP_extra1"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule73"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FunctionRecordArrayPr"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["FRAP_extra"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FRAP_extra1"]] ),And (rn == vars["rule74"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FRAP_extra"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["."]] ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["id"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FRAP_extra"]] ),And (rn == vars["rule75"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FRAP_extra"]], X1 == X0+1, X1 == X2 ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["["]] ,functions["end"](strNum, X3)+1 == X4, functions["symbolAt"](strNum, X3) == vars[view_assign["Exp"]] ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["]"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FRAP_extra"]] ),And (rn == vars["rule76"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FRAP_extra"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule77"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["ExpList"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule78"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["ExpList"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Exp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["EL_extra"]] ),And (rn == vars["rule79"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["EL_extra"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule80"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["EL_extra"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign[";"]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Exp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["EL_extra"]] ),And (rn == vars["rule81"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["ArgList"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule82"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["ArgList"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Exp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["AL_extra"]] ),And (rn == vars["rule83"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["AL_extra"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign[","]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Exp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["AL_extra"]] ), \
		And (rn == vars["rule84"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["AL_extra"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule85"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["UnaryOp"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["-"]] ),And (rn == vars["rule86"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["RelationOp"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["="]] ),And (rn == vars["rule87"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["RelationOp"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["!="]] ),And (rn == vars["rule88"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["RelationOp"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign[">"]] ),And (rn == vars["rule89"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["RelationOp"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["<"]] ),And (rn == vars["rule90"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["RelationOp"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign[">="]] ),And (rn == vars["rule91"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["RelationOp"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["<="]] ))), patterns=[functions["hardcode"](rn,X0,X1,X2,X3,X4,X5,X6)]))

	s.add(functions["end"](strNum,0) > 2)

	for i in range(len(accept_string)+1):
		vars["z%d"%i] = Int('z%d'%i)
	solver["lastz"] = len(accept_string)
	s.add(vars["z0"] > 0)
	s.add(vars["z1"] >= vars["z0"])

	vars["in_extra"] = Int("in_extra")

	# add this constraints for in_xtra too
	for i in range(len(accept_string)+1):
		OrList = []
		for t in terms+["dol"]:
			OrList.append(vars[t] == functions["symbolAt"](strNum,vars["z%d"%i]))
		s.add(Or(OrList))
	OrList = []

	# adding the constraint for extra variable
	for t in terms+["dol"]:
		OrList.append(functions["symbolAt"](strNum,vars["in_extra"]) == vars[t])
	s.add(Or(OrList))

	# for i in range(len(accept_string)):
	# 	s.add(functions["symbolAt"](strNum,vars["z%d"%i]) == vars[accept_string[i]])
	s.add(functions["end"](strNum, 0) <= expansion_constant*len(accept_string))
	s.add(functions["symbolAt"](strNum,0) == vars["N1"])

	for i  in range(expansion_constant*len(accept_string)):
		s.add(functions["valid"](i))

	####################################################################################################
	s.add(functions["lookAheadIndex"](strNum,0) == vars["z0"])
	end_index = 0 # used to count the number f deletions done, as the indices in the test_counter after the deletion will change
	in_index = 0
	COUNT = 0
	insertion_done = False
	deletion_done = False
	#test_counter = find_errors(solver, accept_string)
        test_counter = find_errors_compiler(solver, accept_string)
	test_counter1 = find_test_counter()
        solver["actual_error_location"] = test_counter1[0]
	if test_counter1[0] == test_counter[0]:
		solver["scorrect"] = 1
	else:
		solver["scorrect"] = 0
	if test_counter[0] == -1:
		return 0
	print "Original Error Location:",test_counter1
	print "Returned Error Lcation:",test_counter
	# test_counter = [test_counter,18]
	suspicious_locations = {}
	for key in test_counter:
		suspicious_locations[key] = []
	print "Suspicious Locations Keys:"
	for key in suspicious_locations:
		print key
	print "TEST COUNTER:",test_counter
	testvar = Int('testvar')
	for test_counter_i in range(len(test_counter)):
		p = test_counter[test_counter_i]
		print "Correcting the position:",p
		if test_counter_i != 0:
			sus_first = suspicious_locations[test_counter[0]]
			for fiter in range(len(suspicious_locations[test_counter[0]])):
				accept_string[test_counter[0]] = suspicious_locations[test_counter[0]][fiter]
				print "setting the first error position as:",view_assign_t[suspicious_locations[test_counter[0]][fiter]]
				no_equal_list = []
				for n_times in range(2):
					print "no_equal_list:",no_equal_list
					insertion_done = False
					deletion_done = False
					j = p - end_index + in_index
					print "ITERATION:",COUNT
					COUNT += 1
					astr = [view_assign_t[accept_string[i]] for i in range(len(accept_string))]
					if j != 0:
						sympredef,tmp = parser_main(astr,j)
					else:
						sympredef = []

					print "j:",j

					s.push()
					print ".....................................  PUSH EXECUTED ...................................."

					# dollar at last position. len(accept_string) is changing with iteration
					s.add(functions["symbolAt"](strNum,vars["z%d"%(len(accept_string))]) == vars["dol"])
					s.add(vars["z%d"%(len(accept_string))] <= functions["end"](strNum,0))

					# making the successor function
					# changes need to be done here
					for k in range(len(accept_string)):
						if k == j:
							if j == len(accept_string)-1:
								#check it once
								s.add(If(vars["z%d"%k] == vars["in_extra"], If(vars["in_extra"] == vars["z%d"%(k+1)], functions["lookAheadIndex"](strNum,vars["z%d"%(k)]+1)==vars["z%d"%(j+1)], functions["lookAheadIndex"](strNum, vars["z%d"%k]+1)==vars["z%d"%(k+1)]), And(functions["lookAheadIndex"](strNum, vars["z%d"%k]+1)==vars["in_extra"], functions["lookAheadIndex"](strNum, vars["in_extra"]+1)==vars["z%d"%(k+1)])))
							else:
								s.add(If(vars["z%d"%k] == vars["in_extra"], If(vars["in_extra"] == vars["z%d"%(k+1)], functions["lookAheadIndex"](strNum,vars["z%d"%(k)]+1)==vars["z%d"%(k+2)], functions["lookAheadIndex"](strNum, vars["z%d"%k]+1)==vars["z%d"%(k+1)]), And(functions["lookAheadIndex"](strNum, vars["z%d"%k]+1)==vars["in_extra"], functions["lookAheadIndex"](strNum, vars["in_extra"]+1)==vars["z%d"%(k+1)])))
							continue
						s.add(functions["lookAheadIndex"](strNum, vars["z%d"%k]+1) == vars["z%d"%(k+1)])

					ka = 5 - j
					if ka < 5 :
						ka = 3
					# adding the stric inequality
					# check this thoroughly
					for i in range(1,len(accept_string)):
						if i == j:
							if i == len(accept_string)-1:
								s.add(And(vars["z%d"%i] == vars["in_extra"], vars["z%d"%(i+1)] == vars["in_extra"]))
								s.add(vars["z%d"%(i+1)] <= vars["prefix_limit"])
								continue
							s.add(And(vars["z%d"%i] < vars["in_extra"], vars["z%d"%(i+1)] > vars["in_extra"]))
							continue

						if i == j+ka:
							if i != j+1:
								s.add(And(vars["z%d"%(i)] <= vars["prefix_limit"], vars["z%d"%i] > vars["z%d"%(i-1)]))
							else:
								s.add(And(vars["z%d"%(i)] <= vars["prefix_limit"], vars["z%d"%i] >= vars["z%d"%(i-1)]))
							continue

						if i == j+1:
							s.add(And(vars["z%d"%i] >= vars["z%d"%(i-1)], vars["z%d"%(i)] < vars["z%d"%(i+1)]))
							if i == len(accept_string)-1:
								s.add(vars["z%d"%(i+1)] <= vars["prefix_limit"])
							continue

						if i == j+ka+1:
							s.add(And(vars["z%d"%(i)] >= vars["prefix_limit"], True))
							continue
						if i == len(accept_string)-1 and j+ka>len(accept_string)-1:
							s.add(And(vars["z%d"%(i)] > vars["z%d"%(i-1)], vars["z%d"%(i)] < vars["z%d"%(i+1)]))
							s.add(vars["z%d"%(i+1)] <= vars["prefix_limit"])
							continue
					s.add(And(vars["z%d"%(i)] > vars["z%d"%(i-1)], vars["z%d"%(i)] < vars["z%d"%(i+1)]))

					# modifying the valid  function
					OrList = []
					for i in range(len(accept_string)+1):
						OrList.append(vars["z%d"%i] == x)
					OrList.append(vars["in_extra"] == x)
					OrList.append(And(functions["symbolAt"](strNum,x)>= solver["non_term_start"],functions["symbolAt"](strNum, x) <= solver["non_term_end"]))
					laiList = [functions["lookAheadIndex"](strNum,x)==vars["z%d"%i] for i in range(len(accept_string)+1)]
					laiList.append(functions["lookAheadIndex"](strNum,x) == vars["in_extra"])
					s.add(ForAll(x, functions["valid"](x) == Implies(And(0 <= x, x <= vars["prefix_limit"]), And( functions["lookAheadIndex"](strNum,x) > 0, Or(laiList), Or(OrList) ,Or(And(functions["symbolAt"](strNum, x) <= solver["term_end"], functions["symbolAt"](strNum, x) >= solver["term_start"], functions["lookAheadIndex"](strNum, x) == x), And(functions["symbolAt"](strNum, x) <= solver["non_term_end"], functions["symbolAt"](strNum, x) >= solver["non_term_start"], functions["lookAheadIndex"](strNum,x+1) == functions["lookAheadIndex"](strNum,x), Exists([rn, X1,X2,X3,X4,X5,X6], And(functions["parseTable"](functions["symbolAt"](strNum,x), functions["symbolAt"](strNum, functions["lookAheadIndex"](strNum,x))) == rn,Not(rn ==0),x <= X1, X1 <= X2, X2 <= X3, X3 <= X4, X4 <= X5, X5 <= X6, X6 <= functions["end"](strNum,0), functions["hardcode"](rn, x, X1, X2, X3, X4, X5, X6))))))), patterns=[functions["valid"](x)]))

					# hardcode the parse array before suspicious terminal becomes lookahead
					for i in range(len(sympredef)):
						s.add(functions["symbolAt"](strNum,i) == vars[view_assign[sympredef[i]]])

					# add_soft(functions["symbolAt"](strNum,i) == vars[view_assign[sympredef[i]]],solver)
					# check this also
					for i in range(j+ka+1):
						if i < j:
							s.add(functions["symbolAt"](strNum, vars["z%d"%(i)]) == vars[accept_string[i]])
						else:
							if i > len(accept_string)-1:
								break
							if i+end_index-in_index in test_counter and False:
								pass
								#print "REMOVING %d"%(i+end_index-in_index)
								#if i + end_index-in_index != j:
								#	test_counter.remove(i+end_index-in_index)
								#add_soft(functions["symbolAt"](strNum, vars["z%d"%i]) == vars[accept_string[i]], solver)
							else:
								s.add(functions["symbolAt"](strNum, vars["z%d"%i]) == vars[accept_string[i]])

					#################  Multiple List ###########################
					if len(no_equal_list)!=0:
						AndList = [True]
						for t in no_equal_list:
							AndList.append(Not(functions["symbolAt"](strNum, vars["in_extra"]) == vars[t]))
						s.add(And(AndList))
					##############################################################

					input_file = open("smt_dumped%d"%j,"w+")
					input_file.write(dumpSMT(s))
					input_file.close()


					# p, unsat_soft_constrains, m = naive_maxsat(solver)
					sbp.call('sed "$ d" smt_dumped%d > smt_dumped_final.smt'%j, shell=True)
					output_file = open("tail.smt","w+")
					output_file.write("(push)\n(check-sat)\n")
					n = 1	# keeps track of the number of variables whose value is requested. Used in parsing the output file
					string = "(get-value ((symbolAt 1 z%d)"%(j)
					for i in range(ka):
						if j+i+1 > len(accept_string):
							break
						string += "(symbolAt 1 z%d)"%(j+i+1)
						n += 1
					string += "(symbolAt 1 in_extra)"
					n+=1
					string += "))\n"
					output_file.write(string)
					string = "(get-value (z%d"%j
					for i in range(ka):
						if j+i+1 > len(accept_string):
							break
						string += " z%d"%(j+i+1)
					string += " in_extra"
					string += "))\n"
					output_file.write(string)
					string  = "(get-value ((symbolAt 1 0) "
					for i in range(1, expansion_constant*len(accept_string)):
						string += "(symbolAt 1 %d)"%i
					string += "))\n"
					output_file.write(string)
					output_file.close()


					sbp.call("cat headers.smt smt_dumped_final.smt tail.smt > final_smt.smt", shell=True)
					sbp.call("z3-master/build/z3 -smt2 -t:120000 final_smt.smt > model.txt", shell=True)
					# print string
					try:
						cp = parse_output(ka,n,len(accept_string))
					except:
						s.pop()
						print ".....................................  POP EXECUTED ...................................."
						break
					if cp == -1:
						print "unsat :-("
						s.pop()
						print ".....................................  POP EXECUTED ...................................."
						if len(no_equal_list) == 0:
							sus_first.remove(suspicious_locations[test_counter[0]][fiter])
						else:
							break

					correct_string = []
					for i in range(len(accept_string)):
						if i < j or i > j+ka:
							correct_string.append(accept_string[i])
							continue
						if i == j:
							if cp[n+i-j] == cp[n+n-1]:
								# deletion or replacement
								if cp[n+n-1] == cp[n+i-j+1]:
									# deletion
									deletion_done = True
									end_index += 1
									continue
								else:
									# replacement
									tmp = cp[i-j]
									t = tokens[tmp-solver["non_term_end"]-1]
									correct_string.append(view_assign[t])
									continue
							else:
								# insertion
								insertion_done = True
								in_index += 1
								tmp = cp[i-j]
								t = tokens[tmp-solver["non_term_end"]-1]
								correct_string.append(view_assign[t])
								tmp = cp[n-1]
								t = tokens[tmp-solver["non_term_end"]-1]
								correct_string.append(view_assign[t])
								continue
						else:
							tmp = cp[i-j]
							t = tokens[tmp-solver["non_term_end"]-1]
							correct_string.append(view_assign[t])

					accept_string = correct_string
					pk = []
					for i in range(len(accept_string)):
						pk.append(view_assign_t[accept_string[i]])
					print "accept_string:",pk
					s.pop()
					print ".....................................  POP EXECUTED ...................................."
					pk = []
					print "term_start:",solver["term_start"]
					print "non_term_start:",solver["non_term_start"]
					print "term_end:",solver["term_end"]
					print "non_term_end:",solver["non_term_end"]

					view_assign_nt = solver["view_assign_nt"]
					#print "cp: ",cp
					print "PARSE ARRAY:"
					tmp = len(accept_string)
					if insertion_done:
						tmp-=1
					if deletion_done:
						tmp+=1
					for i in range(expansion_constant*tmp):
						#print "n:%d i:%d"%(n,i)
						tmp=cp[2*n+i]
						# print "position:",i
						# print "tmp:",tmp
						if tmp <= solver["non_term_end"]:
							nt = "N%d"%(tmp-solver["non_term_start"]+1)
							pk.append(view_assign_nt[nt])
						else:
							t = tokens[tmp-solver["non_term_end"]-1]
							pk.append(t)

					if insertion_done == True:
						tlast = solver["lastz"]+1
						vars["z%d"%tlast] = Int('z%d'%tlast)
						solver["lastz"] = tlast
						OrList = []
						for t in terms+["dol"]:
							OrList.append(vars[t] == functions["symbolAt"](strNum,vars["z%d"%tlast]))
						s.add(Or(OrList))
					print pk
					print "Ending the iteration",(COUNT-1)
					print "Test_counter:",test_counter

					no_equal_list.append(correct_string[j+1])
					suspicious_locations[p].append(correct_string[j+1])
					print "suspicious_locations for this position",suspicious_locations[p+1]
					#tmp = deepcopy(accept_string)
					tmp = []
					for i in range(len(accept_string)):
						tmp.append(view_assign_t[accept_string[i]])
					flag = parser_main1(tmp)
					if flag == 1:
						return 1
					else:
						correct_string = []
						for i in range(len(accept_string)):
							if i == j+1:
								continue
							correct_string.append(accept_string[i])
						accept_string = correct_string
						in_index = 0

			suspicious_locations[test_counter[0]] = sus_first
			print "final first suspicious_locations:",suspicious_locations[test_counter[0]]
		else:
			no_equal_list = []
			for n_times in range(2):
					print "no_equal_list:",no_equal_list
					insertion_done = False
					deletion_done = False
					j = p - end_index + in_index
					print "ITERATION:",COUNT
					COUNT += 1
					astr = [view_assign_t[accept_string[i]] for i in range(len(accept_string))]
					if j != 0:
						sympredef,tmp = parser_main(astr,j)
					else:
						sympredef = []
					lastj_term = accept_string[j+1]
					print "j:",j

					s.push()
					print ".....................................  PUSH EXECUTED ...................................."

					# dollar at last position. len(accept_string) is changing with iteration
					s.add(functions["symbolAt"](strNum,vars["z%d"%(len(accept_string))]) == vars["dol"])
					s.add(vars["z%d"%(len(accept_string))] <= functions["end"](strNum,0))

					# making the successor function
					# changes need to be done here
					for k in range(len(accept_string)):
						if k == j:
							if j == len(accept_string)-1:
								#check it once
								s.add(If(vars["z%d"%k] == vars["in_extra"], If(vars["in_extra"] == vars["z%d"%(k+1)], functions["lookAheadIndex"](strNum,vars["z%d"%(k)]+1)==vars["z%d"%(j+1)], functions["lookAheadIndex"](strNum, vars["z%d"%k]+1)==vars["z%d"%(k+1)]), And(functions["lookAheadIndex"](strNum, vars["z%d"%k]+1)==vars["in_extra"], functions["lookAheadIndex"](strNum, vars["in_extra"]+1)==vars["z%d"%(k+1)])))
							else:
								s.add(If(vars["z%d"%k] == vars["in_extra"], If(vars["in_extra"] == vars["z%d"%(k+1)], functions["lookAheadIndex"](strNum,vars["z%d"%(k)]+1)==vars["z%d"%(k+2)], functions["lookAheadIndex"](strNum, vars["z%d"%k]+1)==vars["z%d"%(k+1)]), And(functions["lookAheadIndex"](strNum, vars["z%d"%k]+1)==vars["in_extra"], functions["lookAheadIndex"](strNum, vars["in_extra"]+1)==vars["z%d"%(k+1)])))
							continue
						s.add(functions["lookAheadIndex"](strNum, vars["z%d"%k]+1) == vars["z%d"%(k+1)])

					ka = 5 - j
					if ka < 5 :
						ka =3
					# adding the stric inequality
					# check this thoroughly
					for i in range(1,len(accept_string)):
						if i == j:
							if i == len(accept_string)-1:
								s.add(And(vars["z%d"%i] == vars["in_extra"], vars["z%d"%(i+1)] == vars["in_extra"]))
								s.add(vars["z%d"%(i+1)] <= vars["prefix_limit"])
								continue
							s.add(And(vars["z%d"%i] == vars["in_extra"], vars["z%d"%(i+1)] == vars["in_extra"]))
							continue

						if i == j+ka:
							if i != j+1:
								s.add(And(vars["z%d"%(i)] <= vars["prefix_limit"], vars["z%d"%i] > vars["z%d"%(i-1)]))
							else:
								s.add(And(vars["z%d"%(i)] <= vars["prefix_limit"], vars["z%d"%i] >= vars["z%d"%(i-1)]))
							continue

						if i == j+1:
							s.add(And(vars["z%d"%i] >= vars["z%d"%(i-1)], vars["z%d"%(i)] < vars["z%d"%(i+1)]))
							if i == len(accept_string)-1:
								s.add(vars["z%d"%(i+1)] <= vars["prefix_limit"])
							continue

						if i == j+ka+1:
							s.add(And(vars["z%d"%(i)] >= vars["prefix_limit"], True))
							continue
						if i == len(accept_string)-1 and j+ka>len(accept_string)-1:
							s.add(And(vars["z%d"%(i)] > vars["z%d"%(i-1)], vars["z%d"%(i)] < vars["z%d"%(i+1)]))
							s.add(vars["z%d"%(i+1)] <= vars["prefix_limit"])
							continue
						s.add(And(vars["z%d"%(i)] > vars["z%d"%(i-1)], vars["z%d"%(i)] < vars["z%d"%(i+1)]))

					# modifying the valid  function
					OrList = []
					for i in range(len(accept_string)+1):
						OrList.append(vars["z%d"%i] == x)
					OrList.append(vars["in_extra"] == x)
					OrList.append(And(functions["symbolAt"](strNum,x)>= solver["non_term_start"],functions["symbolAt"](strNum, x) <= solver["non_term_end"]))
					laiList = [functions["lookAheadIndex"](strNum,x)==vars["z%d"%i] for i in range(len(accept_string)+1)]
					laiList.append(functions["lookAheadIndex"](strNum,x) == vars["in_extra"])
					s.add(ForAll(x, functions["valid"](x) == Implies(And(0 <= x, x <= vars["prefix_limit"]), And( functions["lookAheadIndex"](strNum,x) > 0, Or(laiList), Or(OrList) ,Or(And(functions["symbolAt"](strNum, x) <= solver["term_end"], functions["symbolAt"](strNum, x) >= solver["term_start"], functions["lookAheadIndex"](strNum, x) == x), And(functions["symbolAt"](strNum, x) <= solver["non_term_end"], functions["symbolAt"](strNum, x) >= solver["non_term_start"], functions["lookAheadIndex"](strNum,x+1) == functions["lookAheadIndex"](strNum,x), Exists([rn, X1,X2,X3,X4,X5,X6], And(functions["parseTable"](functions["symbolAt"](strNum,x), functions["symbolAt"](strNum, functions["lookAheadIndex"](strNum,x))) == rn,Not(rn ==0),x <= X1, X1 <= X2, X2 <= X3, X3 <= X4, X4 <= X5, X5 <= X6, X6 <= functions["end"](strNum,0), functions["hardcode"](rn, x, X1, X2, X3, X4, X5, X6))))))), patterns=[functions["valid"](x)]))

					# hardcode the parse array before suspicious terminal becomes lookahead
					for i in range(len(sympredef)):
						s.add(functions["symbolAt"](strNum,i) == vars[view_assign[sympredef[i]]])

					# add_soft(functions["symbolAt"](strNum,i) == vars[view_assign[sympredef[i]]],solver)
					# check this also
					for i in range(j+ka+1):
						if i < j:
							s.add(functions["symbolAt"](strNum, vars["z%d"%(i)]) == vars[accept_string[i]])
						else:
							if i > len(accept_string)-1:
								break
							if i+end_index-in_index-1 in test_counter:
								pass
								#print "REMOVING %d"%(i+end_index-in_index)
								#if i + end_index-in_index != j:
								#	test_counter.remove(i+end_index-in_index)
								#add_soft(functions["symbolAt"](strNum, vars["z%d"%i]) == vars[accept_string[i]], solver)
							else:
								s.add(functions["symbolAt"](strNum, vars["z%d"%i]) == vars[accept_string[i]])

					#################  Multiple List ###########################
					if len(no_equal_list)!=0:
						AndList = [True]
						for t in no_equal_list:
							AndList.append(Not(functions["symbolAt"](strNum, vars["in_extra"]) == vars[t]))
						print "Asserting not equal:",AndList
						s.add(And(AndList))
						s.add(testvar == n_times)
					##############################################################
					input_file = open("smt_dumped%d"%j,"w+")
					input_file.write(dumpSMT(s))
					input_file.close()

					# p, unsat_soft_constrains, m = naive_maxsat(solver)
					sbp.call('sed "$ d" smt_dumped%d > smt_dumped_final.smt'%j, shell=True)
					output_file = open("tail.smt","w+")
					output_file.write("(push)\n(check-sat)\n")
					n = 1	# keeps track of the number of variables whose value is requested. Used in parsing the output file
					string = "(get-value ((symbolAt 1 z%d)"%(j)
					for i in range(ka):
						if j+i+1 > len(accept_string):
							break
						string += "(symbolAt 1 z%d)"%(j+i+1)
						n += 1
					string += "(symbolAt 1 in_extra)"
					n+=1
					string += "))\n"
					output_file.write(string)
					string = "(get-value (z%d"%j
					for i in range(ka):
						if j+i+1 > len(accept_string):
							break
						string += " z%d"%(j+i+1)
					string += " in_extra"
					string += "))\n"
					output_file.write(string)
					string  = "(get-value ((symbolAt 1 0) "
					for i in range(1, expansion_constant*len(accept_string)):
						string += "(symbolAt 1 %d)"%i
					string += "))\n(pop)\n"
					output_file.write(string)
					output_file.close()


					sbp.call("cat headers.smt smt_dumped_final.smt tail.smt > final_smt.smt", shell=True)
					sbp.call("z3-master/build/z3 -smt2 -t:120000 final_smt.smt > model.txt", shell=True)
					# print string
					try:
						cp = parse_output(ka,n,len(accept_string))
					except:
						if len(no_equal_list) == 0:
							return 0
						else:
							s.pop()
							print ".....................................  POP EXECUTED ...................................."
							break
					if cp == -1:
						print "unsat :-("
						s.pop()
						print ".....................................  POP EXECUTED ...................................."
						if len(no_equal_list) == 0:
							return 0
						else:
							break


					correct_string = []
					for i in range(len(accept_string)):
						if i < j or i > j+ka:
							correct_string.append(accept_string[i])
							continue
						if i == j:
							if cp[n+i-j] == cp[n+n-1]:
								# deletion or replacement
								if cp[n+n-1] == cp[n+i-j+1]:
									# deletion
									deletion_done = True
									end_index += 1
									continue
								else:
									# replacement
									tmp = cp[i-j]
									t = tokens[tmp-solver["non_term_end"]-1]
									correct_string.append(view_assign[t])
									continue
							else:
								# insertion
								insertion_done = True
								in_index += 1
								tmp = cp[i-j]
								t = tokens[tmp-solver["non_term_end"]-1]
								correct_string.append(view_assign[t])
								tmp = cp[n-1]
								t = tokens[tmp-solver["non_term_end"]-1]
								correct_string.append(view_assign[t])
								continue
						else:
							tmp = cp[i-j]
							t = tokens[tmp-solver["non_term_end"]-1]
							correct_string.append(view_assign[t])

					accept_string = correct_string
					pk = []
					for i in range(len(accept_string)):
						pk.append(view_assign_t[accept_string[i]])
					print "accept_string:",pk
					s.pop()
					print ".....................................  POP EXECUTED ...................................."
					pk = []
					print "term_start:",solver["term_start"]
					print "non_term_start:",solver["non_term_start"]
					print "term_end:",solver["term_end"]
					print "non_term_end:",solver["non_term_end"]

					view_assign_nt = solver["view_assign_nt"]
					#print "cp: ",cp
					print "PARSE ARRAY:"
					tmp = len(accept_string)
					if insertion_done:
						tmp-=1
					if deletion_done:
						tmp+=1
					for i in range(expansion_constant*tmp):
						#print "n:%d i:%d"%(n,i)
						tmp=cp[2*n+i]
						# print "position:",i
						# print "tmp:",tmp
						if tmp <= solver["non_term_end"]:
							nt = "N%d"%(tmp-solver["non_term_start"]+1)
							pk.append(view_assign_nt[nt])
						else:
							t = tokens[tmp-solver["non_term_end"]-1]
							pk.append(t)

					if insertion_done == True:
						tlast = solver["lastz"]+1
						vars["z%d"%tlast] = Int('z%d'%tlast)
						solver["lastz"] = tlast
						OrList = []
						for t in terms+["dol"]:
							OrList.append(vars[t] == functions["symbolAt"](strNum,vars["z%d"%tlast]))
						s.add(Or(OrList))
					print pk
					print "Ending the iteration",(COUNT-1)
					print "Test_counter:",test_counter

					no_equal_list.append(correct_string[j+1])
					print "Adding"
					print p
					print correct_string[j+1]
					suspicious_locations[test_counter[test_counter_i]].append(correct_string[j+1])
					print "suspicious_locations for this location:",suspicious_locations[test_counter[test_counter_i]]
					#tmp = deepcopy(accept_string)
					tmp = []
					for i in range(len(accept_string)):
						tmp.append(view_assign_t[accept_string[i]])
					flag = parser_main1(tmp)
					if flag == 1:
						return 1
					else:
						correct_string = []
						for i in range(len(accept_string)):
							if i == j:
								correct_string.append(accept_string[j])
								correct_string.append(lastj_term)
								continue
							correct_string.append(accept_string[i])

						accept_string = correct_string
						end_index = 0
	ret = final_string(test_counter, accept_string, suspicious_locations, view_assign_t)
	return ret

def find_final_errors(solver, test_counter, accept_string):
	print "........................................ Verification function called ........................"
	s = solver["constraints"]
	vars = solver["vars"]
	functions = solver["functions"]
	# start time
	# return just before
	s_time = calendar.timegm(time.gmtime())
	terms = solver["terms"]
	strNum = solver["num_strings"]
	view_assign = solver["view_assign"]
	view_assign_t = solver["view_assign_t"]
	x,X1,X2,X3,X4,X5,X6,rn = vars["xn"],vars["X1"],vars["X2"],vars["X3"],vars["X4"],vars["X5"],vars["X6"],vars["rn"]
	for fiter in range(len(test_counter)):
		j = test_counter[fiter]
		if j == 0 or j == 1:
			continue
		astr = [view_assign_t[accept_string[i]] for i in range(len(accept_string))]
		if j != 0:
			sympredef,tmp = parser_main(astr,j)
		else:
			sympredef = []
		#lastj_term = accept_string[j+1]
		print "j:",j
		if sympredef == 0:
			e_time = calendar.timegm(time.gmtime())
			solver["vtime"] = str(datetime.timedelta(seconds=(e_time-s_time)))
			return -1

		s.push()
		print ".....................................  PUSH EXECUTED ...................................."

		# dollar at last position. len(accept_string) is changing with iteration
		s.add(functions["symbolAt"](strNum,vars["z%d"%(len(accept_string))]) == vars["dol"])
		s.add(vars["z%d"%(len(accept_string))] <= functions["end"](strNum,0))

		# making the successor function
		# changes need to be done here
		for k in range(j+1):
			s.add(functions["lookAheadIndex"](strNum, vars["z%d"%k]+1) == vars["z%d"%(k+1)])

		# adding the stric inequality
		# check this thoroughly
		for i in range(1,j+1):
			s.add(And(vars["z%d"%i] > vars["z%d"%(i-1)], vars["z%d"%i] < vars["z%d"%(i+1)]))
		s.add(vars["z%d"%j] <= vars["prefix_limit"])
		s.add(vars["z%d"%(j+1)] > vars["prefix_limit"])

		# modifying the valid  function
		OrList = []
		for i in range(len(accept_string)+1):
			OrList.append(vars["z%d"%i] == x)
		OrList.append(vars["in_extra"] == x)
		OrList.append(And(functions["symbolAt"](strNum,x)>= solver["non_term_start"],functions["symbolAt"](strNum, x) <= solver["non_term_end"]))
		laiList = [functions["lookAheadIndex"](strNum,x)==vars["z%d"%i] for i in range(len(accept_string)+1)]
		laiList.append(functions["lookAheadIndex"](strNum,x) == vars["in_extra"])
		s.add(ForAll(x, functions["valid"](x) == Implies(And(0 <= x, x <= vars["prefix_limit"]), And( functions["lookAheadIndex"](strNum,x) > 0, Or(laiList), Or(OrList) ,Or(And(functions["symbolAt"](strNum, x) <= solver["term_end"], functions["symbolAt"](strNum, x) >= solver["term_start"], functions["lookAheadIndex"](strNum, x) == x), And(functions["symbolAt"](strNum, x) <= solver["non_term_end"], functions["symbolAt"](strNum, x) >= solver["non_term_start"], functions["lookAheadIndex"](strNum,x+1) == functions["lookAheadIndex"](strNum,x), Exists([rn, X1,X2,X3,X4,X5,X6], And(functions["parseTable"](functions["symbolAt"](strNum,x), functions["symbolAt"](strNum, functions["lookAheadIndex"](strNum,x))) == rn,Not(rn ==0),x <= X1, X1 <= X2, X2 <= X3, X3 <= X4, X4 <= X5, X5 <= X6, X6 <= functions["end"](strNum,0), functions["hardcode"](rn, x, X1, X2, X3, X4, X5, X6))))))), patterns=[functions["valid"](x)]))

		# hardcode the parse array before suspicious terminal becomes lookahead
		for i in range(len(sympredef)):
			s.add(functions["symbolAt"](strNum,i) == vars[view_assign[sympredef[i]]])

		# add_soft(functions["symbolAt"](strNum,i) == vars[view_assign[sympredef[i]]],solver)
		# check this also

		for i in range(j+1):
			s.add(functions["symbolAt"](strNum, vars["z%d"%(i)]) == vars[accept_string[i]])

		input_file = open("smt_dumped%d"%j,"w+")
		input_file.write(dumpSMT(s))
		input_file.close()

		# p, unsat_soft_constrains, m = naive_maxsat(solver)
		sbp.call('sed "$ d" smt_dumped%d > smt_dumped_final.smt'%j, shell=True)
		output_file = open("tail.smt","w+")
		output_file.write("(push)\n(check-sat)\n")
		output_file.close()

		sbp.call("cat headers.smt smt_dumped_final.smt tail.smt > final_smt.smt", shell=True)
		sbp.call("z3-master/build/z3 -smt2 -t:120000 final_smt.smt > model.txt", shell=True)
		# print string
		output_file = open("model.txt")
		lines = output_file.readlines()
		unsat_flag = False
		if lines[1] == "unsat\n":
			unsat_flag = True
		if unsat_flag == True:
			print "..................................... POP EXECUTED ................................."
			s.pop()
			e_time = calendar.timegm(time.gmtime())
			solver["vtime"] = str(datetime.timedelta(seconds=(e_time-s_time)))
			return j-1
		print "............................. POP EXECUTED ................................."
		s.pop()
	e_time = calendar.timegm(time.gmtime())
	solver["vtime"] = str(datetime.timedelta(seconds=(e_time-s_time)))
	return test_counter[0]
