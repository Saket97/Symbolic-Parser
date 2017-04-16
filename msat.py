from z3 import *
from init import *
import copy

def get_num_disabled_soft_constraints(m,num_soft_constraints,aux_const):

    num_disabled = 0
    for i in range(len(aux_const)):
        num_disabled += int(str(m.evaluate(aux_const[i])))
    return num_disabled

def add_soft(constraint, solver):
    # print "constraint: ",constraint
    if "aux" not in solver:
        solver["aux"] = []
        solver["aux_const"] = []
    aux = solver["aux"]
    aux_const = solver["aux_const"]
    tmp = Bool('aux%d'%(solver["total_var"]))
    tmp1 = Int('aux_const%d'%(solver["total_var"]))
    aux.append(tmp)
    aux_const.append(tmp1)
    solver["total_var"] += 1
    s = solver["constraints"]
    # s.add(Xor(constraint, aux[len(aux)-1]))
    s.add(Implies((Not(aux[len(aux)-1])), constraint))
    s.add(If(aux[len(aux)-1], aux_const[len(aux_const)-1] == 1, aux_const[len(aux_const)-1] == 0))  
    print "constraint:",constraint

def assert_at_most_k(solver, aux_const, k):
    solver["constraints"].add(Sum([aux_const[i] for i in range(len(aux_const))]) <= k)

def find_unsatisfied_soft_constraints(m,aux_const):
    tmp = []
    # print "aux_const inside function ",aux_const
    for i in range(len(aux_const)):
        if int(str(m.evaluate(aux_const[i]))) == 1:
            tmp.append(i)
    return tmp

def naive_maxsat(solver):
    # aux,aux_const = assert_soft_constraints(solver, accept_strings)
    if "aux" not in solver:
        solver["aux"] = []
        solver["aux_const"] = []
    aux = solver["aux"]
    aux_const = solver["aux_const"]
    # print "aux_const[0]: ",aux_const[0]
    r = 0
    solver["num_soft_constraints"] = len(aux)
    # print "num_soft_cconstraints: ",len(aux)
    k = solver["num_soft_constraints"] - 1
    print "%d soft constraints added..."%(k+1)
    # print "hard constraints: ",solver["constraints"].check()
    k = 1
    m = None
    while True:
        solver["constraints"].push()
        print "checking atmost %d constraints can be relaxed"%k      
        assert_at_most_k(solver, aux_const,k)
        solver["constraints"].push()
        is_sat = solver["constraints"].check()
        print solver["constraints"].statistics()
        print "check_Sat: ",is_sat
        # return
        if is_sat == sat or unknown:
            m = solver["constraints"].model()
            return solver["num_soft_constraints"],[],m
        else:
            k += 1
            solver["constraints"].pop()
            solver["constraints"].pop()
            if k >= 5:
                print "Unsat..."
                return [],[],[]
            continue
        if is_sat == unsat:
            if k != solver["num_soft_constraints"] - k -1:
                unsatisfied_soft_constraints = find_unsatisfied_soft_constraints(m, aux_const)
            else:
                unsatisfied_soft_constraints = [i for i in range(solver["num_soft_constraints"])]
            solver["constraints"].pop()
            assert_at_most_k(solver, aux_const, k+1)
            print "Last final check: ",solver["constraints"].check()
            return solver["num_soft_constraints"] - k - 1, unsatisfied_soft_constraints,m
        
        m = solver["constraints"].model()
        num_disabled = get_num_disabled_soft_constraints( m, solver["num_soft_constraints"], aux_const)
        k = num_disabled
        # k += 1
        print "k ",k
        print "saket"
        if k == 0:
            print "it was possible to satisfy all soft constraints"
            # print_grammar(solver)
            return solver["num_soft_constraints"],[],m
        k -= 1
        if (k >= 5):
            print "it was possible to satisfy all soft constraints"
            return solver["num_soft_constraints"],[],m
        solver["constraints"].pop()

