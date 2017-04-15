from z3 import *
from init import *
import datetime
import calendar
import time

def initialize_solver(solver):
	global config
	s = Solver()
	s.set(mbqi=False)
	s.set(macro_finder = True)
	s.set(timeout=120000)
	s.set("qi.profile",True)
	s.set("qi.profile_freq",1000)
	if config['optimize']:
		s.set(unsat_core=True)

	strNum = 1
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

	# num_terms does not include $
	terms = ['t%d'%i for i in range(1,num_terms+1)]
	# terms.append("dol")
	vars.update({"%s"%t : Int('%s'%t) for t in terms})  #t1 is mapped to an integer variable t1 of z3

	vars.update({"eps": Int('eps')})

	solver["non_term_start"] = symbol_counter
	for nt in nonterms:
		s.add(vars[nt]==symbol_counter)
		solver["non_term_end"] = symbol_counter
		symbol_counter+=1

	solver["term_start"] = symbol_counter
	for t in terms:
		s.add(vars[t]==symbol_counter)
		solver["term_end"] = symbol_counter
		symbol_counter+=1

	vars.update({"dol": Int('dol')})
	s.add(vars["dol"]==symbol_counter)
	solver["term_end"] = symbol_counter
	symbol_counter += 1
	s.add(vars['eps']==symbol_counter)
	symbol_counter+=1
	

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
	print "Teemplate declaration starts in %s"%str(datetime.timedelta(seconds=(calendar.timegm(time.gmtime()))))

	for r in range(num_rules):
		vars.update({"x%d"%(r*(size_rules+1)+1): Int('x%d'%(r*(size_rules+1)+1))})

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

	print "Teemplate declared in %s"%str(datetime.timedelta(seconds=(calendar.timegm(time.gmtime()))))

	
	
	for r in range(1,num_rules+1):
		vars.update({"rule%d"%r: Int('rule%d'%r)})
		s.add(vars["rule%d"%r]==r)
	
	
	print "Parse table in %s"%str(datetime.timedelta(seconds=(calendar.timegm(time.gmtime()))))

	######################################################

	# PARSE TABLE CONSTRAINTS

	######################################################

	for n in nonterms:
		for t in terms+['dol']:
			s.add(And(functions["parseTable"](vars[n],vars[t])<=num_rules,functions["parseTable"](vars[n],vars[t])>=0))


	
	# The symbol being expanded at location (second arg) in the parse action array - can be term or nonterm
	functions["symbolAt"] = Function('symbolAt', IntSort(), IntSort(), IntSort())

	# Index in the input string for the lookAhead symbol for the expansion at location (second arg) in the parse action array
	functions["lookAheadIndex"] = Function('lookAheadIndex', IntSort(), IntSort(), IntSort())

	# The ending index in the parse action array of the expansion of the functions["symbolAt"](second arg)
	functions["end"] = Function('end', IntSort(), IntSort(), IntSort())

	# says whether each position in the array is successful or not. symbolAt, i 
	functions["valid"] = Function('valid', IntSort(), BoolSort())

	# one of these rules should apply. rule, lhs, elements in rhs, start and end of all elements in rhs.
	functions["hardcode"] = Function('hardcode', IntSort(), IntSort(), IntSort(),IntSort(), IntSort(), IntSort(), IntSort(), IntSort(), BoolSort() )
	# (rn Int) (X0 Int) (X1 Int) (X2 Int) (X3 Int) (X4 Int)
	
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

	# if solver["comment_out"] == True:
	# 	# lookahead should be a terminal
	# 	s.add(And(functions["ip_str1"](strNum,functions["lookAheadIndex"](strNum,i)) <= solver["term_end"],functions["ip_str1"](strNum,functions["lookAheadIndex"](strNum,i)) >= solver["term_start"] ))
	# 	s.add(Not(functions["ip_str1"](strNum, functions["lookAheadIndex"](strNum,i)) == vars["eps"]))

	# Termination condition
	# if solver["comment_out"] == True:
	# 	s.add(Implies(And(functions["end"](strNum,1) == (i-1), functions["step"](strNum,i-1)), If(functions["ip_str1"](strNum,functions["lookAheadIndex"](strNum,i)) == vars["dol"], And(Not(functions["step"](strNum,i)),functions["success"](strNum,i)), And(Not(functions["step"](strNum,i)),Not(functions["success"](strNum,i))) ) ))
	# else:
	# 	s.add(Implies(And(functions["end"](strNum,1) == (i-1), functions["step"](strNum,i-1)), If(functions["ip_str"](strNum,functions["lookAheadIndex"](strNum,i)) == vars["dol"], And(Not(functions["step"](strNum,i)),functions["success"](strNum,i)), And(Not(functions["step"](strNum,i)),Not(functions["success"](strNum,i))) ) ))
	
	#Propagate success state on end of parse
	# s.add(Implies(Not(functions["step"](strNum,i)),And(Not(functions["step"](strNum,i+1)),functions["success"](strNum,i+1)==functions["success"](strNum,i))))

	# For consuming term
	AndList = []
	# if solver["comment_out"] == True:
	# 	AndList.append(functions["lookAheadIndex"](strNum,i+1) == functions["succ"](strNum,functions["lookAheadIndex"](strNum,i)))
	# else:
	# 	AndList.append(functions["lookAheadIndex"](strNum,i+1) == functions["lookAheadIndex"](strNum,i) + 1)
	AndList.append(functions["step"](strNum,i)) # this step should be successful
	AndList.append(Not(functions["success"](strNum,i))) # parsing should not complete till now
	AndList.append(functions["end"](strNum,i)==i) # terminal should start and end at same index
	OrList = []
	for t in terms:
		OrList.append(functions["symbolAt"](strNum,i)==vars[t]) # symbol should must be a terminal

	if solver["comment_out"] == True:
		s.add(Implies(And(Or(OrList),functions["step"](strNum,i-1)), If(functions["symbolAt"](strNum,i)==functions["ip_str1"](strNum,functions["lookAheadIndex"](strNum,i)), And(AndList), And(Not(functions["step"](strNum,i)), Not(functions["success"](strNum,i))))))
	else:
		s.add(Implies(And(Or(OrList),functions["step"](strNum,i-1)), If(functions["symbolAt"](strNum,i)==functions["ip_str"](strNum,functions["lookAheadIndex"](strNum,i)), And(AndList), And(Not(functions["step"](strNum,i)), Not(functions["success"](strNum,i))) ) ))

	# For expanding nonterm
	OrList = []
	for n in nonterms:
		OrList.append(functions["symbolAt"](strNum,i)==vars[n]) # Symbol should be non terminal

	RHSList=[]	
	RHSList.append(functions["lookAheadIndex"](strNum,i+1) == functions["lookAheadIndex"](strNum,i)) # lookahead shouldn't change
	# RHSList.append(If(functions["symbolInRHS"](functions["parseTable"](functions["symbolAt"](strNum,i),functions["ip_str1"](strNum,functions["lookAheadIndex"](strNum,i))), size_rules) == vars["eps"], functions["end"](strNum,i) == i, functions["end"](strNum,i) == functions["end"](strNum,functions["startPosition"](strNum,size_rules,i)) ))	
	RHSList.append(Implies(functions["symbolInRHS"](functions["parseTable"](functions["symbolAt"](strNum,i),functions["ip_str1"](strNum,functions["lookAheadIndex"](strNum,i))), size_rules) == vars["eps"], functions["end"](strNum,i) == i))	
	RHSList.append(Implies(functions["symbolInRHS"](functions["parseTable"](functions["symbolAt"](strNum,i),functions["ip_str1"](strNum,functions["lookAheadIndex"](strNum,i))), size_rules) != vars["eps"], functions["end"](strNum,i) == functions["end"](strNum,functions["startPosition"](strNum,size_rules,i)) ))	
	for k in range(1, size_rules + 1):
		if solver["comment_out"] == True:
			RHSList.append(Implies(functions["symbolInRHS"](functions["parseTable"](functions["symbolAt"](strNum,i),functions["ip_str1"](strNum,functions["lookAheadIndex"](strNum,i))), k) == vars["eps"], functions["startPosition"](strNum,k,i) == i))
			if k == 1:
				RHSList.append(Implies(functions["symbolInRHS"](functions["parseTable"](functions["symbolAt"](strNum,i),functions["ip_str1"](strNum,functions["lookAheadIndex"](strNum,i))), k) != vars["eps"], And(functions["startPosition"](strNum,k,i) == i+1, functions["symbolAt"](strNum,functions["startPosition"](strNum,k,i)) == functions["symbolInRHS"](functions["parseTable"](functions["symbolAt"](strNum,i),functions["ip_str1"](strNum,functions["lookAheadIndex"](strNum,i))), k))))				
			else:
				RHSList.append(Implies(functions["symbolInRHS"](functions["parseTable"](functions["symbolAt"](strNum,i),functions["ip_str1"](strNum,functions["lookAheadIndex"](strNum,i))), k) != vars["eps"], And( If(functions["symbolInRHS"](functions["parseTable"](functions["symbolAt"](strNum,i),functions["ip_str1"](strNum,functions["lookAheadIndex"](strNum,i))), k-1) != vars["eps"], functions["startPosition"](strNum,k,i) == functions["end"](strNum,functions["startPosition"](strNum,k-1,i)) + 1, functions["startPosition"](strNum,k,i) == i + 1 )  , functions["symbolAt"](strNum,functions["startPosition"](strNum,k,i)) == functions["symbolInRHS"](functions["parseTable"](functions["symbolAt"](strNum,i),functions["ip_str1"](strNum,functions["lookAheadIndex"](strNum,i))), k))))		
	
	RHSList.append(functions["step"](strNum,i))
	RHSList.append( Not(functions["success"](strNum,i)) )
