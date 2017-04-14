from z3 import *
from solver import *
from init import *
from itertools import *
from input_specs_tiger import specs
from parser import parser_main
import pickle
from msat import *
def req_rules(solver):

	m = solver["model"]
	m_vars = solver["vars"]
	m_funs = solver["functions"]

	num_rules = config['num_rules']
	num_nonterms = config['num_nonterms']
	num_terms = config['num_terms']
	size_rules = config['size_rules']

	#check distinct rules
	seen_rules = set()
	distinct_rules = [False for i in range(num_rules)]
	for i in range(num_rules):
		rule = ()
		rule += (int(str(m.evaluate(m_funs["symbolInLHS"](i+1)))),)
		for j in range(size_rules):
			rule += (int(str(m.evaluate(m_funs["symbolInRHS"](i+1,j+1)))),)
		if rule not in seen_rules:
			seen_rules.add(rule)
			distinct_rules[i] = True
		else:
			distinct_rules[i] = False


	#check reachable rules
	reached_rules = [False for i in range(num_rules)]
	reached_nonterms = [False for i in range(num_nonterms)]

	reached_nonterms[0] = True
	changed = True

	while changed:
		changed = False
		for j in range(num_rules):
			if not reached_rules[j] and reached_nonterms[int(str(m.evaluate(m_funs["symbolInLHS"](j+1))))]:
				reached_rules[j] = True
				changed = True
				for k in range(size_rules):
					symbolValue = int(str(m.evaluate(m_funs["symbolInRHS"](j+1,k+1))))
					if symbolValue < num_nonterms:
						if not reached_nonterms[symbolValue]:
							reached_nonterms[symbolValue] = True

	#check producing rules (producing a term or eps)
	producing_rules = [False for i in range(num_rules)]
	producing_nonterms = [False for i in range(num_nonterms)]

	for i in range(num_rules):
		goodrule = False
		for j in range(size_rules):
			symbolValue = int(str(m.evaluate(m_funs["symbolInRHS"](i+1,j+1))))
			if symbolValue >= num_nonterms:
				goodrule = True
			else:
				goodrule = False
				break
		if goodrule:
			producing_nonterms[int(str(m.evaluate(m_funs["symbolInLHS"](i+1))))] = True
			producing_rules[i]= True

	changed = True
	#considered not producing rules as those which do not have terminals on their RHS..Now rectifying this
	while changed:
		changed = False
		for j in range(num_rules):
			if not producing_rules[j]:
				producing_rules[j] = True
				for k in range(size_rules):
					symbolValue = int(str(m.evaluate(m_funs["symbolInRHS"](j+1,k+1))))
					if symbolValue < num_nonterms:
						if not producing_nonterms[symbolValue]:
							producing_rules[j] = False
							break
				if producing_rules[j] == True:
					producing_nonterms[int(str(m.evaluate(m_funs["symbolInLHS"](j+1))))] = True
					changed = True 

	return [(i and j and k) for (i,j,k) in zip(distinct_rules,reached_rules,producing_rules)]


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
		
def assert_grammar_soft(S_target,S_source,req=False):
	print "calling assert_grammar_soft\n"
	s = S_target["constraints"]
	assumptions = []

	num_rules = config['num_rules']
	num_nonterms = config['num_nonterms']
	num_terms = config['num_terms']
	size_rules = config['size_rules']

	if req:
		reqrules = req_rules(S_source)
	
		for r in range(num_rules):
			if reqrules[r]:
				i=0
				v = Bool('p_%d_%d'%((r+1),i))
				s.add(Implies(v, S_target["functions"]["symbolInLHS"](r+1)==int(str(S_source["model"].evaluate(S_source["functions"]["symbolInLHS"](r+1))))))
				assumptions.append(v)
				for i in range(1,size_rules+1):
					v = Bool('p_%d_%d'%((r+1),i))
					s.add(Implies(v, S_target["functions"]["symbolInRHS"](r+1,i)==int(str(S_source["model"].evaluate(S_source["functions"]["symbolInRHS"](r+1,i))))))
					assumptions.append(v)

	else:
		for r in range(num_rules):
			i=0
			v = Bool('p_%d_%d'%((r+1),i))
			s.add(Implies(v, S_target["functions"]["symbolInLHS"](r+1)==int(str(S_source["model"].evaluate(S_source["functions"]["symbolInLHS"](r+1))))))
			assumptions.append(v)
			for i in range(1,size_rules+1):
				v = Bool('p_%d_%d'%((r+1),i))
				s.add(Implies(v, S_target["functions"]["symbolInRHS"](r+1,i)==int(str(S_source["model"].evaluate(S_source["functions"]["symbolInRHS"](r+1,i))))))
				assumptions.append(v)

	return assumptions

def find_errors():
	############################################
	pkl_file = open("tigerTableUpdated.pkl","rb")
	ngrams = pickle.load(pkl_file)
	pkl_file.close()

	############################################
	# string = string.split()
	string = accept_strings[0]
	string = string.split()
	print "STRING :", string
	tmp = []
	for i in range(len(string)):
		if i != 0:
			t1 = (string[i-1],string[i])
			if t1 not in ngrams:
				tmp.append(i)
				continue
			f1 = ngrams[t1]
			if f1 < 7:
				tmp.append(i)
		if i != len(string)-1:
			t1 = (string[i],string[i+1])
			if t1 not in ngrams:
				tmp.append(i)
				continue
			f1 = ngrams[t1]
			if f1 < 7:
				tmp.append(i)
	return tmp

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
	
	test_counter = find_errors()
	# test_counter = [0,2,3,1,-1]
	print "TEST COUNTERS: ",test_counter
	test_counter = [4]

	###################################################################################################
	rn = Int('rn')
	x,X0,X1,X2,X3,X4,X5,X6 = Ints('x X0 X1 X2 X3 X4 X5 X6')
	lim = expansion_constant*len(accept_string)
	s.add(ForAll([rn,X0,X1,X2,X3,X4,X5,X6],Implies( And(0<=X0,X0<=X1,X1<=X2,X2<=X3,X3<=X4,X4<=X5,X5<=X6,X6<=lim),functions["hardcode"](rn,X0,X1,X2,X3,X4,X5,X6) == Or(And (rn == vars["rule1"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Prog1"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Prog"]] ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["dol"]] ),And (rn == vars["rule2"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Prog"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["Exp"]] ),And (rn == vars["rule3"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Exp"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["ExpOR"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["ExpORPr"]] ),And (rn == vars["rule4"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["ExpOR"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["ExpAND"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["ExpANDPr"]] ),And (rn == vars["rule5"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["ExpORPr"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["|"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["Exp"]] ),And (rn == vars["rule6"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["ExpORPr"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule7"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["ExpANDPr"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["&"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["ExpOR"]] ),And (rn == vars["rule8"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["ExpANDPr"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule9"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["ExpAND"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["ArithExp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["RelationExp"]] ),And (rn == vars["rule10"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["ArithExp"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Term"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["TermPr"]] ),And (rn == vars["rule11"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["RelationExp"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["RelationOp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["ArithExp"]] ),And (rn == vars["rule12"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["RelationExp"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule13"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Term"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Factor"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FactorPr"]] ),And (rn == vars["rule14"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["TermPr"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["+"]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Term"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["TermPr"]] ),And (rn == vars["rule15"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["TermPr"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["-"]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Term"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["TermPr"]] ),And (rn == vars["rule16"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["TermPr"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule17"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FactorPr"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["*"]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Factor"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FactorPr"]] ),And (rn == vars["rule18"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FactorPr"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["/"]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Factor"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FactorPr"]] ),And (rn == vars["rule19"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FactorPr"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule20"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Factor"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["nil"]] ),And (rn == vars["rule21"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Factor"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["integer"]] ),And (rn == vars["rule22"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Factor"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["string"]] ),And (rn == vars["rule23"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Factor"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["("]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["ExpList"]] ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign[")"]] ),And (rn == vars["rule24"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Factor"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["UnaryOp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["Exp"]] ),And (rn == vars["rule25"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Factor"]], X1 == X0+1, X2 == X1+1, functions["end"](strNum, X1) == X1, functions["symbolAt"](strNum, X1) == vars[view_assign["if"]] ,functions["end"](strNum, X2)+1 == X3, functions["symbolAt"](strNum, X2) == vars[view_assign["Exp"]] ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["then"]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Exp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["IF_extra"]] ),And (rn == vars["rule26"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["IF_extra"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["else"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["Exp"]] ),And (rn == vars["rule27"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["IF_extra"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule28"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Factor"]], X1 == X0+1, X1 == X2 ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["while"]] ,functions["end"](strNum, X3)+1 == X4, functions["symbolAt"](strNum, X3) == vars[view_assign["Exp"]] ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["do"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["Exp"]] ),And (rn == vars["rule29"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Factor"]], X1 == X0+1, X2 == X1+1, functions["end"](strNum, X1) == X1, functions["symbolAt"](strNum, X1) == vars[view_assign["for"]] ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["id"]] ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign[":="]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Exp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["F1"]] ),And (rn == vars["rule30"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["F1"]], X1 == X0+1, X1 == X2 ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["to"]] ,functions["end"](strNum, X3)+1 == X4, functions["symbolAt"](strNum, X3) == vars[view_assign["Exp"]] ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["do"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["Exp"]] ),And (rn == vars["rule31"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Factor"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["break"]] ),And (rn == vars["rule32"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Factor"]], X1 == X0+1, X2 == X1+1, functions["end"](strNum, X1) == X1, functions["symbolAt"](strNum, X1) == vars[view_assign["let"]] ,functions["end"](strNum, X2)+1 == X3, functions["symbolAt"](strNum, X2) == vars[view_assign["DecList"]] ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["in"]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["ExpList"]] ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["end"]] ),And (rn == vars["rule33"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Factor"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["LValue"]] ),And (rn == vars["rule34"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["DecList"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["DL_extra"]] ),And (rn == vars["rule35"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["DL_extra"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Dec"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["DL_extra"]] ),And (rn == vars["rule36"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["DL_extra"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule37"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Dec"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["TyDec"]] ),And (rn == vars["rule38"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Dec"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["VarDec"]] ),And (rn == vars["rule39"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Dec"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FunDec"]] ),And (rn == vars["rule40"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["TyDec"]], X1 == X0+1, X1 == X2 ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["type"]] ,functions["end"](strNum, X3)+1 == X4, functions["symbolAt"](strNum, X3) == vars[view_assign["TypeId"]] ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["="]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["Ty"]] ), \
		And (rn == vars["rule41"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Ty"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["{"]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["FieldList"]] ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["}"]] ),And (rn == vars["rule42"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Ty"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["array"]] ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["of"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["TypeId"]] ),And (rn == vars["rule43"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["Ty"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["TypeId"]] ),And (rn == vars["rule44"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FieldList"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule45"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FieldList"]], X1 == X0+1, X1 == X2 ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["id"]] ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign[":"]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["TypeId"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FL_extra"]] ),And (rn == vars["rule46"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FL_extra"]], X1 == X0+1, X2 == X1+1, functions["end"](strNum, X1) == X1, functions["symbolAt"](strNum, X1) == vars[view_assign[","]] ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["id"]] ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign[":"]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["TypeId"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FL_extra"]] ),And (rn == vars["rule47"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FL_extra"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ), \
		And (rn == vars["rule48"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FieldExpList"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule49"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FieldExpList"]], X1 == X0+1, X1 == X2 ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["id"]] ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["="]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Exp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FEL_extra"]] ),And (rn == vars["rule50"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FEL_extra"]], X1 == X0+1, X2 == X1+1, functions["end"](strNum, X1) == X1, functions["symbolAt"](strNum, X1) == vars[view_assign[","]] ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["id"]] ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["="]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Exp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FEL_extra"]] ),And (rn == vars["rule51"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FEL_extra"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule52"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["TypeId"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["id"]] ),And (rn == vars["rule53"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["TypeId"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["integer"]] ),And (rn == vars["rule54"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["TypeId"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["string"]] ),And (rn == vars["rule55"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["VD_extra"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule56"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["VD_extra"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign[":"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["TypeId"]] ),And (rn == vars["rule57"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["VarDec"]], X1 == X0+1, X2 == X1+1, functions["end"](strNum, X1) == X1, functions["symbolAt"](strNum, X1) == vars[view_assign["var"]] ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["id"]] ,functions["end"](strNum, X3)+1 == X4, functions["symbolAt"](strNum, X3) == vars[view_assign["VD_extra"]] ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign[":="]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["Exp"]] ),And (rn == vars["rule58"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FunDec"]], X1 == X0+1, X2 == X1+1, functions["end"](strNum, X1) == X1, functions["symbolAt"](strNum, X1) == vars[view_assign["function"]] ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["id"]] ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["("]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["FieldList"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["F2"]] ),And (rn == vars["rule59"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["F2"]], X1 == X0+1, X1 == X2 ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign[")"]] ,functions["end"](strNum, X3)+1 == X4, functions["symbolAt"](strNum, X3) == vars[view_assign["VD_extra"]] ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["="]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["Exp"]] ),And (rn == vars["rule60"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["LValue"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["id"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["LD_extra"]] ),And (rn == vars["rule61"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["LD_extra"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FunctionRecordArrayPr"]] ),And (rn == vars["rule62"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["LD_extra"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FunctionRecordArray"]] ),And (rn == vars["rule63"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FunctionRecordArray"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["("]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["ArgList"]] ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign[")"]] ),And (rn == vars["rule64"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FunctionRecordArray"]], X1 == X0+1, X2 == X1+1, functions["end"](strNum, X1) == X1, functions["symbolAt"](strNum, X1) == vars[view_assign["{"]] ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["id"]] ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["="]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Exp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["F3"]] ),And (rn == vars["rule65"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["F3"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["FRA_extra"]] ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["}"]] ),And (rn == vars["rule66"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FRA_extra"]], X1 == X0+1, X2 == X1+1, functions["end"](strNum, X1) == X1, functions["symbolAt"](strNum, X1) == vars[view_assign[","]] ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["id"]] ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["="]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Exp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FRA_extra"]] ), \
		And (rn == vars["rule67"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FRA_extra"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule68"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FunctionRecordArray"]], X1 == X0+1, X1 == X2 ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["["]] ,functions["end"](strNum, X3)+1 == X4, functions["symbolAt"](strNum, X3) == vars[view_assign["Exp"]] ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["]"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FRA_extra1"]] ),And (rn == vars["rule69"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FRA_extra1"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FunctionRecordArrayPr"]] ),And (rn == vars["rule70"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FRA_extra1"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["of"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["Exp"]] ),And (rn == vars["rule71"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FRAP_extra1"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign[":="]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["Exp"]] ),And (rn == vars["rule72"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FRAP_extra1"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule73"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FunctionRecordArrayPr"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["FRAP_extra"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FRAP_extra1"]] ),And (rn == vars["rule74"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FRAP_extra"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["."]] ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["id"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FRAP_extra"]] ),And (rn == vars["rule75"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FRAP_extra"]], X1 == X0+1, X1 == X2 ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["["]] ,functions["end"](strNum, X3)+1 == X4, functions["symbolAt"](strNum, X3) == vars[view_assign["Exp"]] ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["]"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["FRAP_extra"]] ),And (rn == vars["rule76"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["FRAP_extra"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule77"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["ExpList"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule78"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["ExpList"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Exp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["EL_extra"]] ),And (rn == vars["rule79"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["EL_extra"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule80"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["EL_extra"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign[";"]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Exp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["EL_extra"]] ),And (rn == vars["rule81"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["ArgList"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule82"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["ArgList"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Exp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["AL_extra"]] ),And (rn == vars["rule83"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["AL_extra"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign[","]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["Exp"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["AL_extra"]] ), \
		And (rn == vars["rule84"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["AL_extra"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule85"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["UnaryOp"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["-"]] ),And (rn == vars["rule86"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["RelationOp"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["="]] ),And (rn == vars["rule87"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["RelationOp"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["!="]] ),And (rn == vars["rule88"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["RelationOp"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign[">"]] ),And (rn == vars["rule89"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["RelationOp"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["<"]] ),And (rn == vars["rule90"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["RelationOp"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign[">="]] ),And (rn == vars["rule91"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["RelationOp"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["<="]] ))), patterns=[functions["hardcode"](rn,X0,X1,X2,X3,X4,X5,X6)]))

	# s.add(ForAll([rn,X0,X1,X2,X3,X4,X5,X6], functions["hardcode"](rn, X0, X1, X2, X3, X4, X5, X6) == Or(And (rn == vars["rule1"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["S1"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["S"]] ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["dol"]] ),And (rn == vars["rule2"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["S"]], X1 == X0+1, X1 == X2 ,X3 == X2+1, functions["end"](strNum, X2) == X2, functions["symbolAt"](strNum, X2) == vars[view_assign["a"]] ,functions["end"](strNum, X3)+1 == X4, functions["symbolAt"](strNum, X3) == vars[view_assign["A"]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["B"]] ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["b"]] ),And (rn == vars["rule3"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["A"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X4 == X3+1, functions["end"](strNum, X3) == X3, functions["symbolAt"](strNum, X3) == vars[view_assign["a"]] ,functions["end"](strNum, X4)+1 == X5, functions["symbolAt"](strNum, X4) == vars[view_assign["A"]] ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["c"]] ),And (rn == vars["rule4"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["A"]], X1 == X0, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X5 == X6 ),And (rn == vars["rule5"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["B"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X5 == X4+1, functions["end"](strNum, X4) == X4, functions["symbolAt"](strNum, X4) == vars[view_assign["b"]] ,functions["end"](strNum, X5) == X6, functions["symbolAt"](strNum, X5) == vars[view_assign["B"]] ),And (rn == vars["rule6"],functions["end"](strNum,X0) == X6, functions["end"](strNum,X5) == X6, functions["symbolAt"](strNum, X0) == vars[view_assign["B"]], X1 == X0+1, X1 == X2 ,X2 == X3 ,X3 == X4 ,X4 == X5 ,X6 == X5, functions["end"](strNum, X5) == X5, functions["symbolAt"](strNum, X5) == vars[view_assign["c"]] ))))


	s.add(functions["end"](strNum,0) > len(accept_string))
	
	for i in range(len(accept_string)+1):
		vars["z%d"%i] = Int('z%d'%i)
	s.add(vars["z0"] > 0)
	s.add(vars["z%d"%(len(accept_string))] <= functions["end"](strNum,0))
	
	# making the successor function
	for j in range(len(accept_string)):
		s.add(functions["lookAheadIndex"](strNum, vars["z%d"%j]+1) == vars["z%d"%(j+1)])
	
	# adding the stric inequality
	for i in range(1,len(accept_string)):
		s.add(And(vars["z%d"%i] < vars["z%d"%(i+1)], vars["z%d"%i] > vars["z%d"%(i-1)]))

	for i in range(len(accept_string)+1):
		OrList = []
		for t in terms:
			OrList.append(t == vars["z%d"%i])
		s.add(Or(OrList))

	s.add(functions["end"](strNum, 0) <= expansion_constant*len(accept_string))

	####################################################################################################

	# Start parsing with N1 as the first symbol
	view_assign = solver["view_assign"]
	astr,l,m = specs()
	astr = astr[0]

	s.add(ForAll(x, functions["valid"](x) == Implies(And(0 <= x, x <= functions["end"](strNum,0)), And( functions["lookAheadIndex"](strNum,x) > 0, Or([functions["lookAheadIndex"](strNum,x)==vars["z%d"%i] for i in range(len(accept_string)+1)]) ,Or(And(functions["symbolAt"](strNum, x) <= solver["term_end"], functions["symbolAt"](strNum, x) >= solver["term_start"], functions["lookAheadIndex"](strNum, x) == x), And(functions["symbolAt"](strNum, x) <= solver["non_term_end"], functions["symbolAt"](strNum, x) >= solver["non_term_start"], functions["lookAheadIndex"](strNum,x+1) == functions["lookAheadIndex"](strNum,x), Exists([rn, X1,X2,X3,X4,X5,X6], And(functions["parseTable"](functions["symbolAt"](strNum,x), functions["symbolAt"](strNum, functions["lookAheadIndex"](strNum,x))) == rn,Not(rn ==0),x <= X1, X1 <= X2, X2 <= X3, X3 <= X4, X4 <= X5, X5 <= X6, X6 <= functions["end"](strNum,0), functions["hardcode"](rn, x, X1, X2, X3, X4, X5, X6))))))), patterns=[functions["valid"](x)]))
	s.add(functions["lookAheadIndex"](strNum,0) == vars["z0"])

	for j in test_counter:
		sympredef = parser_main(astr,j)
		s.push()
		print "parse array lenght;",len(sympredef)
		for i in range(len(sympredef)):
			if i != j:
				s.add(functions["symbolAt"](strNum,i) == vars[view_assign[sympredef[i]]])
				print "Asserting: functions['symbolAt'](strNum,%d) == vars[%s]"%(i,view_assign[sympredef[i]])
			else:
				add_soft(solver,functions["symbolAt"](strNum,i) == vars[view_assign[sympredef[i]]])

		s.add(functions["symbolAt"](strNum,0) == vars["N1"])

		for i in range(j+1):
			if i == j:
				add_soft(solver, functions["symbolAt"](strNum,vars["z%d"%i]) == vars[accept_string[i]])
				continue
			if i != len(accept_string):
				s.add(functions["symbolAt"](strNum,vars["z%d"%i]) == vars[accept_string[i]])
			else:
				s.add(functions["symbolAt"](strNum,vars["z%d"%i]) == vars["dol"])
		
		for i in range(len(sympredef)+2):
			s.add(functions["valid"](i))
			
		p, unsat_soft_constrains, m = naive_maxsat(solver)

		tmp=int(str(m.evaluate(m_funs["ip_str1"](1, m_funs["succ"](1,i)))))
		accept_string[j] = tokens[tmp-solver["non_term_end"]]
		s.pop()

	
	
		# adding the respective terminal at different positions in parse action array
	p = [4,10,30,57,89]
	
	# asserting all other positions in parse action array should be non terminal
	# s.add(ForAll(x, Implies(Not(Or([x == vars["z%d"%i] for i in range(len(accept_string)+1)])), And(x <= solver["non_term_end"], x >= solver["non_term_start"]))))
	# s.add(ForAll(x, functions["valid"](x) == Implies(x < functions["end"](strNum,0), And(functions["lookAheadIndex"](strNum,x) <= len(accept_string), functions["lookAheadIndex"](strNum,x) >= 0,Or(And(functions["symbolAt"](strNum, x) <= solver["term_end"], functions["symbolAt"](strNum, x) >= solver["term_start"], functions["symbolAt"](strNum, x) == functions["ip_str1"](strNum, functions["lookAheadIndex"](strNum,x)), functions["succ"](strNum,functions["lookAheadIndex"](strNum,x)) == functions["lookAheadIndex"](strNum,x+1)), And(functions["symbolAt"](strNum, x) <= solver["non_term_end"], functions["symbolAt"](strNum, x) >= solver["non_term_start"], functions["lookAheadIndex"](strNum,x+1) == functions["lookAheadIndex"](strNum,x), Or(And(functions["symbolAt"](strNum,x) <= solver["term_end"], functions["symbolAt"](strNum,x) >= solver["term_start"]),Exists([rn, X1,X2,X3,X4,X5,X6], And(functions["parseTable"](functions["symbolAt"](strNum,x), functions["ip_str1"](strNum,functions["lookAheadIndex"](strNum,x))) == rn,Not(rn ==0),x <= X1, X1 <= X2, X2 <= X3, X3 <= X4, X4 <= X5, X5 <= X6, X6 <= functions["end"](strNum,0), functions["hardcode"](rn, x, X1, X2, X3, X4, X5, X6))))))))))
	 # functions["valid"](x) == Implies(And(0 <= x, x <= functions["end"](strNum,0)), And( functions["lookAheadIndex"](strNum,x) > 0, Or([functions["lookAheadIndex"](strNum,x)==vars["z%d"%i] for i in range(len(accept_string)+1)]) ,Or(And(functions["symbolAt"](strNum, x) <= solver["term_end"], functions["symbolAt"](strNum, x) >= solver["term_start"], functions["lookAheadIndex"](strNum, x) == x), And(functions["symbolAt"](strNum, x) <= solver["non_term_end"], functions["symbolAt"](strNum, x) >= solver["non_term_start"], functions["lookAheadIndex"](strNum,x+1) == functions["lookAheadIndex"](strNum,x), Exists([rn, X1,X2,X3,X4,X5,X6], And(functions["parseTable"](functions["symbolAt"](strNum,x), functions["symbolAt"](strNum, functions["lookAheadIndex"](strNum,x))) == rn,Not(rn ==0),x <= X1, X1 <= X2, X2 <= X3, X3 <= X4, X4 <= X5, X5 <= X6, X6 <= functions["end"](strNum,0), functions["hardcode"](rn, x, X1, X2, X3, X4, X5, X6)))))))

	# Starting lookAheadIndex


	# for i in range(expansion_constant*len(accept_string)):
	# 	# print "asserting parser start in %s"%str(datetime.timedelta(seconds=(calendar.timegm(time.gmtime()))))
	# 	# single_step(solver,strNum,i+1)
	# 	s.add(functions["valid"](i))
	# 	