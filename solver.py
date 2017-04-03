from z3 import *
from init import *
import datetime

def initialize_solver(solver):
	global config

	s = Solver()
	s.set(mbqi=False)
	s.set(macro_finder = True)
	if config['optimize']:
		s.set(unsat_core=True)

	num_rules = config['num_rules'] #Number of rules
	size_rules = config['size_rules']  #Max number of symbols in RHS
	num_nonterms = config['num_nonterms']  #Number of nonterms
	num_terms = config['num_terms']   #Number of terms

	vars = {}
	functions = {}

	x = Int('x')
	y = Int('y')
	z = Int('z')
	w = Int('w')

	######################################################

	# SYMBOLS

	######################################################

	symbol_counter = 0

	nonterms = ['N%d'%i for i in range(1,num_nonterms+1)]
	vars.update({"%s"%nt : Int('%s'%nt) for nt in nonterms}) #N1 is mapped to an integer variable N1 of z3

	terms = ['t%d'%i for i in range(1,num_terms+1)]
	vars.update({"%s"%t : Int('%s'%t) for t in terms})  #t1 is mapped to an integer variable t1 of z3

	vars.update({"eps": Int('eps')})

	for nt in nonterms:
		s.add(vars[nt]==symbol_counter)
		symbol_counter+=1

	solver["term_start"] = symbol_counter
	for t in terms:
		s.add(vars[t]==symbol_counter)
		symbol_counter+=1

	s.add(vars['eps']==symbol_counter)
	symbol_counter+=1
	solver["term_end"] = symbol_counter

	######################################################

	# BASIC FUNCTIONS
	#functions is a dictionary
	######################################################

	#has (second arg) been witnessed to be in first set of (first arg), in template rule number (third arg), according to construction condition number (fourth arg)? if no, return -1 else return the nonterm or term due to which this witness occurred
	functions["firstWitness"] = Function('firstWitness',IntSort(),IntSort(),IntSort(),IntSort(),IntSort())

	#has (second arg) been witnessed to be in follow set of (first arg), in template rule number (third arg), according to construction condition number (fourth arg) ? if no, return -1 else return the nonterm due to which this witness occurred
	functions["followWitness"] = Function('followWitness',IntSort(),IntSort(),IntSort(),IntSort(),IntSort())

	#Return the existential variable i for first set construction for the given nonterm, term pair
	functions["get_i"] = Function('get_i',IntSort(),IntSort(),IntSort())

	#Return the existential variable j for first set construction for the given nonterm, term pair
	functions["get_j"] = Function('get_j',IntSort(),IntSort(),IntSort())

	#Return the existential variable m for follow set construction for the given nonterm, term pair
	functions["get_m"] = Function('get_m',IntSort(),IntSort(),IntSort())

	#Return the existential variable n for follow set construction for the given nonterm, term pair
	functions["get_n"] = Function('get_n',IntSort(),IntSort(),IntSort())

	# is eps in the first set of the nonterm second arg after first arg iteration
	functions["epsWitness"] = Function('epsWitness',IntSort(),IntSort(),BoolSort())

	#is second arg in first of first arg?
	functions["first"] = Function('first',IntSort(),IntSort(),BoolSort())

	#is second arg in follow of first arg?
	functions["follow"] = Function('follow',IntSort(),IntSort(),BoolSort())

	#returns rule number in the parse table cell corresponding to (first arg) nonterm and (second arg) term
	functions["parseTable"] = Function('parseTable', IntSort(), IntSort(), IntSort())

	######################################################

	# TEMPLATE CONSTRAINTS

	######################################################

	for r in range(num_rules):
		print "new rule: %d"%r
		vars.update({"x%d"%(r*(size_rules+1)+1): Int('x%d'%(r*(size_rules+1)+1))})
		# print "x%d"%(r*(size_rules+1)+1)

		for i in range(2,size_rules+2):
			vars.update({"x%d"%(r*(size_rules+1)+i): Int('x%d'%(r*(size_rules+1)+i))})
			# print "x%d"%(r*(size_rules+1)+i)
	print "num_rules: ",num_rules

	# What is the symbol at (second arg) location in RHS of rule no (first arg)
	functions["symbolInRHS"] = Function('symbolInRHS', IntSort(), IntSort(), IntSort())

	# What is the symbol in LHS of rule no (first arg)
	functions["symbolInLHS"] = Function('symbolInLHS', IntSort(), IntSort())

	# Initialize symbolInRHS and symbolInLHS
	for r in range(num_rules):
		for i in range(2,size_rules+2):
			s.add(functions["symbolInRHS"](r+1,i-1) == vars["x%d"%(r*(size_rules+1)+i)])
		s.add(functions["symbolInLHS"](r+1) == vars["x%d"%(r*(size_rules+1)+1)])

	#Possible values for LHS and RHS. For any particular rule LHS must be non term and RHS should be combinatin of these
	for r in range(num_rules):
		OrList = []
		for n in nonterms:
			OrList.append(functions["symbolInLHS"](r+1)==vars[n])
		s.add(Or(OrList))

		for i in range(2,size_rules+2):
			OrList = []
			for v in terms+nonterms+["eps"]:
				OrList.append(functions["symbolInRHS"](r+1,i-1)==vars[v])
			s.add(Or(OrList))


	#Avoid trivial num_rules-+-+
	for r in range(1,num_rules+1):
		for i in range(2,size_rules+1):
			s.add(Implies(functions["symbolInRHS"](r,i)==vars["eps"],functions["symbolInRHS"](r,i-1)==vars["eps"]))
			s.add(Implies(functions["symbolInRHS"](r,size_rules)==functions["symbolInLHS"](r),functions["symbolInRHS"](r,size_rules-1)!=vars["eps"]))
	
	print "Teemplate declared in %s"%str(datetime.timedelta(seconds=(calendar.timegm(time.gmtime())-sp_time)))

	
	
	for r in range(1,num_rules+1):
		vars.update({"rule%d"%r: Int('rule%d'%r)})
		s.add(vars["rule%d"%r]==r)
	vars.update({"dol": Int('dol')})
	s.add(vars["dol"]==symbol_counter)
	sp_time = solver["start_time"]
	print "Parse table in %s"%str(datetime.timedelta(seconds=(calendar.timegm(time.gmtime())-sp_time)))

	######################################################

	# PARSE TABLE CONSTRAINTS

	######################################################

	for n in nonterms:
		for t in terms+['dol']:
			s.add(And(functions["parseTable"](vars[n],vars[t])<=num_rules,functions["parseTable"](vars[n],vars[t])>=0))


	
	# Lookup and constraint application was successful on step (second arg) in parse action array
	functions["step"] = Function('step', IntSort(), IntSort(), BoolSort())

	# True if parsing was completed on or before step (second arg)
	functions["success"] = Function('success', IntSort(), IntSort(), BoolSort())

	# The symbol being expanded at location (second arg) in the parse action array - can be term or nonterm
	functions["symbolAt"] = Function('symbolAt', IntSort(), IntSort(), IntSort())

	# The symbol at location (arg) in the input string
	functions["ip_str"] = Function('ip_str', IntSort(), IntSort(), IntSort())

	functions["ip_str1"] = Function('ip_str1', IntSort(), IntSort(), IntSort())

	functions["succ"] = Function('succ', IntSort(), IntSort(), IntSort())

	functions["pred"] = Function('pred', IntSort(), IntSort(), IntSort())

	# Index in the input string for the lookAhead symbol for the expansion at location (second arg) in the parse action array
	functions["lookAheadIndex"] = Function('lookAheadIndex', IntSort(), IntSort(), IntSort())

	# Where does the (second arg) symbol in RHS of the rule getting expanded at (third arg) step in parse action array, start expanding
	functions["startPosition"] = Function('startPosition', IntSort(), IntSort(), IntSort(), IntSort())

	# The ending index in the parse action array of the expansion of the functions["symbolAt"](second arg)
	functions["end"] = Function('end', IntSort(), IntSort(), IntSort())

	solver["constraints"] = s
	solver["vars"] = vars
	solver["functions"] = functions
	solver["terms"] = terms
	solver["nonterms"] = nonterms


# Incremental parsing step number i to constrain the parse action array for the input string strNum in the solver of solver
def single_step(solver,strNum,i):
	######################################################

	# PARSING ALGORITHM

	######################################################

	s = solver["constraints"]
	vars = solver["vars"]
	functions = solver["functions"]
	terms = solver["terms"]
	nonterms = solver["nonterms"]


	num_rules = config['num_rules'] #Number of rules
	size_rules = config['size_rules']  #Max number of symbols in RHS
	num_nonterms = config['num_nonterms']  #Number of nonterms
	num_terms = config['num_terms']   #Number of terms

	x = Int('x')

	if solver["comment_out"] == True:
		s.add(And(functions["ip_str1"](strNum,functions["lookAheadIndex"](strNum,i)) <= solver["term_end"],functions["ip_str1"](strNum,functions["lookAheadIndex"](strNum,i)) >= solver["term_start"] ))
		s.add(Not(functions["ip_str1"](strNum, functions["lookAheadIndex"](strNum,i)) == vars["eps"]))

	# Termination condition
	if solver["comment_out"] == True:
		s.add(Implies(And(functions["end"](strNum,1) == (i-1), functions["step"](strNum,i-1)), If(functions["ip_str1"](strNum,functions["lookAheadIndex"](strNum,i)) == vars["dol"], And(Not(functions["step"](strNum,i)),functions["success"](strNum,i)), And(Not(functions["step"](strNum,i)),Not(functions["success"](strNum,i))) ) ))
	else:
		s.add(Implies(And(functions["end"](strNum,1) == (i-1), functions["step"](strNum,i-1)), If(functions["ip_str"](strNum,functions["lookAheadIndex"](strNum,i)) == vars["dol"], And(Not(functions["step"](strNum,i)),functions["success"](strNum,i)), And(Not(functions["step"](strNum,i)),Not(functions["success"](strNum,i))) ) ))
	
	#Propagate success state on end of parse
	s.add(Implies(Not(functions["step"](strNum,i)),And(Not(functions["step"](strNum,i+1)),functions["success"](strNum,i+1)==functions["success"](strNum,i))))

	# For consuming term
	AndList = []
	if solver["comment_out"] == True:
		AndList.append(functions["lookAheadIndex"](strNum,i+1) == functions["succ"](strNum,functions["lookAheadIndex"](strNum,i)))	
	else:
		AndList.append(functions["lookAheadIndex"](strNum,i+1) == functions["lookAheadIndex"](strNum,i) + 1)
	AndList.append(functions["step"](strNum,i))
	AndList.append(Not(functions["success"](strNum,i)))
	AndList.append(functions["end"](strNum,i)==i)
	OrList = []
	for t in terms:
		OrList.append(functions["symbolAt"](strNum,i)==vars[t])
	if solver["comment_out"] == True:
		s.add(Implies(And(Or(OrList),functions["step"](strNum,i-1)), If(functions["symbolAt"](strNum,i)==functions["ip_str1"](strNum,functions["lookAheadIndex"](strNum,i)), And(AndList), And(Not(functions["step"](strNum,i)), Not(functions["success"](strNum,i))) ) ))
	else:
		s.add(Implies(And(Or(OrList),functions["step"](strNum,i-1)), If(functions["symbolAt"](strNum,i)==functions["ip_str"](strNum,functions["lookAheadIndex"](strNum,i)), And(AndList), And(Not(functions["step"](strNum,i)), Not(functions["success"](strNum,i))) ) ))

	# For expanding nonterm
	for k in range(1,size_rules+2):
		RHSList=[]
		AndList=[]
		for j in range(1,k):
			if solver["comment_out"] == True:
				RHSList.append(functions["symbolInRHS"](functions["parseTable"](functions["symbolAt"](strNum,i),functions["ip_str1"](strNum,functions["lookAheadIndex"](strNum,i))), j) == vars["eps"])
			else:
				RHSList.append(functions["symbolInRHS"](functions["parseTable"](functions["symbolAt"](strNum,i),functions["ip_str"](strNum,functions["lookAheadIndex"](strNum,i))), j) == vars["eps"])
			AndList.append(functions["startPosition"](strNum,j,i) == i)
			
			
		for j in range(k, size_rules + 1):
			if solver["comment_out"] == True:
				RHSList.append(functions["symbolInRHS"](functions["parseTable"](functions["symbolAt"](strNum,i),functions["ip_str1"](strNum,functions["lookAheadIndex"](strNum,i))), j) != vars["eps"])
			else:	
				RHSList.append(functions["symbolInRHS"](functions["parseTable"](functions["symbolAt"](strNum,i),functions["ip_str"](strNum,functions["lookAheadIndex"](strNum,i))), j) != vars["eps"])
			if j != k :
				AndList.append(functions["startPosition"](strNum,j,i) == functions["end"](strNum,functions["startPosition"](strNum,j-1,i)) + 1)	
			else:
				AndList.append(functions["startPosition"](strNum,j,i) == i+1)	
			if solver["comment_out"] == True:
				AndList.append(functions["symbolAt"](strNum,functions["startPosition"](strNum,j,i)) == functions["symbolInRHS"](functions["parseTable"](functions["symbolAt"](strNum,i),functions["ip_str1"](strNum,functions["lookAheadIndex"](strNum,i))), j))
			else:
				AndList.append(functions["symbolAt"](strNum,functions["startPosition"](strNum,j,i)) == functions["symbolInRHS"](functions["parseTable"](functions["symbolAt"](strNum,i),functions["ip_str"](strNum,functions["lookAheadIndex"](strNum,i))), j))
		
		AndList.append(functions["lookAheadIndex"](strNum,i+1) == functions["lookAheadIndex"](strNum,i))
		
		if k!=size_rules+1:
			AndList.append(functions["end"](strNum,i) == functions["end"](strNum,functions["startPosition"](strNum,size_rules,i)))
		else:
			AndList.append(functions["end"](strNum,i) == i)
		
		AndList.append(functions["step"](strNum,i))
		AndList.append( Not(functions["success"](strNum,i)) )

		OrList = []
		for n in nonterms:
			OrList.append(functions["symbolAt"](strNum,i)==vars[n])
		if solver["comment_out"] == True:
			s.add(Implies(And(Or(OrList),functions["step"](strNum,i-1)),If(functions["parseTable"](functions["symbolAt"](strNum,i),functions["ip_str1"](strNum,functions["lookAheadIndex"](strNum,i))) != 0, Implies(And(RHSList),And(AndList)), And(Not(functions["step"](strNum,i)),Not(functions["success"](strNum,i)) ) )))
		else:
			s.add(Implies(And(Or(OrList),functions["step"](strNum,i-1)),If(functions["parseTable"](functions["symbolAt"](strNum,i),functions["ip_str"](strNum,functions["lookAheadIndex"](strNum,i))) != 0, Implies(And(RHSList),And(AndList)), And(Not(functions["step"](strNum,i)),Not(functions["success"](strNum,i)) ) )))
