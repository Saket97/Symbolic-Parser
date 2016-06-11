from z3 import *
from init import *
from test import *
from input_specs import *

constraint_no = 0
def initialize_solver(solver):
	global config
	global constraint_no
	s = Solver()

	s.set(mbqi=True)
	if config['optimize']:
		s.set(unsat_core=True)
	constdict = solver['dictconst']
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
		s.assert_and_track(vars[nt]==symbol_counter,'constraint45-%d'%(constraint_no))
		constdict['constraint45-%d'%(constraint_no)] = vars[nt]==symbol_counter
		constraint_no += 1
		symbol_counter+=1

	for t in terms:
		s.assert_and_track(vars[t]==symbol_counter, 'constraint51-%d'%(constraint_no))
		constdict['constraint51-%d'%(constraint_no)] = vars[t]==symbol_counter
		constraint_no += 1
		symbol_counter+=1

	s.assert_and_track(vars['eps']==symbol_counter, 'constraint56-%d'%(constraint_no))
	constdict['constraint56-%d'%(constraint_no)] = vars['eps']==symbol_counter
	constraint_no += 1
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
			s.assert_and_track(functions["symbolInRHS"](r+1,i-1) == vars["x%d"%(r*(size_rules+1)+i)], 'sInRhs%d'%(r*(size_rules+1)+i))
			constdict['sInRhs%d'%(r*(size_rules+1)+i)]= functions["symbolInRHS"](r+1,i-1) == vars["x%d"%(r*(size_rules+1)+i)]
		s.assert_and_track(functions["symbolInLHS"](r+1) == vars["x%d"%(r*(size_rules+1)+1)],'sInlhs:x%d'%(r*(size_rules+1)+1))
		constdict['sInlhs:x%d'%(r*(size_rules+1)+1)] = functions["symbolInLHS"](r+1) == vars["x%d"%(r*(size_rules+1)+1)]

	#Possible values for LHS and RHS. For any particular rule LHS must be non term and RHS should be combinatin of these
	for r in range(num_rules):
		OrList = []
		for n in nonterms:
			OrList.append(functions["symbolInLHS"](r+1)==vars[n])
		s.assert_and_track(Or(OrList), 'constraint129-%d'%(constraint_no))
		constdict['constraint129-%d'%(constraint_no)] = Or(OrList)
		constraint_no += 1

		for i in range(2,size_rules+2):
			OrList = []
			for v in terms+nonterms+["eps"]:
				OrList.append(functions["symbolInRHS"](r+1,i-1)==vars[v])
			s.assert_and_track(Or(OrList), 'constraint137-%d'%(constraint_no))
			constdict['constraint137-%d'%(constraint_no)] = Or(OrList)


	#Avoid trivial num_rules-+-+
	for r in range(1,num_rules+1):
		s.assert_and_track(Implies(functions["symbolInRHS"](r,size_rules)==functions["symbolInLHS"](r),functions["symbolInRHS"](r,size_rules-1)!=vars["eps"]),'leftRecursion%d'%(r))
		for i in range(2,size_rules+1):
			s.assert_and_track(Implies(functions["symbolInRHS"](r,i)==vars["eps"],functions["symbolInRHS"](r,i-1)==vars["eps"]), 'epsConst%d,%d'%(r,i))
			constdict['epsConst%d,%d'%(r,i)] = Implies(functions["symbolInRHS"](r,i)==vars["eps"],functions["symbolInRHS"](r,i-1)==vars["eps"])
			constdict['leftRecursion%d'%(r)] = Implies(functions["symbolInRHS"](r,size_rules)==functions["symbolInLHS"](r),functions["symbolInRHS"](r,size_rules-1)!=vars["eps"])
	functionArgs = [IntSort() for i in range(size_rules+1)]
	functions["derivedBy"] = Function('derivedBy',functionArgs)

	for r in range(num_rules):
		tempList = []
		for j in range(size_rules):
			tempList.append(functions["symbolInRHS"](r+1,j+1))
		s.assert_and_track(functions["derivedBy"](tempList)==functions["symbolInLHS"](r+1), 'constraint155-%d'%(constraint_no))
		constdict['constraint155-%d'%(constraint_no)] = functions["derivedBy"](tempList)==functions["symbolInLHS"](r+1)
		constraint_no += 1

	######################################################

	# FIRST SET WITNESS CONSTRAINTS

	######################################################

	for r in range(1,num_rules+1):
		vars.update({"rule%d"%r: Int('rule%d'%r)})
		s.assert_and_track(vars["rule%d"%r]==r, 'constraint167-%d'%(constraint_no))
		constdict['constraint167-%d'%(constraint_no)] = vars["rule%d"%(r)]==r
		constraint_no += 1

	num_conds = 1
	for r in range(1,2*size_rules+1):
		vars.update({"cond%d"%r: Int('cond%d'%r)})
		s.assert_and_track(vars["cond%d"%r]==r, 'constraint174-%d'%(constraint_no))
		constdict['constraint174-%d'%(constraint_no)] = vars["cond%d"%r]==r
		constraint_no += 1
		num_conds+=1

	# Definition constraint: firstWitness must either return -1 or return nonterm or term
	for n in nonterms+terms:
		for t in terms:
			for r in (1,num_rules+1):
				for c in range(1,2*size_rules+1):
					s.assert_and_track(And(functions["firstWitness"](vars[n],vars[t],r,c) >= -1, functions["firstWitness"](vars[n],vars[t],r,c) < vars['eps'] ),'firstWitnessReturn%s,%s,%d,%d'%(n,t,r,c) )
					constdict['firstWitnessReturn%s,%s,%d,%d'%(n,t,r,c)] = And(functions["firstWitness"](vars[n],vars[t],r,c) >= -1, functions["firstWitness"](vars[n],vars[t],r,c) < vars['eps'] )

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
				s.assert_and_track(functions["firstWitness"](-1,vars[t],r,c) == -1, 'constraint200-%d'%(constraint_no) )
				constdict['constraint200-%d'%(constraint_no)] = functions["firstWitness"](-1,vars[t],r,c) == -1
				constraint_no += 1

	# Definition constraint: epsWitness must be true for eps
	for i in range(num_rules+1):
		s.assert_and_track(functions["epsWitness"](i,vars["eps"]), 'constraint206-%d'%(constraint_no))
		constdict['constraint206-%d'%(constraint_no)] = functions["epsWitness"](i,vars["eps"])
		constraint_no += 1

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

				s.assert_and_track(If(And(tempList), ( functions["firstWitness"](functions["symbolInLHS"](r),vars[t],vars["rule%d"%(r)],vars["cond%d"%(i)]) == functions["symbolInRHS"](r,i)), ( functions["firstWitness"](functions["symbolInLHS"](r),vars[t],vars["rule%d"%(r)],vars["cond%d"%(i)]) == -1) ), 'firstseteps%d,%d,%s'%(r,i,t))
				constdict['firstseteps%d,%d,%s'%(r,i,t)] = If(And(tempList), ( functions["firstWitness"](functions["symbolInLHS"](r),vars[t],vars["rule%d"%(r)],vars["cond%d"%(i)]) == functions["symbolInRHS"](r,i)), ( functions["firstWitness"](functions["symbolInLHS"](r),vars[t],vars["rule%d"%(r)],vars["cond%d"%(i)]) == -1) )

					
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

				s.assert_and_track(If(And(tempList), ( functions["firstWitness"](functions["symbolInLHS"](r),vars[t],vars["rule%d"%(r)],vars["cond%d"%(size_rules+i)]) == functions["symbolInRHS"](r,i)), ( functions["firstWitness"](functions["symbolInLHS"](r),vars[t],vars["rule%d"%(r)],vars["cond%d"%(size_rules+i)]) == -1) ), 'firstsetfirsteps%d,%d,%s'%(r,i,t))
				constdict['firstsetfirsteps%d,%d,%s'%(r,i,t)] = If(And(tempList), ( functions["firstWitness"](functions["symbolInLHS"](r),vars[t],vars["rule%d"%(r)],vars["cond%d"%(size_rules+i)]) == functions["symbolInRHS"](r,i)), ( functions["firstWitness"](functions["symbolInLHS"](r),vars[t],vars["rule%d"%(r)],vars["cond%d"%(size_rules+i)]) == -1) )
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

		s.assert_and_track(Or(OrList)==functions["epsWitness"](0,vars[n]),'%s->eps'%(n))
		constdict['%s->eps'%(n)] = Or(OrList)==functions["epsWitness"](0,vars[n])

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

			s.assert_and_track(Or(OrList)==functions["epsWitness"](i,vars[n]), 'constraint311-%d'%(constraint_no))
			constdict['constraint311-%d'%(constraint_no)] = Or(OrList)==functions["epsWitness"](i,vars[n])
			constraint_no += 1

	######################################################

	# FIRST SET CONSTRAINTS

	######################################################

	# Definition constraint: no nonterm in first sets
	for nt in terms+nonterms+["eps"]:
		for n in nonterms:
			s.assert_and_track(Not(functions["first"](vars[nt],vars[n])),'%s notInFirstSetOf %s'%(nt,n))
			constdict['%s notInFirstSetOf %s'%(nt,n)] = Not(functions["first"](vars[nt],vars[n]))

	# Definition constraint: functions["first"](eps) = {eps}
	for t in terms:
		s.assert_and_track(Not(functions["first"](vars["eps"],vars[t])), 'constraint330-%d'%(constraint_no))
		constdict['constraint330-%d'%(constraint_no)] = Or(OrList)==functions["epsWitness"](i,vars[n])
		constraint_no += 1
	s.assert_and_track(functions["first"](vars["eps"],vars["eps"]), 'constraint332-%d'%(constraint_no))
	constdict['constraint332-%d'%(constraint_no)] = functions["first"](vars["eps"],vars["eps"])
	constraint_no += 1
	

	# Definition constraint: functions["first"](term) = {term}
	for nt in terms:
		for t in terms+["eps"]:
			if nt == t:
				s.assert_and_track(functions["first"](vars[nt],vars[t]), 'constraint342-%d'%(constraint_no))
				constdict['constraint342-%d'%(constraint_no)] = functions["first"](vars[nt],vars[t])
				constraint_no += 1
			else:
				s.assert_and_track(Not(functions["first"](vars[nt],vars[t])), 'constraint345-%d'%(constraint_no))
				constdict['constraint345-%d'%(constraint_no)] = Not(functions["first"](vars[nt],vars[t]))
				constraint_no += 1


	######################################################

	# FIRST SET CONSTRUCTION

	######################################################

	for n in nonterms:
		for t in terms:
			var = "%(nonterm)s%(term)s"%{"nonterm":n, "term":t}
			
			vars["i_%s"%var] = Int("i_%s"%var)
			vars["j_%s"%var] = Int("j_%s"%var)
			s.assert_and_track(functions["get_i"](vars[n],vars[t])==vars["i_%s%s"%(n,t)], 'constraint328-%d'%(constraint_no))
			constdict['constraint328-%d'%(constraint_no)] = functions["get_i"](vars[n],vars[t])==vars["i_%s%s"%(n,t)]
			constraint_no += 1
			s.assert_and_track(functions["get_j"](vars[n],vars[t])==vars["j_%s%s"%(n,t)], 'constraint365-%d'%(constraint_no))
			constdict['constraint365-%d'%(constraint_no)] = functions["get_j"](vars[n],vars[t])==vars["j_%s%s"%(n,t)]
			constraint_no += 1

			tempList = []
			for i in range(1,num_rules+1):
				tempList.append(vars["i_%s"%var]==vars["rule%d"%(i)])
			s.assert_and_track(Or(tempList), 'constraint373-%d'%(constraint_no))
			constdict['constraint373-%d'%(constraint_no)] = Or(tempList)
			constraint_no += 1

			tempList = []
			for i in range(1,2*size_rules+1):
				tempList.append(vars["j_%s"%var]==vars["cond%d"%(i)])
			s.assert_and_track(Or(tempList), 'constraint379-%d'%(constraint_no))
			constdict['constraint379-%d'%(constraint_no)] = Or(tempList)
			constraint_no += 1

			
			for i in range(1,num_rules+1):
				s.assert_and_track(Implies(And(functions["first"](vars[n],vars[t]),vars["i_%s"%var]==vars["rule%d"%(i)]),vars[n]==functions["symbolInLHS"](i)), 'constraint385-%d'%(constraint_no))
				constdict['constraint385-%d'%(constraint_no)] = Implies(And(functions["first"](vars[n],vars[t]),vars["i_%s"%var]==vars["rule%d"%(i)]),vars[n]==functions["symbolInLHS"](i))
				constraint_no += 1

			s.assert_and_track(Implies(functions["first"](vars[n],vars[t]),( functions["firstWitness"](vars[n],vars[t],vars["i_%s"%var],vars["j_%s"%var]) != -1)), 'constraint389-%d'%(constraint_no))
			constdict['constraint389-%d'%(constraint_no)] = Implies(functions["first"](vars[n],vars[t]),( functions["firstWitness"](vars[n],vars[t],vars["i_%s"%var],vars["j_%s"%var]) != -1))
			constraint_no += 1

			tempList = []
			for i in range(1,num_rules+1):
				for j in range(1,2*size_rules+1):
					tempList.append( (functions["firstWitness"](vars[n],vars[t],vars["rule%d"%i],vars["cond%d"%j])) == -1)

			s.assert_and_track(Implies(Not(functions["first"](vars[n],vars[t])),And(tempList)), 'constraint398-%d'%(constraint_no))
			constdict['constraint398-%d'%(constraint_no)] = Implies(Not(functions["first"](vars[n],vars[t])),And(tempList))
			constraint_no += 1

		s.assert_and_track(functions["first"](vars[n],vars["eps"])==functions["epsWitness"](num_rules,vars[n]), 'epsInFirstSet%s'%(n))
		constdict['epsInFirstSet%s'%(n)] = functions["first"](vars[n],vars["eps"])==functions["epsWitness"](num_rules,vars[n])

	######################################################

	# FOLLOW SET WITNESS CONSTRAINTS

	######################################################

	vars.update({"dol": Int('dol')})
	s.assert_and_track(vars["dol"]==symbol_counter, 'constraint412-%d'%(constraint_no))
	constdict['constraint412-%d'%(constraint_no)] = vars["dol"]==symbol_counter
	constraint_no + 1

	while (num_conds <= (size_rules*(size_rules+1))/2):
		vars.update({"cond%d"%num_conds: Int('cond%d'%num_conds)})
		num_conds+=1
	
	# Definition constraint: followWitness must either return -1 or return nonterm or term
	for n in nonterms:
		for t in terms+["dol"]:
			for r in (1,num_rules+1):
				for c in range(1,(size_rules*(size_rules+1))/2):
					s.assert_and_track(And(functions["followWitness"](vars[n],vars[t],r,c) >= -1, functions["followWitness"](vars[n],vars[t],r,c) < vars['eps'] ), 'constraint425-%d'%(constraint_no) )
					constdict['constraint425-%d'%(constraint_no)] = And(functions["followWitness"](vars[n],vars[t],r,c) >= -1, functions["followWitness"](vars[n],vars[t],r,c) < vars['eps'] ) 
					constraint_no +=1

	# Definition constraint: forall terms and dol t, functions["followWitness"](t,t,m_tt,n_tt) = t
	for t in terms+["dol"]:
		var = "%s%s"%(str(vars[t]),str(vars[t]))
		vars["m_%s"%var] = Int('m_%s'%var)
		vars["n_%s"%var] = Int('n_%s'%var)
		s.assert_and_track(functions["followWitness"](vars[t],vars[t],vars["m_%s"%var],vars["n_%s"%var])==vars[t], 'constraint434-%d'%(constraint_no))
		constdict['constraint434-%d'%(constraint_no)] = functions["followWitness"](vars[t],vars[t],vars["m_%s"%var],vars["n_%s"%var])==vars[t]
		constraint_no += 1
		s.assert_and_track(functions["get_m"](vars[t],vars[t])==vars["m_%s"%var], 'constraint437-%d'%(constraint_no))
		constdict['constraint437-%d'%(constraint_no)] = functions["get_m"](vars[t],vars[t])==vars["m_%s"%var]
		constraint_no += 1
		s.assert_and_track(functions["get_n"](vars[t],vars[t])==vars["n_%s"%var], 'constraint440-%d'%(constraint_no))
		constdict['constraint440-%d'%(constraint_no)] = functions["get_m"](vars[t],vars[t])==vars["m_%s"%var]
		constraint_no += 1

	# Definition constraint: followWitness must return -1 for -1 as nonterm arg
	for t in terms+["dol"]:
		for r in (1,num_rules+1):
			for c in range(1,(size_rules*(size_rules+1))/2):
				s.assert_and_track(functions["followWitness"](-1,vars[t],r,c) == -1 , 'constraint448-%d'%(constraint_no))
				constdict['constraint448-%d'%(constraint_no)] = functions["followWitness"](-1,vars[t],r,c) == -1 
				constraint_no += 1

	# Definition constraint: dol has been witnessed to be in functions["follow"](N1)
	# NOTE: N1 is the starting nonterm
	vars["m_N1dol"] = Int('m_N1dol')
	vars["n_N1dol"] = Int('n_N1dol')
	s.assert_and_track(functions["get_m"](vars["N1"],vars["dol"])==vars["m_N1dol"], 'constraint456-%d'%(constraint_no))
	constdict['constraint456-%d'%(constraint_no)] = functions["get_m"](vars["N1"],vars["dol"])==vars["m_N1dol"]
	constraint_no += 1
	
	s.assert_and_track(functions["get_n"](vars["N1"],vars["dol"])==vars["n_N1dol"], 'constraint460-%d'%(constraint_no))
	constdict['constraint460-%d'%(constraint_no)] = functions["get_n"](vars["N1"],vars["dol"])==vars["n_N1dol"]
	constraint_no += 1

	s.assert_and_track(functions["followWitness"](vars["N1"],vars["dol"],vars["m_N1dol"],vars["n_N1dol"])==vars["dol"], 'constraint464-%d'%(constraint_no))
	constdict['constraint464-%d'%(constraint_no)] = functions["followWitness"](vars["N1"],vars["dol"],vars["m_N1dol"],vars["n_N1dol"])==vars["dol"]
	constraint_no += 1

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

					s.assert_and_track((functions["followWitness"](functions["symbolInRHS"](r,i),vars[t],vars["rule%d"%(r)],vars["cond%d"%condNo])==vars[t])==And(tempList), 'followWitnesseps%d,%d,%d,%s'%(r,i,j,t))
					constdict['followWitnesseps%d,%d,%d,%s'%(r,i,j,t)] = (functions["followWitness"](functions["symbolInRHS"](r,i),vars[t],vars["rule%d"%(r)],vars["cond%d"%condNo])==vars[t])==And(tempList)

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

				s.assert_and_track((functions["followWitness"](functions["symbolInRHS"](r,i),vars[t],vars["rule%d"%(r)],vars["cond%d"%condNo])==functions["symbolInLHS"](r))==And(tempList), 'followWiitnessepsEnd%d,%d,%s'%(r,i,t))
				constdict['followWiitnessepsEnd%d,%d,%s'%(r,i,t)] = (functions["followWitness"](functions["symbolInRHS"](r,i),vars[t],vars["rule%d"%(r)],vars["cond%d"%condNo])==functions["symbolInLHS"](r))==And(tempList)
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
			s.assert_and_track(Not(functions["follow"](vars[n],vars[nt])), '%sInFollowSetOf%s'%(n,nt))
			constdict['%sInFollowSetOf%s'%(n,nt)] = Not(functions["follow"](vars[n],vars[nt]))

	# Definition constraint: dol is in functions["follow"](N1)
	# NOTE: N1 is the starting nonterm
	s.assert_and_track(functions["follow"](vars["N1"],vars["dol"]), 'constraint558-%d'%(constraint_no))
	constdict['constraint558-%d'%(constraint_no)] = functions["follow"](vars["N1"],vars["dol"])
	constraint_no += 1

	######################################################

	# FOLLOW SET CONSTRUCTION

	######################################################

	for n in nonterms:
		for t in terms:
			var = "%(nonterm)s%(term)s"%{"nonterm":n, "term":t}
			vars["m_%s"%var] = Int("m_%s"%var)
			vars["n_%s"%var] = Int("n_%s"%var)
			s.assert_and_track(functions["get_m"](vars[n],vars[t])==vars["m_%s"%(var)], 'constraint573-%d'%(constraint_no))
			constdict['constraint573-%d'%(constraint_no)] = functions["get_m"](vars[n],vars[t])==vars["m_%s"%(var)]
			constraint_no += 1
			s.assert_and_track(functions["get_n"](vars[n],vars[t])==vars["n_%s"%(var)], 'constraint576-%d'%(constraint_no))
			constdict['constraint576-%d'%(constraint_no)] = functions["get_n"](vars[n],vars[t])==vars["n_%s"%(var)]
			constraint_no += 1

			tempList = []
			for i in range(1,num_rules+1):
				tempList.append(vars["m_%s"%var]==vars["rule%d"%(i)])
			s.assert_and_track(Or(tempList), 'constraint583-%d'%(constraint_no))
			constdict['constraint583-%d'%(constraint_no)] = Or(tempList)
			constraint_no += 1

			tempList = []
			for i in range(1,followCondEnd):
				tempList.append(vars["n_%s"%var]==vars["cond%d"%i])
			s.assert_and_track(Or(tempList), 'constraint589-%d'%(constraint_no))
			constdict['constraint589-%d'%(constraint_no)] = Or(tempList)
			constraint_no += 1

			for r in range(1,num_rules+1):
				condNo = 1
				for i in range(1,size_rules):
					for j in range(j+1,size_rules+1):
						s.assert_and_track(Implies(And(functions["follow"](vars[n],vars[t]),vars["m_%s"%var]==vars["rule%d"%(r)],vars["n_%s"%var]==vars["cond%d"%(condNo)]),vars[n]==functions["symbolInRHS"](r,i)), 'constraint598-%d'%(constraint_no))
						constdict['constraint598-%d'%(constraint_no)] = Implies(And(functions["follow"](vars[n],vars[t]),vars["m_%s"%var]==vars["rule%d"%(r)],vars["n_%s"%var]==vars["cond%d"%(condNo)]),vars[n]==functions["symbolInRHS"](r,i))
						constraint_no += 1
						condNo += 1

				for i in range(1,size_rules+1):
					s.assert_and_track(Implies(And(functions["follow"](vars[n],vars[t]),vars["m_%s"%var]==vars["rule%d"%(r)],vars["n_%s"%var]==vars["cond%d"%(condNo)]),vars[n]==functions["symbolInRHS"](r,i)), 'constraint604-%d'%(constraint_no))
					constdict['constraaint604-%d'%(constraint_no)] = Implies(And(functions["follow"](vars[n],vars[t]),vars["m_%s"%var]==vars["rule%d"%(r)],vars["n_%s"%var]==vars["cond%d"%(condNo)]),vars[n]==functions["symbolInRHS"](r,i))
					constraint_no += 1
					condNo += 1

			s.assert_and_track(Implies(functions["follow"](vars[n],vars[t]),functions["followWitness"](vars[n],vars[t],vars["m_%s"%var],vars["n_%s"%var])!=-1), 'constraint609-%d'%(constraint_no))
			constdict['constraint609-%d'%(constraint_no)] = Implies(functions["follow"](vars[n],vars[t]),functions["followWitness"](vars[n],vars[t],vars["m_%s"%var],vars["n_%s"%var])!=-1)
			constraint_no += 1

			tempList = []
			for i in range(1,num_rules+1):
				for j in range(1,followCondEnd):
					tempList.append(functions["followWitness"](vars[n],vars[t],vars["rule%d"%i],vars["cond%d"%j])==-1)
			s.assert_and_track(Implies(Not(functions["follow"](vars[n],vars[t])),And(tempList)), 'constraint617-%d'%(constraint_no))
			constdict['constraint617-%d'%(constraint_no)] = Implies(Not(functions["follow"](vars[n],vars[t])),And(tempList))
			constraint_no += 1

		t = "dol"
		if n != "N1":
			var = "%(nonterm)s%(dol)s"%{"nonterm":n,"dol":t}
			vars["m_%s"%var] = Int("m_%s"%var)
			vars["n_%s"%var] = Int("n_%s"%var)
			s.assert_and_track(functions["get_m"](vars[n],vars[t])==vars["m_%s"%(var)], 'constraint626-%d'%(constraint_no))
			constdict['constraint626-%d'%(constraint_no)] = functions["get_m"](vars[n],vars[t])==vars["m_%s"%(var)]
			constraint_no +=1
			s.assert_and_track(functions["get_n"](vars[n],vars[t])==vars["n_%s"%(var)], 'constraint629-%d'%(constraint_no))
			constdict['constraint629-%d'%(constraint_no)] = functions["get_n"](vars[n],vars[t])==vars["n_%s"%(var)]
			constraint_no += 1


			tempList = []
			for r in range(1,num_rules+1):
				tempList.append(vars["m_%s"%var]==vars["rule%d"%(r)])
			s.assert_and_track(Or(tempList), 'constraint637-%d'%(constraint_no))
			constdict['constraint637-%d'%(constraint_no)] = Or(tempList)
			constraint_no +=1

			tempList = []
			for i in range(followCondMid,followCondEnd):
				tempList.append(vars["n_%s"%var]==vars["cond%d"%i])
			s.assert_and_track(Or(tempList), 'constraint644-%d'%(constraint_no))
			constdict['constraint644-%d'%(constraint_no)] = Or(tempList)
			constraint_no += 1

			for r in range(1,num_rules+1):
				condNo = followCondMid
				for i in range(1,size_rules+1):
					s.assert_and_track(Implies(And(functions["follow"](vars[n],vars[t]),vars["m_%s"%var]==vars["rule%d"%(r)],vars["n_%s"%var]==vars["cond%d"%(condNo)]),vars[n]==functions["symbolInRHS"](r,i)), 'constraint651-%d'%(constraint_no))
					constdict['constraint651-%d'%(constraint_no)] = Implies(And(functions["follow"](vars[n],vars[t]),vars["m_%s"%var]==vars["rule%d"%(r)],vars["n_%s"%var]==vars["cond%d"%(condNo)]),vars[n]==functions["symbolInRHS"](r,i))
					constraint_no += 1

					condNo += 1

			s.assert_and_track(Implies(functions["follow"](vars[n],vars[t]),functions["followWitness"](vars[n],vars[t],vars["m_%s"%var],vars["n_%s"%var])!=-1), 'constraint657-%d'%(constraint_no))
			constdict['constraint657-%d'%(constraint_no)] = Implies(functions["follow"](vars[n],vars[t]),functions["followWitness"](vars[n],vars[t],vars["m_%s"%var],vars["n_%s"%var])!=-1)
			constraint_no += 1

			tempList = []
			for i in range(1,num_rules+1):
				for j in range(followCondMid,followCondEnd):
					tempList.append(functions["followWitness"](vars[n],vars[t],vars["rule%d"%i],vars["cond%d"%j])==-1)
			s.assert_and_track(Implies(Not(functions["follow"](vars[n],vars[t])),And(tempList)), 'constraint665-%d'%(constraint_no))
			constdict['constraint666'%(constraint_no)] = Implies(Not(functions["follow"](vars[n],vars[t])),And(tempList))
			constraint_no += 1

	######################################################

	# PARSE TABLE CONSTRAINTS

	######################################################

	for n in nonterms:
		for t in terms+['dol']:
			s.assert_and_track(And(functions["parseTable"](vars[n],vars[t])<=num_rules,functions["parseTable"](vars[n],vars[t])>=0), 'constraint677-%d'%(constraint_no))
			constdict['constraint677-%d'%(constraint_no)] = And(functions["parseTable"](vars[n],vars[t])<=num_rules,functions["parseTable"](vars[n],vars[t])>=0)
			constraint_no += 1

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

				s.assert_and_track((functions["parseTable"](vars[n],vars[t])==vars["rule%d"%r])==And(functions["symbolInLHS"](r)==vars[n],Or(tempAnd)), 'parseTable%s,%s,%d'%(n,t,r))
				constdict['parseTable%s,%s,%d'%(n,t,r)] = (functions["parseTable"](vars[n],vars[t])==vars["rule%d"%r])==And(functions["symbolInLHS"](r)==vars[n],Or(tempAnd))
		
		for r in range(1,num_rules+1):
			tempList = []
			for i in range(1,size_rules+1):
				tempList.append(functions["first"](functions["symbolInRHS"](r,i),vars["eps"]))
			tempList.append(functions["follow"](functions["symbolInLHS"](r),vars["dol"]))

			s.assert_and_track((functions["parseTable"](vars[n],vars["dol"])==vars["rule%d"%r])==And(functions["symbolInLHS"](r)==vars[n],And(tempList)), 'constraint713-%d'%(constraint_no))
			constdict['constraint713-%d'%(constraint_no)] = (functions["parseTable"](vars[n],vars["dol"])==vars["rule%d"%r])==And(functions["symbolInLHS"](r)==vars[n],And(tempList))
			constraint_no += 1

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
	global constraint_no
	constdict = solver['dictconst']
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
	s.assert_and_track(Implies(And(functions["end"](strNum,1) == (i-1), functions["step"](strNum,i-1)), If(functions["ip_str"](strNum,functions["lookAheadIndex"](strNum,i)) == vars["dol"], And(Not(functions["step"](strNum,i)),functions["success"](strNum,i)), And(Not(functions["step"](strNum,i)),Not(functions["success"](strNum,i))) ) ), 'constraint779-%d'%(constraint_no))
	constdict['constraint779-%d'%(constraint_no)] = Implies(And(functions["end"](strNum,1) == (i-1), functions["step"](strNum,i-1)), If(functions["ip_str"](strNum,functions["lookAheadIndex"](strNum,i)) == vars["dol"], And(Not(functions["step"](strNum,i)),functions["success"](strNum,i)), And(Not(functions["step"](strNum,i)),Not(functions["success"](strNum,i))) ) )
	constraint_no += 1
	
	#Propagate success state on end of parse
	s.assert_and_track(Implies(Not(functions["step"](strNum,i)),And(Not(functions["step"](strNum,i+1)),functions["success"](strNum,i+1)==functions["success"](strNum,i))), 'constraint784-%d'%(constraint_no))
	constdict['constraint784-%d'%(constraint_no)] = Implies(Not(functions["step"](strNum,i)),And(Not(functions["step"](strNum,i+1)),functions["success"](strNum,i+1)==functions["success"](strNum,i)))
	constraint_no += 1

	# For consuming term
	AndList=[]
	AndList.append(functions["lookAheadIndex"](strNum,i+1) == functions["lookAheadIndex"](strNum,i) + 1)
	AndList.append(functions["step"](strNum,i))
	AndList.append(Not(functions["success"](strNum,i)))
	AndList.append(functions["end"](strNum,i)==i)
	OrList = []
	for t in terms:
		OrList.append(functions["symbolAt"](strNum,i)==vars[t])
	s.assert_and_track(Implies(And(Or(OrList),functions["step"](strNum,i-1)), If(functions["symbolAt"](strNum,i)==functions["ip_str"](strNum,functions["lookAheadIndex"](strNum,i)), And(AndList), And(Not(functions["step"](strNum,i)), Not(functions["success"](strNum,i))) ) ), 'constraint797-%d'%(constraint_no))
	constdict['constraint797-%d'%(constraint_no)] =  Implies(And(Or(OrList),functions["step"](strNum,i-1)), If(functions["symbolAt"](strNum,i)==functions["ip_str"](strNum,functions["lookAheadIndex"](strNum,i)), And(AndList), And(Not(functions["step"](strNum,i)), Not(functions["success"](strNum,i))) ) )
	constraint_no += 1

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
		s.assert_and_track(Implies(And(Or(OrList),functions["step"](strNum,i-1)),If(functions["parseTable"](functions["symbolAt"](strNum,i),functions["ip_str"](strNum,functions["lookAheadIndex"](strNum,i))) != 0, Implies(And(RHSList),And(AndList)), And(Not(functions["step"](strNum,i)),Not(functions["success"](strNum,i)) ) )), 'constraint831-%d'%(constraint_no))
		constdict['constraint831-%d'%(constraint_no)] = Implies(And(Or(OrList),functions["step"](strNum,i-1)),If(functions["parseTable"](functions["symbolAt"](strNum,i),functions["ip_str"](strNum,functions["lookAheadIndex"](strNum,i))) != 0, Implies(And(RHSList),And(AndList)), And(Not(functions["step"](strNum,i)),Not(functions["success"](strNum,i)) ) ))
		constraint_no += 1
