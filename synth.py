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
	
	add_accept_string(SP,accept_list[int(sys.argv[1])])
	
	# print "starting maxsat solver..."
	# result, doubt_pos,m = naive_maxsat(SP)
	f3 = open("SMTconstraints.smt","w+")
	f3.write(dumpSMT(SP["constraints"]))
	f3.close()
	# p, unsat_soft_constrains, m = naive_maxsat(SP)
	# print SP["constraints"].check()
	# SP["accept_list"] = accept_list
	# # print "atmost %d positions in the string are correct"%result
	# SP["model"] = m
	# for t in SP["terms"]:
	# 	print "%s %s"%(t,str(m.evaluate(SP["vars"][t])))

	# for i in range(SP["num_soft_constraints"]):
	# 	if int(str(m.evaluate(SP["aux_const"][i]))) == 1:
	# 		print "%d "%i,
	
	# print "lookAheadIndex ",m[SP["functions"]["lookAheadIndex"]]
	# print "symbolAt ",m[SP["functions"]["symbolAt"]]
	# print "end ",m[SP["functions"]["end"]]
	
	# tmp = print_grammar(SP)
	end_time = calendar.timegm(time.gmtime())
	print "\nSolving time taken: %s"%str(datetime.timedelta(seconds=(end_time-start_time)))
	# results = open("results_file_rebuttal.csv","a+")
	# a,r,c = specs()
	# parser.parser_main(tmp, len(tmp))
	#print "a[0] ",a[0]
	# results.write("%d,%d,%s,%d,%d\n"%(len(find_original_grammar()), len(a[0].split()), str(datetime.timedelta(seconds=(end_time-start_time))), parser.parser_main(tmp),c["size_rules"]))
	# results.close()	

main()
