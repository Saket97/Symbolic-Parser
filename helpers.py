from z3 import *
from solver import *
from init import *
from itertools import *
from msat import assert_and_track_soft, add_soft
constraint_no = 0
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
	terms = solver["terms"]
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
					print "eps\t",
			print ""
	# print "follow: ",m.evaluate(m_funs["follow"](m_vars['N3'], m_vars['dol']))
	# print "follow: ",m.evaluate(m_funs["follow"](m_vars['N1'], m_vars['dol']))
	accept_list = solver["accept_list"]
	print "accept_list ",accept_list
	i = -1
	# while i < len(accept_list[0]):
	print "corrected string: "
	while True:
		symbolValue = int(str(m.evaluate(m_funs["ip_str1"](1, m_funs["succ"](1,i)))))
		if symbolValue >= solver["term_end"]:
			return
		print "%s "%(tokens[symbolValue-num_nonterms]),
		i = int(str(m.evaluate(m_funs["succ"](1,i))))
	print ""

def assert_grammar_soft(S_target,S_source,req=False):

	s = S_target["constraints"]
	constdict = S_target["dictconst"]
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


def assert_grammar_hard(S_target,S_source,req=False):

	s = S_target["constraints"]

	num_rules = config['num_rules']
	num_nonterms = config['num_nonterms']
	num_terms = config['num_terms']
	size_rules = config['size_rules']

	if req:
		reqrules = req_rules(S_source)
	
		for r in range(num_rules):
			if reqrules[r]:
				s.add(S_target["functions"]["symbolInLHS"](r+1)==int(str(S_source["model"].evaluate(S_source["functions"]["symbolInLHS"](r+1)))))
				for i in range(1,size_rules+1):
					s.add(S_target["functions"]["symbolInRHS"](r+1,i)==int(str(S_source["model"].evaluate(S_source["functions"]["symbolInRHS"](r+1,i)))))
	else:
		for r in range(num_rules):
			s.add(S_target["functions"]["symbolInLHS"](r+1)==int(str(S_source["model"].evaluate(S_source["functions"]["symbolInLHS"](r+1)))))
			for i in range(1,size_rules+1):
				s.add(S_target["functions"]["symbolInRHS"](r+1,i)==int(str(S_source["model"].evaluate(S_source["functions"]["symbolInRHS"](r+1,i)))))


def add_bad_grammar(S_target,S_source,iterationNo):

	s = S_target["constraints"]

	num_rules = config['num_rules']
	num_nonterms = config['num_nonterms']
	num_terms = config['num_terms']
	size_rules = config['size_rules']

	for perm in list(permutations(range(1,num_nonterms))):
		# check reachable rules
		rules = req_rules(S_source)
		AndList = []
		for i in range(num_rules):
			if rules[i]:
				lhsSymbol = int(str(S_source["model"].evaluate(S_source["functions"]["symbolInLHS"](i+1))))
				tempList = []
				for j in range(size_rules):
					symbolValue = int(str(S_source["model"].evaluate(S_source["functions"]["symbolInRHS"](i+1,j+1))))
					if symbolValue < num_nonterms and symbolValue > 0:
						tempList.append(perm[symbolValue-1])
					else:
						tempList.append(symbolValue)
				if lhsSymbol > 0:
					AndList.append(S_target["functions"]["derivedBy"](tempList)==perm[lhsSymbol-1])
				else:
					AndList.append(S_target["functions"]["derivedBy"](tempList)==lhsSymbol)

		s.add(Not(And(AndList)))


def add_accept_string(solver,accept_string):

	s = solver["constraints"]
	constdict = solver["dictconst"]
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
	
	print "adding string constraints..."
	######## adding initial succ function constraint ######
	if solver["comment_out"] == True:
		for j in range(-1,len(accept_string)):
			add_soft(functions["succ"](strNum,j) == j+1, solver)

	for j in range(len(accept_string)):
		s.add(functions["ip_str"](strNum,j) == vars[accept_string[j]])
	s.add(functions["ip_str"](strNum,len(accept_string)) == vars["dol"])

	if solver["comment_out"] == True:
		####### making ipstr1 function 
		for j in range(-1,len(accept_string)):
			add_soft(functions["ip_str1"](strNum,functions["succ"](strNum,j)) == functions["ip_str"](strNum,j+1), solver)
		
		tmp = [i for i in range(-1, len(accept_string))]
		for i in range(solver["n_insertions"]):
			tmp.append(10000+i)
		for i in tmp:
			if i >= 10000:
				s.add(And(functions["pred"](strNum,i) < len(accept_string), functions["pred"](strNum,i) >= -1))
			### making pred function ###
			s.add(Implies(functions["succ"](strNum,i) >= 10000, If(i <= len(accept_string), functions["pred"](strNum,functions["succ"](strNum,i)) == i, functions["pred"](strNum,functions["succ"](strNum,i)) == functions["pred"](strNum,i))))
			## succ should always be greater than the number if it is not extra ###
			if i < len(accept_string):
				OrList = []
				OrList.append(And(functions["succ"](strNum,i) > i,functions["succ"](strNum,i) <= i+2))
				for j in range(solver["n_insertions"]):
					OrList.append(functions["succ"](strNum,i) == 10000+i)
				s.add(Or(OrList))
				# s.add(Or(And(functions["succ"](strNum,i) > i,functions["succ"](strNum,i) <= i+2), functions["succ"](strNum,i) == 1000, functions["succ"](strNum,i) == 1001))
			else:
				s.add(Or(And(functions["succ"](strNum, i) <= functions["pred"](strNum,i) + 2, functions["succ"](strNum,i) > functions["pred"](strNum,i)), And(functions["succ"](strNum,i) < 10000+solver["n_insertions"], functions["succ"](strNum,i)> 10000)))
				
			s.add(functions["succ"](strNum,i) >= 0)

		for i in tmp:
			OrList = []
			for t in terms+['dol']:
				if t == "eps":
					continue
				if t == "dol":
					if (i >= len(accept_string)-2 and i < 10000):
						OrList.append(functions["ip_str1"](strNum, i) == vars[t])
						# print functions["ip_str1"](strNum, i) == vars[t]
					else:
						OrList.append(Not(functions["ip_str1"](strNum, i) == vars["dol"]))
						# print Not(functions["ip_str1"](strNum, i) == vars["dol"])
					continue
				OrList.append(functions["ip_str1"](strNum, i) == vars[t])
				# print functions["ip_str1"](strNum, i) == vars[t]
			s.add(Or(OrList))

	# Start parsing with N1 as the first symbol
	
	s.add(functions["symbolAt"](strNum,1) == vars["N1"])

	# Starting lookAheadIndex
	s.add(functions["lookAheadIndex"](strNum,1) == 0)

	# Starting step
	s.add(functions["step"](strNum,0))

	# Do required number of steps
	for i in range(expansion_constant*len(accept_string)):
		single_step(solver,strNum,i+1)
	s.assert_and_track(functions["success"](strNum,expansion_constant*len(accept_string)),'parsing_string%d_success'%(strNum))
	constdict['parsing_string%d_success'%(strNum)] = functions["success"](strNum,expansion_constant*len(accept_string))

def add_reject_strings(solver):

	s = solver["constraints"]
	vars = solver["vars"]
	functions = solver["functions"]
	constdict = solver["dictconst"]

	assert("type" not in solver)
	solver["type"] = "reject"
	assert("num_strings" not in solver)
	solver["num_strings"] = len(reject_list)

	expansion_constant = config['expansion_constant']  #Determines the max. number of parse actions to take while parsing

	# Take input and construct the ip_str function
	for strNum in range(len(reject_list)):
		for j in range(len(reject_list[strNum])):
			s.assert_and_track(functions["ip_str"](strNum,j) == vars[reject_list[strNum][j]],'make_ipstr_reject_strNum%d_pos%d'%(strNum,j))
			constdict['make_ipstr_reject_strNum%d_pos%d'%(strNum,j)] = functions["ip_str"](strNum,j) == vars[reject_list[strNum][j]]
		s.assert_and_track(functions["ip_str"](strNum,len(reject_list[strNum]))==vars["dol"], 'make_ipstr_reject_strNum%d_pos%d'%(strNum,len(reject_list[strNum])))
		constdict['make_ipstr_reject_strNum%d_pos%d'%(strNum,len(reject_list[strNum]))] = functions["ip_str"](strNum,len(reject_list[strNum]))==vars["dol"]

	# Start parsing with N1 as the first symbol
	for strNum in range(len(reject_list)):
		s.add(functions["symbolAt"](strNum,1) == vars["N1"])

	# Starting lookAheadIndex
	for strNum in range(len(reject_list)):
		s.add(functions["lookAheadIndex"](strNum,1) == 0)

	# Starting step
	for strNum in range(len(reject_list)):
		s.add(functions["step"](strNum,0))

	SuccessList = []

	# Do required number of steps
	for strNum in range(len(reject_list)):
		for i in range(expansion_constant*len(reject_list[strNum])):
			single_step(solver,strNum,i+1)
		SuccessList.append(functions["success"](strNum,expansion_constant*len(reject_list[strNum])))

	s.assert_and_track(Or(SuccessList), 'successful_parsing_reject_strings')

######################################################

# OPTIMIZATION PROCEDURE

######################################################

def add_threshold(solver,unsat_core,threshold):
	s = solver["constraints"]

	clist = []
	for c in unsat_core:
		clist.append(If(c, 0, 1))
	s.add(Sum(clist) <= (IntVal(len(unsat_core) * threshold)))


def get_solution_optimize(SP):

	i=0
	s = SP["constraints"]
	print "Adding string " + str(i+1)
	accept_string=accept_list[0]
	add_accept_string(SP,accept_string)

	check_result = SP["constraints"].check()
	if check_result == unsat:
		return check_result

	SP["model"] = SP["constraints"].model()
	print_grammar(SP)

	i+=1
	while i < len(accept_list):
		print "Adding string " + str(i+1)
		accept_string=accept_list[i]
		add_accept_string(SP,accept_string)
		i+=1
		SP["constraints"].push()

		assumptions = assert_grammar_soft(S_source=SP,S_target=SP,req=True)

		check_result = SP["constraints"].check(assumptions)
		num_unsat=0
		while check_result == unsat:
			num_unsat+=1
			print "Unsat core #%d"%num_unsat
			unsatCore = SP["constraints"].unsat_core()

			if len(unsatCore) == 0:
				print "Failed to find unsat core"
				return unsat

			assumptions = [x for x in assumptions if x not in unsatCore]
			for x in unsatCore:
				s.add(x==False)
			check_result = SP["constraints"].check(assumptions)

		SP["model"] = SP["constraints"].model()
		print_grammar(SP)
		SP["constraints"].pop()

	return check_result



