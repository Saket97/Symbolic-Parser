from z3 import *
from init import *
from helpers import *
from solver import *
from test import *
import sys
import calendar
import time
import datetime
import parser
from msat import *

#SP instance
def main1():
	sp_time = calendar.timegm(time.gmtime())
	print "Initializing SP..."
	SP = {}
	SP["dictconst"] = {}
	SP["comment_out"] = False
	initialize_solver(SP)
	print "SP initialized in %s"%str(datetime.timedelta(seconds=(calendar.timegm(time.gmtime())-sp_time)))
	num = nums()
	original_grammar = find_original_grammar()
	repair(SP, original_grammar, num['num_rules'], num['size_rules'])
	#SN instance
	if config['neg_egs']:
		sn_time = calendar.timegm(time.gmtime())
		print "Initializing SN..."
		SN = {}
		SN["comment_out"] = False
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
			print "No such grammar possible under present constraints"
			break

		SP["model"] = SP["constraints"].model()
		print "follow set ",SP["model"][SP["functions"]["follow"]]
		print "parse table ",SP["model"][SP["functions"]["parseTable"]]
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


def main():
	sp_time = calendar.timegm(time.gmtime())
	print "Initialising SP..."
	SP = {}
	SP["comment_out"] = True
	# SP["n_insertions"] = int(input("Enter the maximum number of insertions: (Time needed depends on this):"))
	SP["n_insertions"] = 2
	SP["total_var"] = 1000
	SP["dictconst"] = {}
	initialize_solver(SP)
	# SP["constraints"].set(unsat_core=True)
	print "SP initialized in %s"%str(datetime.timedelta(seconds=(calendar.timegm(time.gmtime())-sp_time)))
	
	num = nums()
	original_grammar = find_original_grammar()
	repair(SP, original_grammar, num['num_rules'], num['size_rules'])

	
	start_time = calendar.timegm(time.gmtime())
	# for accept_string in accept_list:
	# 	add_accept_string(SP,accept_string)
	add_accept_string(SP,accept_list[int(sys.argv[1])])
	
	print "starting maxsat solver..."
	# result, doubt_pos,m = naive_maxsat(SP)
	p, unsat_soft_constrains, m = naive_maxsat(SP)
	# print SP["constraints"].check()
	SP["accept_list"] = accept_list
	# print "atmost %d positions in the string are correct"%result
	SP["model"] = m
	for t in SP["terms"]:
		print "%s %s"%(t,str(m.evaluate(SP["vars"][t])))
	print "$ %s"%(str(m.evaluate(SP["vars"]['dol'])))
	# print "ip_str(1,0) ",str(m.evaluate(SP["functions"]["ip_str"](1,0)))
	for i in range(SP["num_soft_constraints"]):
		if int(str(m.evaluate(SP["aux_const"][i]))) == 1:
			print "%d "%i,
	# print "lookAheadIndex ",m[SP["functions"]["lookAheadIndex"]]
	# print "ip_str1 ",m[SP["functions"]["ip_str1"]]
	print "succ ",m[SP["functions"]["succ"]]
	print "pred ",m[SP["functions"]["pred"]]
	print "ip_str1 ",m[SP["functions"]["ip_str1"]]
	tmp = print_grammar(SP)
	end_time = calendar.timegm(time.gmtime())
	print "\nSolving time taken: %s"%str(datetime.timedelta(seconds=(end_time-start_time)))
	results = open("results_file1.csv","a+")
	a,r,c = specs()
	print "a[0] ",a[0]
	results.write("%d,%d,%s,%d,%d\n"%(len(find_original_grammar()), len(a[0].split(' ')), str(datetime.timedelta(seconds=(end_time-start_time))), parser.parser_main(tmp),c["size_rules"]))
	results.close()	

# if sys.argv[1] == 'mode1':
# 	main1()
# else:
# 	main()
main()