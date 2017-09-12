from z3 import *
from init import *
from helpers import *
from solver import *
from test import *
import sys
import calendar
import time
import datetime
from parser_verify import parser_main1
from msat import *
def dumpSMT(f):
	v = (Ast * 0)()
	a = f.assertions()
	f = And(*a)
	return Z3_benchmark_to_smtlib_string(f.ctx_ref(), "","", "","",0,v,f.as_ast())

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
	# print "original_grammar_synth: ", original_grammar
	repair(SP, original_grammar, num['num_rules'], num['size_rules'])


	start_time = calendar.timegm(time.gmtime())
        SP["A_string"],b,c = specs()
	ret_string = add_accept_string(SP,accept_list[int(sys.argv[1])])

	end_time = calendar.timegm(time.gmtime())
	pr_time = str(datetime.timedelta(seconds=(end_time-start_time)))
	print "\nSolving time taken: %s"%str(datetime.timedelta(seconds=(end_time-start_time)))
	# results = open("results_file_rebuttal.csv","a+")
	a,r,c = specs()
	# parser.parser_main(tmp, len(tmp))
	#print "a[0] ",a[0]
	# results.write("%d,%d,%s,%d,%d\n"%(len(find_original_grammar()), len(a[0].split()), str(datetime.timedelta(seconds=(end_time-start_time))), parser.parser_main(tmp),c["size_rules"]))
	# results.close()
	print "CORRECT STRING=",ret_string
	results = open("results_file_rebuttal.csv","a+")

	results.write("%d %d %s %d %s %d %d %d\n"%(int(sys.argv[2]), len(a[0].split()), pr_time, ret_string, SP["vtime"], SP["scorrect"], SP["compiler_returned_error_location"], SP["actual_error_location"]))
main()
