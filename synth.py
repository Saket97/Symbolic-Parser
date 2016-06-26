
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
def analyse_unsat(u_core, solver):
	category = OrderedDict([('first_set_first_Subset',0), ('first_set_eps_subset',0) ,('eps_first_set_rule',0),('next_first_in_follow',0),('$_in_follow_N1',0),('follow_lhs_in_rhs',0),('parse_table_first',0),('parse_table_follow',0)])
	for constraint in u_core:
		if 'first_set_first_Subset' in str(constraint):# A -> B C first B < First A
			category['first_set_first_Subset'] += 1
		else:
			if 'first_set_eps_subset' in str(constraint):# A -> B C first B has eps then first C < first A
				category['first_set_eps_subset'] += 1
			else:

				if 'eps_first_set_rule' in str(constraint): # A -> B C first B and C has eps then First A has eps
					category['eps_first_set_rule'] += 1
				else:
					if 'next_first_in_follow' in str(constraint): # A -> B C D if firs C has eps then first D in follow B
						category['next_first_in_follow'] += 1
					else:
						if '$_in_follow_N1' in str(constraint):
							category['$_in_follow_N1'] += 1
						else:
							if 'follow_lhs_in_rhs' in str(constraint):
								category['follow_lhs_in_rhs'] += 1
							else:
								if 'parse_table_first' in str(constraint):
									category['parse_table_first'] += 1
								else:
									if 'parse_table_follow' in str(constraint):
										category['parse_table_follow'] += 1

	for k,t in category.items():
		print k," : ",t


def main():
	print "PROBLEM WITH CODE: IT GIVES UNSAT IF THE NO STRING OF GIVEN LENGTH IS POSSIBLE i.e. NO EXACT POSITION IS RETURNED"
	print "If we want to insert then we can insert to right, check for left"
	sp_time = calendar.timegm(time.gmtime())
	print "Initialising SP..."
	SP = {}
	SP["total_var"] = 1000
	SP["dictconst"] = {}
	initialize_solver(SP)
	SP["constraints"].set(unsat_core=True)

	num = nums()
	original_grammar = find_original_grammar()
	repair(SP, original_grammar, num['num_rules'], num['size_rules'])

	print "SP initialized in %s"%str(datetime.timedelta(seconds=(calendar.timegm(time.gmtime())-sp_time)))
	start_time = calendar.timegm(time.gmtime())

	accept_list, aux, aux_const = assert_soft(accept_strings, SP)
	SP["aux"] = aux
	SP["aux_const"] = aux_const
	# result, doubt_pos = naive_maxsat(SP, accept_strings)

	for accept_string in accept_list:
		add_accept_string(SP,accept_string)

	result, doubt_pos,m = naive_maxsat(SP, accept_strings)

	print "atmost %d positions in the string are correct"%result
	print "doubtful positions ",doubt_pos
	for i in range(len(doubt_pos)):
		print "correction_proposed ",m.evaluate(SP["vars"][accept_list[0][i]])
	end_time = calendar.timegm(time.gmtime())
	print "Solving time taken: %s"%str(datetime.timedelta(seconds=(end_time-start_time)))

def main1():

	sp_time = calendar.timegm(time.gmtime())
	
	print "Initializing SP..."

	print "to-proceed in synth: ",to_proceed
	if  to_proceed == False:
		return
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
	accept_list = list_from_strings(accept_strings, SP)

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