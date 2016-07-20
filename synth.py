
from z3 import *
from init import *
from helpers import *
from solver import *
from test import *
from msat import *
from collections import OrderedDict
import calendar
import time
import datetime
from itertools import *

#SP instance
	# category = OrderedDict([('first_set_first_Subset',0), ('first_set_eps_subset',0) ,('eps_first_set_rule',0),('next_first_in_follow',0),('$_in_follow_N1',0),('follow_lhs_in_rhs',0),('parse_table_first',0),('parse_table_follow',0)])
	

def main():
	sp_time = calendar.timegm(time.gmtime())
	print "Initialising SP..."
	SP = {}
	SP["n_insertions"] = int(input("Enter the maximum number of insertions: (Time needed depends on this):"))
	SP["total_var"] = 1000
	SP["dictconst"] = {}
	initialize_solver(SP)
	# SP["constraints"].set(unsat_core=True)

	num = nums()
	original_grammar = find_original_grammar()
	repair(SP, original_grammar, num['num_rules'], num['size_rules'])

	print "SP initialized in %s"%str(datetime.timedelta(seconds=(calendar.timegm(time.gmtime())-sp_time)))
	start_time = calendar.timegm(time.gmtime())
	for accept_string in accept_list:
		add_accept_string(SP,accept_string)
	print "starting maxsat solver..."
	result, doubt_pos,m = naive_maxsat(SP)
	SP["accept_list"] = accept_list
	print "atmost %d positions in the string are correct"%result
	SP["model"] = m
	for t in SP["terms"]:
		print "%s %s"%(t,str(m.evaluate(SP["vars"][t])))
	# print "ip_str(1,0) ",str(m.evaluate(SP["functions"]["ip_str"](1,0)))

	# print "lookAheadIndex ",m[SP["functions"]["lookAheadIndex"]]
	# print "ip_str1 ",m[SP["functions"]["ip_str1"]]
	print "succ ",m[SP["functions"]["succ"]]
	print "pred ",m[SP["functions"]["pred"]]
	print SP["term_start"]
	print SP["term_end"]
	print_grammar(SP)
	end_time = calendar.timegm(time.gmtime())
	print "Solving time taken: %s"%str(datetime.timedelta(seconds=(end_time-start_time)))

def main1():

	sp_time = calendar.timegm(time.gmtime())
	
	print "Initializing SP..."

	SP = {}
	SP["total_var"] = 1000
	SP['dictconst'] = {}
	initialize_solver(SP)
	SP['constraints'].set(unsat_core=True)

	num = nums()
	original_grammar = find_original_grammar()
	repair(SP, original_grammar, num['num_rules'], num['size_rules'])

	print "SP initialized in %s"%str(datetime.timedelta(seconds=(calendar.timegm(time.gmtime())-sp_time)))

	#SN instance
	if config['neg_egs']:
		sn_time = calendar.timegm(time.gmtime())
		print "Initializing SN..."
		SN = {}
		SN['dictconst'] = {}
		initialize_solver(SN)
		add_reject_strings(SN)
		print "SN initialized in %s"%str(datetime.timedelta(seconds=(calendar.timegm(time.gmtime())-sn_time)))

	check_result = sat
	iterationNo = 1

	start_time = calendar.timegm(time.gmtime())

	# if config['optimize']:
	#	accept_list.sort(key = len, reverse=True)
	# 	print accept_list
	# accept_list = list_from_strings(accept_strings, SP)
	SP["accept_list"] = list_from_strings2(accept_strings)
	# mk_incremental_function(SP)

	while check_result != unsat:

		print "Iteration %d:"%iterationNo
		print "Solving SP"

		if config['optimize']:
			check_result = get_solution_optimize(SP)
		else:
			for accept_string in accept_list:
				add_accept_string(SP,accept_string)

			check_result = SP["constraints"].check()

		if check_result == unsat:
			print "this string is not parsable."
			tmp = SP['constraints'].unsat_core()
			SP['unsat'] = tmp
			print 'unsat_core',tmp
			A = []
			B = []
			C = []
			# for constraint in tmp:
			# 	constraint = str(constraint)
			# 	C.append(SP["dictconst"][constraint])

			# 	if 'input' in constraint:
			# 		B.append(SP["dictconst"][constraint])
			# 	else:
			# 		A.append(SP['dictconst'][constraint])
			# print binary_interpolant(And(B),And(A))
			# print sequence_interpolant(C)
			# print "proof: ",SP["constraints"].proof()
			#analyse_unsat(tmp, SP)
			print "No such grammar possible under present constraints"
			break

		SP["model"] = SP["constraints"].model()

		if config['neg_egs']:
			SN["constraints"].push()

			assert_grammar_hard(S_target=SN,S_source=SP,req=False)

			print "Solving SN"
			check_result = SN["constraints"].check()
			print check_result

			if check_result != unsat:
				SN["model"] = SN["constraints"].model()
				add_bad_grammar(S_target=SP,S_source=SN,iterationNo=iterationNo)
				SN["constraints"].pop()
			
			else:
				print("Grammar found!")
				correct = True
		else:
			check_result = unsat # negative examples are trivially satisfied
		
		print "STRING ACCEPTED"	
		print_grammar(SP)
		iterationNo += 1

	end_time = calendar.timegm(time.gmtime())
	print "Solving time taken: %s"%str(datetime.timedelta(seconds=(end_time-start_time)))

	print "specs:"
	print config
	print accept_list
	# print reject_list
	return SP


main()
correct = False	