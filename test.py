from input_specs7 import *
from init import *
from z3 import *

def add_constraints(solver, view_assign, original_grammar, num_rules, size_rules):
	s = solver['constraints']
	vars = solver['vars']
	i = 1
	size_rules = len(original_grammar[0])-1
	constdict = solver["dictconst"]
	for r in range(num_rules):
		s.assert_and_track(vars['x%d'%(r*(size_rules+1)+1)] == vars[view_assign[original_grammar[r][0]]], 'input x%d'%(r*(size_rules+1)+1))
		constdict['input x%d'%(r*(size_rules+1)+1)] = (vars['x%d'%(r*(size_rules+1)+1)] == vars[view_assign[original_grammar[r][0]]])
		print "constdictx1: ",solver["dictconst"]["input x1"]
		print('x%d %s %d'%((r*(size_rules+1)+1),view_assign[original_grammar[r][0]], i))
		i += 1
		
		for j in range(1,size_rules+1):
			
			if original_grammar[r][j] == 'eps':
				# pass
				# # if (r*(size_rules+1)+j+1) == 5:
				# # 	s.assert_and_track(vars['x%d'%(r*(size_rules+1)+j+1)] == vars['eps'], '%d'%(r*(size_rules+1)+j+1))
				# # 	i += 1	
				# # 	continue
				s.assert_and_track(vars['x%d'%(r*(size_rules+1)+j+1)] == vars['eps'], 'input x%d'%(r*(size_rules+1)+j+1))
				constdict['input x%d'%(r*(size_rules+1)+j+1)] = vars['x%d'%(r*(size_rules+1)+j+1)] == vars['eps']
				print('x%d  eps %d'%(r*(size_rules+1)+j+1, i))
				i += 1
			else:
				if (r*(size_rules+1)+j+1) == 13:
					continue
				s.assert_and_track(vars['x%d'%(r*(size_rules+1)+j+1)] == vars[view_assign[original_grammar[r][j]]], 'input x%d'%(r*(size_rules+1)+j+1))
				constdict['input x%d'%(r*(size_rules+1)+j+1)] = vars['x%d'%(r*(size_rules+1)+j+1)] == vars[view_assign[original_grammar[r][j]]]
				
				print('x%d %s %d'%((r*(size_rules+1)+j+1),view_assign[original_grammar[r][j]], i))
				i += 1

def add_parse_table_constraints(solver,parse_table,view_assign):
	s = solver["constraints"]
	vars = solver['vars']
	functions = solver['functions']
	constdict = solver["dictconst"]
	print "parse_table: ",parse_table
	for i in range(len(parse_table)):
		non_terminal = parse_table[i]['non_term']
		for k,t in parse_table[i].items():
			if k == 'non_term':
				continue
			if t:	
				s.assert_and_track(functions['parseTable'](vars[view_assign[non_terminal]],vars[view_assign[k]]) == vars['rule%d'%(t)],'%s %s parse table input'%(non_terminal,k))
				constdict['%s %s parse table input'%(non_terminal,k)] = functions['parseTable'](vars[view_assign[non_terminal]],vars[view_assign[k]]) == vars['rule%d'%(t)]
			else:
				s.assert_and_track(functions['parseTable'](vars[view_assign[non_terminal]],vars[view_assign[k]]) == 0,'%s %s parse table input'%(non_terminal,k))
				constdict['%s %s parse table input'%(non_terminal,k)] = functions['parseTable'](vars[view_assign[non_terminal]],vars[view_assign[k]]) == 0

def add_first_set_constraints(solver, first_set, follow_set, view_assign):
	s = solver["constraints"]
	vars = solver["vars"]
	functions = solver["functions"]
	constdict = solver["dictconst"]
	print "first set:",first_set
	print "follow set:",follow_set

	for i in range(len(first_set)):
		non_terminal = str(first_set[i]['non_term'])
		for k,t in first_set[i].items():
			if k == 'non_term':
				continue;
			if t != 0:
				s.assert_and_track(functions["first"](vars[view_assign[non_terminal]], vars[view_assign[str(k)]]), 'first set input %s %s'%(non_terminal,k))
				constdict['first set input %s %s'%(non_terminal,k)] = functions["first"](vars[view_assign[non_terminal]], vars[view_assign[str(k)]])
			else:
				s.assert_and_track(Not(functions["first"](vars[view_assign[non_terminal]], vars[view_assign[str(k)]])), 'first set input %s %s'%(non_terminal,k))
				constdict['first set input %s %s'%(non_terminal,k)] = Not(functions["first"](vars[view_assign[non_terminal]], vars[view_assign[str(k)]]))

	for i in range(len(follow_set)):
		non_terminal = str(follow_set[i]['non_term'])
		for k,t in follow_set[i].items():
			if k == 'non_term':
				continue;
			if t != 0:
				s.assert_and_track(functions["follow"](vars[view_assign[non_terminal]], vars[view_assign[str(k)]]), 'follow set input %s %s'%(non_terminal, k))
				constdict['follow set input %s %s'%(non_terminal, k)] = functions["follow"](vars[view_assign[non_terminal]], vars[view_assign[str(k)]])
			else:
				s.assert_and_track(Not(functions["follow"](vars[view_assign[non_terminal]], vars[view_assign[str(k)]])), 'follow set input %s %s'%(non_terminal, str(k)))
				constdict['follow set input %s %s'%(non_terminal, str(k))] = Not(functions["follow"](vars[view_assign[non_terminal]], vars[view_assign[str(k)]]))

def repair(solver, original_grammar, num_rules, size_rules):
	view_assign = {}
	
	i = 1
	for ch in non_tokens:
		view_assign[ch] = 'N%d'%(i)
		i += 1

	i = 1
	for ch in tokens:
		view_assign[ch] = 't%d'%(i)
		i += 1
	view_assign['eps'] = 'eps'
	parse_table = get_parse_table()
	first_set = get_first_set()
	follow_set = get_follow_set()
	view_assign['dol'] = 'dol'
	view_assign['$'] = 'dol'
	print('view_assign-',view_assign)
	add_constraints(solver,view_assign,original_grammar,num_rules, size_rules)
	add_parse_table_constraints(solver,parse_table,view_assign)
	# add_first_set_constraints(solver, first_set, follow_set, view_assign)

