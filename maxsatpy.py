from z3 import *

def mk_fresh_bool_var_array(num_vars,solver):
    result = []
    vars = solver["vars"]
    total_num_vars = solver["total_var"]
    for i in range(num_vars):
    	result.append(Bool('var%d'%(total_num_vars)))
    	# vars['var%d'%(total_num_vars)] = Bool('var%d'%(total_num_vars))
    	solver["total_var"] += 1
    return result


    # Z3_ast * result = (Z3_ast *) malloc(sizeof(Z3_ast) * num_vars);
    # unsigned i;
    # for (i = 0; i < num_vars; i++) {
    #     result[i] = mk_fresh_bool_var(ctx);
    # }
    # return result;

def assert_hard_constraints():
	pass

def assert_soft(in_strings,solver):
	num_soft_constraints = 0
	s = solver["constraints"]
	vars = solver["vars"]
	in_terms = [in_strings[i].split(' ') for i in range(len(in_strings))]
	accept_list = []

	num_strings = len(in_strings)
	aux = []
	for i in range(num_strings):
		tmp = []
		for j in range(len(in_strings[i])):
			tmp.append('aux_%d_%d'%(i,j))
			vars['aux_%d_%d'%(i,j)] = Bool('aux_%d_%d'%(i,j))
			num_soft_constraints += 1
		aux.append(tmp)
	
	solver["num_soft_constraints"] = num_soft_constraints
	for j in range(len(in_terms)):
		tmp = []
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
			s.assert_and_track(Xor(vars['a%d_%d'%(j,i)] == vars["t%s"%(tokens.index(in_terms[j][i])+1)], vars["aux_%d_%d"%(j,i)]), 'adding_terminal_at_%d_to_str_%d'%(i,j))

	
		# for i in in_terms[j]:
		# 	if i not in tokens:
		# 		print "This string is not accepted."
		# 		global to_proceed

		# 		to_proceed = False
		# 		print "to_proceed: ",to_proceed
		# 		return
		# 		# print "saket"
		# 	tmp.append("t%s"%(tokens.index(i)+1))
		# accept_list.append(tmp)
	
	return accept_list

def mk_full_adder(solver,in_1, in_2, cin):
	vars = solver["vars"]
	vars["cout"]
    cout = Or(ctx, And(in_1, in_2), And(in_1, cin), And(in_2, cin))
    out  = Xor(Xor(in_1, in_2), cin);
    return cout,out

def mk_adder(solver,num_bits, in_1, in_2,result): 

    # Z3_cin, cout, out;
    # unsigned i;
    # cin = Z3_mk_false(ctx);
    cin = Bool('var_%d'(solver["total_var"]+1))
    solver["constraints"].add(cin == False)
    # for (i = 0; i < num_bits; i++) {
    #     mk_full_adder(ctx, in_1[i], in_2[i], cin, &out, &cout);
    #     result[i] = out;
    #     cin = cout;
    # }
    # result[num_bits] = cout;

    for i in range(num_bits):
    	cout,out = mk_full_adder(in_1[i], in_2[i], cin)
    	result[i] = out
    	cin = cout
    result[num_bits] = cout

#return  out_num_ins
def mk_adder_pairs(solver,num_bits, num_ins, in, out_num_ins, out):
	out_num_bits = num_bits + 1
	i = 0
	_in = in
	_out = out
	if num_ins % 2 == 0:
		out_num_ins = num_ins/2
	else:
		out_num_ins = num_ins/2 + 1

	tmpin, tmpout = 0,0
	for i in range(num_ins/2):
		mk_adder(num_bits, _in[tmpin:], _in[tmpin + num_bits:],_out[tmpout:])
		tmpin += num_bits
		tmpin += num_bits
		tmpout += out_num_bits

	if num_ins/2 != 0:
		for i in range(num_bits):
			_out[i] = _in[i]
		_out[num_bits] = Bool('var%d'%(solver["total_var"]+1))
		solver["constraints"].add(_out[num_bits] == False)
	return out_num_ins





