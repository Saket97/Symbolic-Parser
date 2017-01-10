
from z3 import *
from init import *
from helpers import *
from solver import *
from test import *
from views import *

import calendar
import time
import datetime

#SP instance
def main(ogrammar,table_parse=None, first_set=None, follow_set=None, parsetablegrammar=False,firstgrammar=False, parsetablefirst=False):
	sp_time = calendar.timegm(time.gmtime())
	print "Initializing SP..."
	SP = {}
	initialize_solver(SP)

	num = nums()
	original_grammar = ogrammar
	repair(SP, original_grammar, num['num_rules'], num['size_rules'], parsetablegrammar, firstgrammar, parsetablefirst, table_parse=table_parse, first_set=first_set, follow_set=follow_set)

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
			return [tmp,False]
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
				global correct
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
	return [None,True]

# main()
correct = False	