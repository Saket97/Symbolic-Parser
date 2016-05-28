from input_specs import *
from solver import *
from z3 import *
# from test import *
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

	num_rules = config['num_rules']
	num_nonterms = config['num_nonterms']
	num_terms = config['num_terms']
	size_rules = config['size_rules']

	rules = req_rules(solver)

	for i in range(num_rules):
		if rules[i]:
			# print "inner ",(m.evaluate(m_funs["symbolInLHS"](i+1)))
			symbolValue = int(str(m.evaluate(m_funs["symbolInLHS"](i+1))))
			# print "symbol value ",symbolValue
			print "N%d\t->\t"%(symbolValue+1),
			for j in range(size_rules):
				# print "inner ",(m.evaluate(m_funs["symbolInRHS"](i+1,j+1)))
				symbolValue = int(str(m.evaluate(m_funs["symbolInRHS"](i+1,j+1))))
				# print "symbol value ",symbolValue
				if symbolValue < num_nonterms:
					print "N%d\t"%(symbolValue+1),
				elif symbolValue < num_nonterms + num_terms:
					print "%s\t"%(tokens[symbolValue-num_nonterms]),
				elif symbolValue == num_nonterms + num_terms:
					print "eps\t",
			print ""
	print "follow: ",str(m.evaluate(m_funs["follow"](m_vars['N1'],m_vars['t2'])))
	print "eps: ",m.evaluate(m_vars['eps'])
	# print m.evaluate(m_vars['N1'])
	# tempList = []
	# for r in range(1,num_rules):
	# 	for c in range(1,size_rules*(size_rules+1)/2):
	# 		tempList.append()
	print "followWitness: ",int(str(m.evaluate(m_funs["followWitness"](m_vars['N1'],m_vars['t2'],m_funs["get_m"](m_vars['N1'],m_vars['t2']),m_funs["get_n"](m_vars['N1'],m_vars['t2'])))))
	print "followWitness: ",int(str(m.evaluate(m_funs["followWitness"](m_vars['N1'],m_vars['t2'],1,m_funs["get_n"](m_vars['N1'],m_vars['t2'])))))
	print "followWitness: ",int(str(m.evaluate(m_funs["followWitness"](m_vars['N1'],m_vars['t2'],2,m_funs["get_n"](m_vars['N1'],m_vars['t2'])))))
	print "followWitness: ",m.evaluate(m_funs["followWitness"](m_funs["symbolInLHS"](2),m_vars['t2'],m_funs["get_i"](m_funs["symbolInLHS"](2),m_vars['t2']),m_funs["get_j"](m_funs["symbolInLHS"](2),m_vars['t2'])))

def main():
	SP = {}
	initialize_solver(SP)
	original_grammar = find_original_grammar()
	# print "original_grammar:",original_grammar
	num = nums()
	print "calling repair function"
	repair(SP,original_grammar,num['num_rules'],num['size_rules'])
	check_sat = SP['constraints'].check()
	if check_sat == sat:
		print 'Correct Parse Table'
		SP['model'] = SP['constraints'].model()
		print_grammar(SP)
	else:
		u_core = SP['constraints'].unsat_core()
		print "unsat core ",u_core

	print 
main()