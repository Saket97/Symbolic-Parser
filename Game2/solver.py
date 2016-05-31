from z3 import *
from init import *
from test import *
from input_specs import *

def initialize_solver(solver):
	global config

	s = Solver()
	s.set(mbqi=True)
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

	for t in terms:
		s.add(vars[t]==symbol_counter)
		symbol_counter+=1

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

	for r in range(num_rules):
		vars.update({"x%d"%(r*(size_rules+1)+1): Int('x%d'%(r*(size_rules+1)+1))})

		for i in range(2,size_rules+2):
			vars.update({"x%d"%(r*(size_rules+1)+i): Int('x%d'%(r*(size_rules+1)+i))})

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

	functionArgs = [IntSort() for i in range(size_rules+1)]
	functions["derivedBy"] = Function('derivedBy',functionArgs)

	for r in range(num_rules):
		tempList = []
		for j in range(size_rules):
			tempList.append(functions["symbolInRHS"](r+1,j+1))
		s.add(functions["derivedBy"](tempList)==functions["symbolInLHS"](r+1))

	######################################################

	# FIRST SET WITNESS CONSTRAINTS

	######################################################

	for r in range(1,num_rules+1):
		vars.update({"rule%d"%r: Int('rule%d'%r)})
		s.add(vars["rule%d"%r]==r)

	num_conds = 1
	for r in range(1,2*size_rules+1):
		vars.update({"cond%d"%r: Int('cond%d'%r)})
		s.add(vars["cond%d"%r]==r)
		num_conds+=1

	# Definition constraint: firstWitness must either return -1 or return nonterm or term
	for n in nonterms+terms:
		for t in terms:
			for r in (1,num_rules+1):
				for c in range(1,2*size_rules+1):
					s.add(And(functions["firstWitness"](vars[n],vars[t],r,c) >= -1, functions["firstWitness"](vars[n],vars[t],r,c) < vars['eps'] ) )

	# Definition constraint: forall terms t, functions["firstWitness"](t,t,i_tt,j_tt) = t
	for t in terms:
		var = "%s%s"%(str(vars[t]),str(vars[t]))
		vars["i_%s"%var] = Int('i_%s'%var)
		vars["j_%s"%var] = Int('j_%s'%var)
		s.add(functions["firstWitness"](vars[t],vars[t],vars["i_%s"%var],vars["j_%s"%var])==vars[t])
		s.add(functions["get_i"](vars[t],vars[t])==vars["i_%s"%var])
		s.add(functions["get_j"](vars[t],vars[t])==vars["j_%s"%var])

	# Definition constraint: firstWitness must return -1 for -1 as nonterm arg
	for t in terms:
		for r in (1,num_rules+1):
			for c in range(1,2*size_rules+1):
				s.add(functions["firstWitness"](-1,vars[t],r,c) == -1 )

	# Definition constraint: epsWitness must be true for eps
	for i in range(num_rules+1):
		s.add(functions["epsWitness"](i,vars["eps"]))

	######################################################

	# FIRST SET WITNESS CONSTRUCTION

	######################################################

	for r in range(1,num_rules+1):
		for i in range(1,size_rules+1):
			for t in terms:
				tempList = []
				for j in range(1,i):
					tempList.append(functions["symbolInRHS"](r,j)==vars["eps"])
				tempList.append(functions["first"](functions["symbolInRHS"](r,i),vars[t]))
				tempList.append(functions["symbolInRHS"](r,i)!=functions["symbolInLHS"](r))

				temp = functions["firstWitness"](functions["symbolInRHS"](r,i),vars[t],functions["get_i"](functions["symbolInRHS"](r,i),vars[t]),functions["get_j"](functions["symbolInRHS"](r,i),vars[t]))
				for j in range(num_rules):
					temp = functions["firstWitness"](temp,vars[t],functions["get_i"](temp,vars[t]),functions["get_j"](temp,vars[t]))
				tempList.append(temp==vars[t])

				s.add(If(And(tempList), ( functions["firstWitness"](functions["symbolInLHS"](r),vars[t],vars["rule%d"%(r)],vars["cond%d"%(i)]) == functions["symbolInRHS"](r,i)), ( functions["firstWitness"](functions["symbolInLHS"](r),vars[t],vars["rule%d"%(r)],vars["cond%d"%(i)]) == -1) ))

					
		for i in range(1,size_rules+1):
			for t in terms:
				tempList = []
				for j in range(1,i):
					tempList.append(functions["first"](functions["symbolInRHS"](r,j),vars["eps"]))
				tempList.append(functions["first"](functions["symbolInRHS"](r,i),vars[t]))
				tempList.append(functions["symbolInRHS"](r,i)!=functions["symbolInLHS"](r))

				temp = functions["firstWitness"](functions["symbolInRHS"](r,i),vars[t],functions["get_i"](functions["symbolInRHS"](r,i),vars[t]),functions["get_j"](functions["symbolInRHS"](r,i),vars[t]))
				for j in range(num_rules):
					temp = functions["firstWitness"](temp,vars[t],functions["get_i"](temp,vars[t]),functions["get_j"](temp,vars[t]))
				tempList.append(temp==vars[t])

				s.add(If(And(tempList), ( functions["firstWitness"](functions["symbolInLHS"](r),vars[t],vars["rule%d"%(r)],vars["cond%d"%(size_rules+i)]) == functions["symbolInRHS"](r,i)), ( functions["firstWitness"](functions["symbolInLHS"](r),vars[t],vars["rule%d"%(r)],vars["cond%d"%(size_rules+i)]) == -1) ))


	##################### HANDLING FREE VARIABLES ##########################################
	for nt in nonterms:
		for t in terms:
			firstCondList = []
			for r in range(1,num_rules+1):
				for i in range(1,size_rules+1):
					tempList = []
					tempList.append(functions["symbolInLHS"](r) == vars[nt])
					for j in range(1,i):
						tempList.append(functions["symbolInRHS"](r,j)==vars["eps"])
					tempList.append(functions["first"](functions["symbolInRHS"](r,i),vars[t]))
					tempList.append(functions["symbolInRHS"](r,i)!=functions["symbolInLHS"](r))

					temp = functions["firstWitness"](functions["symbolInRHS"](r,i),vars[t],functions["get_i"](functions["symbolInRHS"](r,i),vars[t]),functions["get_j"](functions["symbolInRHS"](r,i),vars[t]))
					for j in range(num_rules):
						temp = functions["firstWitness"](temp,vars[t],functions["get_i"](temp,vars[t]),functions["get_j"](temp,vars[t]))
					tempList.append(temp==vars[t])
					firstCondList.append(And(tempList))

			for r in range(1,num_rules+1):
				for i in range(1,size_rules+1):
					tempList = []
					tempList.append(functions["symbolInLHS"](r) == vars[nt])
					for j in range(1,i):
						tempList.append(functions["first"](functions["symbolInRHS"](r,j),vars["eps"]))
					tempList.append(functions["first"](functions["symbolInRHS"](r,i),vars[t]))
					tempList.append(functions["symbolInRHS"](r,i)!=functions["symbolInLHS"](r))

					temp = functions["firstWitness"](functions["symbolInRHS"](r,i),vars[t],functions["get_i"](functions["symbolInRHS"](r,i),vars[t]),functions["get_j"](functions["symbolInRHS"](r,i),vars[t]))
					for j in range(num_rules):
						temp = functions["firstWitness"](temp,vars[t],functions["get_i"](temp,vars[t]),functions["get_j"](temp,vars[t]))
					tempList.append(temp==vars[t])					
					firstCondList.append(And(tempList))
			s.add(Implies(Not(Or(firstCondList)), Not(functions["first"](vars[nt],vars[t]))))
	########################################################################################
	for n in nonterms:
		OrList = []

		for r in range(1,num_rules+1):
			tempList = []
			tempList.append(functions["symbolInLHS"](r)==vars[n])
			for i in range(1,size_rules+1):
				tempList.append(functions["symbolInRHS"](r,i)==vars["eps"])
			OrList.append(And(tempList))

		s.add(Or(OrList)==functions["epsWitness"](0,vars[n]))

	for i in range(1,num_rules+1):

		for n in nonterms:
			OrList = []

			OrList.append(functions["epsWitness"](i-1,vars[n]))

			for r in range(1,num_rules+1):
				tempList = []
				tempList.append(functions["symbolInLHS"](r)==vars[n])
				for j in range(1,size_rules+1):
					tempList.append(functions["epsWitness"](i-1,functions["symbolInRHS"](r,j)))
				OrList.append(And(tempList))

			s.add(Or(OrList)==functions["epsWitness"](i,vars[n]))

	######################################################

	# FIRST SET CONSTRAINTS

	######################################################

	# Definition constraint: no nonterm in first sets
	for nt in terms+nonterms+["eps"]:
		for n in nonterms:
			s.add(Not(functions["first"](vars[nt],vars[n])))

	# Definition constraint: functions["first"](eps) = {eps}
	for t in terms:
		s.add(Not(functions["first"](vars["eps"],vars[t])))
	s.add(functions["first"](vars["eps"],vars["eps"]))
	

	# Definition constraint: functions["first"](term) = {term}
	for nt in terms:
		for t in terms+["eps"]:
			if nt == t:
				s.add(functions["first"](vars[nt],vars[t]))
			else:
				s.add(Not(functions["first"](vars[nt],vars[t])))


	######################################################

	# FIRST SET CONSTRUCTION

	######################################################

	for n in nonterms:
		for t in terms:
			var = "%(nonterm)s%(term)s"%{"nonterm":n, "term":t}
			
			vars["i_%s"%var] = Int("i_%s"%var)
			vars["j_%s"%var] = Int("j_%s"%var)
			s.add(functions["get_i"](vars[n],vars[t])==vars["i_%s%s"%(n,t)])
			s.add(functions["get_j"](vars[n],vars[t])==vars["j_%s%s"%(n,t)])

			tempList = []
			for i in range(1,num_rules+1):
				tempList.append(vars["i_%s"%var]==vars["rule%d"%(i)])
			s.add(Or(tempList))

			tempList = []
			for i in range(1,2*size_rules+1):
				tempList.append(vars["j_%s"%var]==vars["cond%d"%(i)])
			s.add(Or(tempList))

			
			for i in range(1,num_rules+1):
				s.add(Implies(And(functions["first"](vars[n],vars[t]),vars["i_%s"%var]==vars["rule%d"%(i)]),vars[n]==functions["symbolInLHS"](i)))

			s.add(Implies(functions["first"](vars[n],vars[t]),( functions["firstWitness"](vars[n],vars[t],vars["i_%s"%var],vars["j_%s"%var]) != -1)))

			tempList = []
			for i in range(1,num_rules+1):
				for j in range(1,2*size_rules+1):
					tempList.append( (functions["firstWitness"](vars[n],vars[t],vars["rule%d"%i],vars["cond%d"%j])) == -1)

			s.add(Implies(Not(functions["first"](vars[n],vars[t])),And(tempList)))

		s.add(functions["first"](vars[n],vars["eps"])==functions["epsWitness"](num_rules,vars[n]))

	######################################################

	# FOLLOW SET WITNESS CONSTRAINTS

	######################################################

	vars.update({"dol": Int('dol')})
	s.add(vars["dol"]==symbol_counter)

	while (num_conds <= (size_rules*(size_rules+1))/2):
		vars.update({"cond%d"%num_conds: Int('cond%d'%num_conds)})
		num_conds+=1
	
	# Definition constraint: followWitness must either return -1 or return nonterm or term
	for n in nonterms:
		for t in terms+["dol"]:
			for r in (1,num_rules+1):
				for c in range(1,(size_rules*(size_rules+1))/2):
					s.add(And(functions["followWitness"](vars[n],vars[t],r,c) >= -1, functions["followWitness"](vars[n],vars[t],r,c) < vars['eps'] ) )

	# Definition constraint: forall terms and dol t, functions["followWitness"](t,t,m_tt,n_tt) = t
	for t in terms+["dol"]:
		var = "%s%s"%(str(vars[t]),str(vars[t]))
		vars["m_%s"%var] = Int('m_%s'%var)
		vars["n_%s"%var] = Int('n_%s'%var)
		s.add(functions["followWitness"](vars[t],vars[t],vars["m_%s"%var],vars["n_%s"%var])==vars[t])
		s.add(functions["get_m"](vars[t],vars[t])==vars["m_%s"%var])
		s.add(functions["get_n"](vars[t],vars[t])==vars["n_%s"%var])

	# Definition constraint: followWitness must return -1 for -1 as nonterm arg
	for t in terms+["dol"]:
		for r in (1,num_rules+1):
			for c in range(1,(size_rules*(size_rules+1))/2):
				s.add(functions["followWitness"](-1,vars[t],r,c) == -1 )

	# Definition constraint: dol has been witnessed to be in functions["follow"](N1)
	# NOTE: N1 is the starting nonterm
	vars["m_N1dol"] = Int('m_N1dol')
	vars["n_N1dol"] = Int('n_N1dol')
	s.add(functions["get_m"](vars["N1"],vars["dol"])==vars["m_N1dol"])
	s.add(functions["get_n"](vars["N1"],vars["dol"])==vars["n_N1dol"])
	s.add(functions["followWitness"](vars["N1"],vars["dol"],vars["m_N1dol"],vars["n_N1dol"])==vars["dol"])

	######################################################

	# FOLLOW SET WITNESS CONSTRUCTION

	###############+																#######################################

	for r in range(1,num_rules+1):
		condNo = 1
		for i in range(1,size_rules):
			for j in range(i+1,size_rules+1):
				for t in terms:
					tempList = []
					for k in range(i+1,j):
						tempList.append(functions["first"](functions["symbolInRHS"](r,k),vars["eps"]))
					tempList.append(functions["first"](functions["symbolInRHS"](r,j),vars[t]))

					s.add((functions["followWitness"](functions["symbolInRHS"](r,i),vars[t],vars["rule%d"%(r)],vars["cond%d"%condNo])==vars[t])==And(tempList))

				condNo += 1

		followCondMid = condNo

		for i in range(1,size_rules+1):
			for t in terms+['dol']:
				tempList = []
				for k in range(i+1,size_rules+1):
					tempList.append(functions["first"](functions["symbolInRHS"](r,k),vars["eps"]))
				tempList.append(functions["follow"](functions["symbolInLHS"](r),vars[t]))
				tempList.append(functions["symbolInRHS"](r,i)!=functions["symbolInLHS"](r))

				temp = functions["followWitness"](functions["symbolInLHS"](r),vars[t],functions["get_i"](functions["symbolInLHS"](r),vars[t]),functions["get_j"](functions["symbolInLHS"](r),vars[t]))
				for j in range(num_rules):
					temp = functions["followWitness"](temp,vars[t],functions["get_m"](temp,vars[t]),functions["get_n"](temp,vars[t]))
				tempList.append(temp==vars[t])

				s.add((functions["followWitness"](functions["symbolInRHS"](r,i),vars[t],vars["rule%d"%(r)],vars["cond%d"%condNo])==functions["symbolInLHS"](r))==And(tempList))

			condNo += 1

		followCondEnd = condNo

	#################### HANDLING FREE VARIABLES ##########################################
	for nt in nonterms:
		for t in terms:
			followCondList = []
			for r in range(1,num_rules+1):
				# condNo = 1
				for i in range(1,size_rules):
					for j in range(i+1,size_rules+1):
						tempList = []
						tempList.append(functions["symbolInRHS"](r,i) == vars[nt])
						for k in range(i+1,j):
							tempList.append(functions["first"](functions["symbolInRHS"](r,k),vars["eps"]))
						tempList.append(functions["first"](functions["symbolInRHS"](r,j),vars[t]))

						followCondList.append(And(tempList))
						# s.add((functions["followWitness"](functions["symbolInRHS"](r,i),vars[t],vars["rule%d"%(r)],vars["cond%d"%condNo])==vars[t])==And(tempList))

			for r in range(1,num_rules+1):
				for i in range(1,size_rules+1):
					tempList = []
					tempList.append(functions["symbolInRHS"](r,i) == vars[nt])
					for k in range(i+1,size_rules+1):
						tempList.append(functions["first"](functions["symbolInRHS"](r,k),vars["eps"]))
					tempList.append(functions["follow"](functions["symbolInLHS"](r),vars[t]))
					tempList.append(functions["symbolInRHS"](r,i)!=functions["symbolInLHS"](r))

					temp = functions["followWitness"](functions["symbolInLHS"](r),vars[t],functions["get_i"](functions["symbolInLHS"](r),vars[t]),functions["get_j"](functions["symbolInLHS"](r),vars[t]))
					for j in range(num_rules):
						temp = functions["followWitness"](temp,vars[t],functions["get_m"](temp,vars[t]),functions["get_n"](temp,vars[t]))
					tempList.append(temp==vars[t])
					followCondList.append(And(tempList))				
					# s.add(((functions["followWitness"](functions["symbolInRHS"](r,i),vars[t],vars["rule%d"%(r)],vars["cond%d"%condNo])==functions["symbolInLHS"](r))==And(tempList)))
			
			s.add(Implies(Not(Or(followCondList)), Not (functions["follow"](vars[nt], vars[t]))))	
	#######################################################################################
	######################################################

	# FOLLOW SET CONSTRAINTS

	######################################################

	# Definition constraints: no nonterm and eps in follow sets
	for n in nonterms+["eps"]:
		for nt in nonterms+["eps"]:
			s.add(Not(functions["follow"](vars[n],vars[nt])))

	# Definition constraint: dol is in functions["follow"](N1)
	# NOTE: N1 is the starting nonterm
	s.add(functions["follow"](vars["N1"],vars["dol"]))

	######################################################

	# FOLLOW SET CONSTRUCTION

	######################################################

	for n in nonterms:
		for t in terms:
			var = "%(nonterm)s%(term)s"%{"nonterm":n, "term":t}
			vars["m_%s"%var] = Int("m_%s"%var)
			vars["n_%s"%var] = Int("n_%s"%var)
			s.add(functions["get_m"](vars[n],vars[t])==vars["m_%s"%(var)])
			s.add(functions["get_n"](vars[n],vars[t])==vars["n_%s"%(var)])

			tempList = []
			for i in range(1,num_rules+1):
				tempList.append(vars["m_%s"%var]==vars["rule%d"%(i)])
			s.add(Or(tempList))

			tempList = []
			for i in range(1,followCondEnd):
				tempList.append(vars["n_%s"%var]==vars["cond%d"%i])
			s.add(Or(tempList))

			for r in range(1,num_rules+1):
				condNo = 1
				for i in range(1,size_rules):
					for j in range(j+1,size_rules+1):
						s.add(Implies(And(functions["follow"](vars[n],vars[t]),vars["m_%s"%var]==vars["rule%d"%(r)],vars["n_%s"%var]==vars["cond%d"%(condNo)]),vars[n]==functions["symbolInRHS"](r,i)))
						condNo += 1

				for i in range(1,size_rules+1):
					s.add(Implies(And(functions["follow"](vars[n],vars[t]),vars["m_%s"%var]==vars["rule%d"%(r)],vars["n_%s"%var]==vars["cond%d"%(condNo)]),vars[n]==functions["symbolInRHS"](r,i)))
					condNo += 1

			s.add(Implies(functions["follow"](vars[n],vars[t]),functions["followWitness"](vars[n],vars[t],vars["m_%s"%var],vars["n_%s"%var])!=-1))

			tempList = []
			for i in range(1,num_rules+1):
				for j in range(1,followCondEnd):
					tempList.append(functions["followWitness"](vars[n],vars[t],vars["rule%d"%i],vars["cond%d"%j])==-1)
			s.add(Implies(Not(functions["follow"](vars[n],vars[t])),And(tempList)))

		t = "dol"
		if n != "N1":
			var = "%(nonterm)s%(dol)s"%{"nonterm":n,"dol":t}
			vars["m_%s"%var] = Int("m_%s"%var)
			vars["n_%s"%var] = Int("n_%s"%var)
			s.add(functions["get_m"](vars[n],vars[t])==vars["m_%s"%(var)])
			s.add(functions["get_n"](vars[n],vars[t])==vars["n_%s"%(var)])


			tempList = []
			for r in range(1,num_rules+1):
				tempList.append(vars["m_%s"%var]==vars["rule%d"%(r)])
			s.add(Or(tempList))

			tempList = []
			for i in range(followCondMid,followCondEnd):
				tempList.append(vars["n_%s"%var]==vars["cond%d"%i])
			s.add(Or(tempList))

			for r in range(1,num_rules+1):
				condNo = followCondMid
				for i in range(1,size_rules+1):
					s.add(Implies(And(functions["follow"](vars[n],vars[t]),vars["m_%s"%var]==vars["rule%d"%(r)],vars["n_%s"%var]==vars["cond%d"%(condNo)]),vars[n]==functions["symbolInRHS"](r,i)))
					condNo += 1

			s.add(Implies(functions["follow"](vars[n],vars[t]),functions["followWitness"](vars[n],vars[t],vars["m_%s"%var],vars["n_%s"%var])!=-1))

			tempList = []
			for i in range(1,num_rules+1):
				for j in range(followCondMid,followCondEnd):
					tempList.append(functions["followWitness"](vars[n],vars[t],vars["rule%d"%i],vars["cond%d"%j])==-1)
			s.add(Implies(Not(functions["follow"](vars[n],vars[t])),And(tempList)))

	######################################################

	# PARSE TABLE CONSTRAINTS

	######################################################

	for n in nonterms:
		for t in terms+['dol']:
			s.add(And(functions["parseTable"](vars[n],vars[t])<=num_rules,functions["parseTable"](vars[n],vars[t])>=0))

	######################################################

	# PARSE TABLE CONSTRUCTION

	######################################################

	for n in nonterms:
		for t in terms:
			for r in range(1,num_rules+1):
				tempAnd = []
				for i in range(1,size_rules+1):
					tempList = []
					for j in range(1,i):
						tempList.append(functions["first"](functions["symbolInRHS"](r,j),vars["eps"]))
					tempList.append(functions["first"](functions["symbolInRHS"](r,i),vars[t]))
					tempAnd.append(And(tempList))
				
				tempList = []	
				for i in range(1,size_rules+1):
					tempList.append(functions["first"](functions["symbolInRHS"](r,i),vars["eps"]))
				tempList.append(functions["follow"](functions["symbolInLHS"](r),vars[t]))
				tempAnd.append(And(tempList))

				s.add((functions["parseTable"](vars[n],vars[t])==vars["rule%d"%r])==And(functions["symbolInLHS"](r)==vars[n],Or(tempAnd)))

		for r in range(1,num_rules+1):
			tempList = []
			for i in range(1,size_rules+1):
				tempList.append(functions["first"](functions["symbolInRHS"](r,i),vars["eps"]))
			tempList.append(functions["follow"](functions["symbolInLHS"](r),vars["dol"]))

			s.add((functions["parseTable"](vars[n],vars["dol"])==vars["rule%d"%r])==And(functions["symbolInLHS"](r)==vars[n],And(tempList)))

	######################################################

	# PARSING FUNCTIONS

	######################################################

	#We take an 'array' of parse actions and use that to process the input, using the following functions

	#The following functions are defined for parsing the (first arg) input string
	# Lookup and constraint application was successful on step (second arg) in parse action array
	functions["step"] = Function('step', IntSort(), IntSort(), BoolSort())

	# True if parsing was completed on or before step (second arg)
	functions["success"] = Function('success', IntSort(), IntSort(), BoolSort())

	# The symbol being expanded at location (second arg) in the parse action array - can be term or nonterm
	functions["symbolAt"] = Function('symbolAt', IntSort(), IntSort(), IntSort())

	# The symbol at location (arg) in the input string
	functions["ip_str"] = Function('ip_str', IntSort(), IntSort(), IntSort())

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

	# Termination condition
	s.add(Implies(And(functions["end"](strNum,1) == (i-1), functions["step"](strNum,i-1)), If(functions["ip_str"](strNum,functions["lookAheadIndex"](strNum,i)) == vars["dol"], And(Not(functions["step"](strNum,i)),functions["success"](strNum,i)), And(Not(functions["step"](strNum,i)),Not(functions["success"](strNum,i))) ) ))
	
	#Propagate success state on end of parse
	s.add(Implies(Not(functions["step"](strNum,i)),And(Not(functions["step"](strNum,i+1)),functions["success"](strNum,i+1)==functions["success"](strNum,i))))

	# For consuming term
	AndList=[]
	AndList.append(functions["lookAheadIndex"](strNum,i+1) == functions["lookAheadIndex"](strNum,i) + 1)
	AndList.append(functions["step"](strNum,i))
	AndList.append(Not(functions["success"](strNum,i)))
	AndList.append(functions["end"](strNum,i)==i)
	OrList = []
	for t in terms:
		OrList.append(functions["symbolAt"](strNum,i)==vars[t])
	s.add(Implies(And(Or(OrList),functions["step"](strNum,i-1)), If(functions["symbolAt"](strNum,i)==functions["ip_str"](strNum,functions["lookAheadIndex"](strNum,i)), And(AndList), And(Not(functions["step"](strNum,i)), Not(functions["success"](strNum,i))) ) ))

	# For expanding nonterm
	for k in range(1,size_rules+2):
		RHSList=[]
		AndList=[]
		for j in range(1,k):
			RHSList.append(functions["symbolInRHS"](functions["parseTable"](functions["symbolAt"](strNum,i),functions["ip_str"](strNum,functions["lookAheadIndex"](strNum,i))), j) == vars["eps"])
			AndList.append(functions["startPosition"](strNum,j,i) == i)
			
			
		for j in range(k, size_rules + 1):
			RHSList.append(functions["symbolInRHS"](functions["parseTable"](functions["symbolAt"](strNum,i),functions["ip_str"](strNum,functions["lookAheadIndex"](strNum,i))), j) != vars["eps"])
			if j != k :
				AndList.append(functions["startPosition"](strNum,j,i) == functions["end"](strNum,functions["startPosition"](strNum,j-1,i)) + 1)	
			else:
				AndList.append(functions["startPosition"](strNum,j,i) == i+1)	
			AndList.append(functions["symbolAt"](strNum,functions["startPosition"](strNum,j,i)) == functions["symbolInRHS"](functions["parseTable"](functions["symbolAt"](strNum,i),functions["ip_str"](strNum,functions["lookAheadIndex"](strNum,i))), j))
		
		AndList.append(functions["lookAheadIndex"](strNum,i+1) == functions["lookAheadIndex"](strNum,i))
		
		if k!=size_rules+1:
			AndList.append(functions["end"](strNum,i) == functions["end"](strNum,functions["startPosition"](strNum,size_rules,i)))
		else:
			AndList.append(functions["end"](strNum,i) == i)
		
		AndList.append(functions["step"](strNum,i))
		AndList.append( Not(functions["success"](strNum,i))  )

		OrList = []
		for n in nonterms:
			OrList.append(functions["symbolAt"](strNum,i)==vars[n])
		s.add(Implies(And(Or(OrList),functions["step"](strNum,i-1)),If(functions["parseTable"](functions["symbolAt"](strNum,i),functions["ip_str"](strNum,functions["lookAheadIndex"](strNum,i))) != 0, Implies(And(RHSList),And(AndList)), And(Not(functions["step"](strNum,i)),Not(functions["success"](strNum,i)) ) )))
