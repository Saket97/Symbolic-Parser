
from z3 import *
from init import *
from helpers import *
from solver import *
from test import *


import calendar
import time
import datetime

#SP instance
def main():
	sp_time = calendar.timegm(time.gmtime())
	print "Initializing SP..."
	SP = {}
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
		initialize_solver(SN)
		add_reject_strings(SN)
		print "SN initialized in %s"%str(datetime.timedelta(seconds=(calendar.timegm(time.gmtime())-sn_time)))

	check_result = sat
	iterationNo = 1

	start_time = calendar.timegm(time.gmtime())

	# if config['optimize']:
	#	accept_list.sort(key = len, reverse=True)
	# 	print accept_list

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
			tmp = SP['constraints'].unsat_core()
			SP['unsat'] = tmp
			print 'unsat_core',tmp
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
			
		print_grammar(SP)
		iterationNo += 1

	end_time = calendar.timegm(time.gmtime())
	print "Solving time taken: %s"%str(datetime.timedelta(seconds=(end_time-start_time)))

	print "specs:"
	print config
	print accept_list
	print reject_list
	return SP

main()
correct = False	