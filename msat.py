from z3 import *
from init import *
import copy

def get_num_disabled_soft_constraints(m,num_soft_constraints,aux_const):
    # num_disabled = 0
    # for i in range(num_soft_constraints):
    #     if m.evaluate(aux_vars[i]) == True:
    #         num_disabled += 1
    # return num_disabled
    num_disabled = 0
    for i in range(len(aux_const)):
        num_disabled += int(str(m.evaluate(aux_const[i])))
    return num_disabled

def assert_soft(in_strings,solver):
    num_soft_constraints = 0
    s = solver["constraints"]
    vars = solver["vars"]
    terms = solver["terms"]
    in_terms = [in_strings[i].split(' ') for i in range(len(in_strings))]
    accept_list = []
    num_soft_constraints = 0
    
    aux = []
    aux_const = []
    for i in range(len(in_terms)):
        for j in range(len(in_terms[i])):
            aux.append(Bool('aux_%d_%d'%(i,j)))
            aux_const.append(Int('aux_const_%d_%d'%(i,j)))
            num_soft_constraints += 1
    idx = 0
    solver["num_soft_constraints"] = num_soft_constraints
    for j in range(len(in_terms)):
        tmp1 = []        
        for i in range(len(in_terms[j])):
            tmp1.append('a%d_%d'%(j,i))
            vars['a%d_%d'%(j,i)] = Int('a%d_%d'%(j,i))
        accept_list.append(tmp1)
        
        for i in range(len(in_terms[j])):
            if in_terms[j][i] not in tokens:
                print "this string is not accepted."
                global to_proceed
                to_proceed = False
                return
            OrList = []
            for t in terms:
                OrList.append(vars["a%d_%d"%(j,i)] == vars[t])
            s.add(Or(OrList))
            s.assert_and_track(Xor(vars['a%d_%d'%(j,i)] == vars["t%s"%(tokens.index(in_terms[j][i])+1)], aux[idx]), 'adding_terminal_at_%d_to_str_%d'%(i,j))
            idx += 1
    for i in range(len(aux)):
        s.add(If(aux[i], aux_const[i] == 1, aux_const[i] == 0))

    return accept_list,aux,aux_const

def assert_soft_constraints(solver, constraints):
    s = solver["constraints"]
    solver["num_soft_constraints"] = len(constraints)
    aux = []
    aux_const = []
    for i in range(len(constraints)):
        aux.append(Bool('aux_%d'%(solver["total_var"]+1)))
        aux_const.append(Int('aux_const_%d'%(solver["total_var"]+1)))
        solver["total_var"] += 1
    for i in range(len(constraints)):
        s.assert_and_track(Xor(constraints[i],aux[i]), 'soft_%d'%i)
        s.assert_and_track(If(aux[i], aux_const[i] == 1, aux_const[i] == 0), 'aux_const_%d'%(solver["total_var"]+1))
        solver["total_var"] += 1

    return aux,aux_const

def assert_at_most_k(solver, aux_const, k):
    tmp = 0
    for i in range(len(aux_const)):
        tmp += aux_const[i]
    # print "tmp: ",tmp
    solver["constraints"].add(tmp <= k)

def find_unsatisfied_soft_constraints(m,aux_const):
    tmp = []
    # print "aux_const inside function ",aux_const
    for i in range(len(aux_const)):
        if int(str(m.evaluate(aux_const[i]))) == 1:
            tmp.append(i)
    return tmp

def naive_maxsat(solver, accept_strings):
    # aux,aux_const = assert_soft_constraints(solver, accept_strings)
    aux = solver["aux"]
    aux_const = solver["aux_const"]
    # if is_sat == unsat:
    #     print "unsat_core ",solver["constraints"].unsat_core()
    #     return -1,[],-1
    r = 0
    k = solver["num_soft_constraints"] - 1
    
    while True:
        print "checking atmost %d constraints can be relaxed"%k      
        assert_at_most_k(solver, aux_const,k)
        is_sat = solver["constraints"].check()
        print "check_Sat: ",is_sat
        
        if is_sat == unsat:
            if k != solver["num_soft_constraints"] - k -1:
                unsatisfied_soft_constraints = find_unsatisfied_soft_constraints(m, aux_const)
            else:
                unsatisfied_soft_constraints = [i for i in range(solver["num_soft_constraints"])]
            return solver["num_soft_constraints"] - k - 1, unsatisfied_soft_constraints,m
        
        m = solver["constraints"].model()
        # print "model ",m
        # print "aux_const ",aux_const
        num_disabled = get_num_disabled_soft_constraints( m, solver["num_soft_constraints"], aux_const)
        k = num_disabled
        
        if k == 0:
            print "it was possible to satisfy all soft constraints"
            return solver["num_soft_constraints"],[],m
        k -= 1


# x = Int('x')
# SP = {}
# SP["constraints"] = Solver()
# SP["constraints"].set(unsat_core=True)
# SP["total_var"] = 1
# constraints = [x >= 0, x < 5,  x < 15]
# SP["num_soft_constraints"] = len(constraints)

# accept_strings = constraints
# # assert_soft_constraints(SP, constraints)
# SP["constraints"].assert_and_track(x < 0, 'hard')
# result,unsatisfied_soft_constraints = naive_maxsat(SP, accept_strings)
# print "only %d soft constraints can be satisfied"%result
# print "unsatisfied soft constraints are numbered ",unsatisfied_soft_constraints
# print SP["constraints"].assertions()+

# counter_bits_sz return
# def assert_at_most_k(solver, n, lits, k):
    # if k >= n or n <= 1:
    #     return
    # counter_bits_sz = None
    # counter_bits_sz,counter_bits = mk_counter_circuit(solver, n, lits, counter_bits_sz)
    # assert_le_k(solver, counter_bits_sz, counter_bits, k)


# def mk_full_adder(solver, in_1, in_2, cin, out, cout):
#     #out and cout are passed by value
#     cout = Or(And(in_1,in_2), And(in_1,cin), And(in_2,cin))
#     # solver["constraints"].assert_and_track(cout,'adding_cout%d'%(solver["total_var"]+1))
#     solver["total_var"] += 1
#     out = Xor(Xor(in_1,in_2),cin)
#     # solver["constraints"].assert_and_track(out, 'adding_out%d'%(solver["total_var"]+1))
#     solver["total_var"] += 1
#     return out,cout

# def mk_adder(solver, num_bits, in_1, in_2, result, tmpin, tmpout):
#     cin = Bool('var%d'%(solver["total_var"]+1))
#     solver["constraints"].add(cin == False)
#     for i in range(num_bits):
#         out,cout = mk_full_adder(solver,in_1[tmpin+i], in_2[tmpin + num_bits + i], cin, None,None)
#         result[tmpout+i] = out
#         cin = cout
#     result[tmpout+num_bits] = cout


# def mk_adder_pairs(solver, num_bits, num_ins, inp, out_num_ins, out):
#     # out_num_ins is passed by value
#     out_num_bits = num_bits + 1
#     i = 0
#     _in = inp
#     _out = out
#     if num_ins%2 == 0:
#         out_num_ins = num_ins/2
#     else:
#         out_num_ins = num_ins/2 + 1
#     tmpin, tmpout = 0,0
#     for i in range(num_ins/2):
#         mk_adder(solver, num_bits, _in, _in, _out, tmpin, tmpout)
#         tmpin += num_bits
#         tmpin += num_bits
#         tmpout += out_num_bits
#     if num_ins%2 != 0:
#         for i in range(num_bits):
#             _out[i] = _in[i]
        
#         _out[num_bits] = Bool('var%d'%(solver["total_var"]+1))
#         solver["total_var"] += 1
#         solver["constraints"].assert_and_track(Not(_out[num_bits]), 'adding out_num_bits%d'%(solver["total_var"]+1))
#         solver["total_var"] += 1
#     return out_num_ins

# def mk_counter_circuit(solver, n, lits, out_sz):
#     # out_sz is passed as value
#     num_ins = n
#     num_bits = 1
#     aux1 = []
#     aux2 = []
#     if n == 0:
#         return 0
#     # copy.deepcopy(aux1,lits)
#     for i in range(len(lits)):
#         aux1.append(lits[i])
#         aux2.append(None)
#     while num_ins > 1:
#         new_num_ins = None
#         new_num_ins = mk_adder_pairs(solver, num_bits, num_ins, aux1, new_num_ins, aux2)
#         num_ins = new_num_ins
#         num_bits += 1
#         tmp = aux1
#         aux1 = aux2
#         aux2 = tmp
#     out_sz = num_bits
#     return out_sz, aux1

# def get_bit(val, idx):
#     mask = 1 << (idx & 31)
#     return (val & mask) !=0


# def assert_le_k(solver, n, val, k):
#     not_val = Not(val[0])
#     solver["constraints"].assert_and_track(Not(val[0]), 'val[0]_%d'%(solver["total_var"]+1))
#     solver["total_var"] += 1
#     solver["total_var"] += 1
#     if get_bit(k,0):
#         out = Bool('var%d'%(solver["total_var"]+1))
#         solver["constraints"].assert_and_track((out), 'add_in_le_k_%d'%(solver["total_var"]+1))
#         solver["total_var"] += 1
#     out = not_val
#     for idx in range(1,n):
#         not_val = Not(val[idx])
#         solver["constraints"].assert_and_track(Not(val[idx]), 'Not(val[idx])%d'%(solver["total_var"]+1))
#         solver["total_var"] += 1
#         if get_bit(k,idx):
#             i1 = not_val
#             i2 = out
#         else:
#             i1 = Bool('var%d'%(solver["total_var"]+1))
#             solver["total_var"] += 1
#             solver["constraints"].assert_and_track(i1 == False, 'i1_%d'%(solver["total_var"]+1))
#             solver["total_var"] += 1
#             i2 = Bool('var%d'%(solver["total_var"]+1))
#             solver["total_var"] += 1
#             solver["constraints"].assert_and_track(i1 == False, 'i2_%d'%(solver["total_var"]+1))

#         out = Or(i1,i2,And(not_val,out))
#         solver["constraints"].assert_and_track(out, 'out_last%d'%(solver["total_var"]+1))
#         solver["total_var"] += 1
