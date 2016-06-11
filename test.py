from input_specs import *
from init import *

def discover(original_grammar):
	non_tokens = []
	for string in original_grammar:
		ch = string[0]
		if ch not in non_tokens:
			non_tokens.append(ch)
		else:
			pass
	return non_tokens

def add_constraints(solver, view_assign, original_grammar, num_rules, size_rules):
	s = solver['constraints']
	vars = solver['vars']
	i = 1
	constdict = solver["dictconst"]
	for r in range(num_rules):
		s.assert_and_track(vars['x%d'%(r*(size_rules+1)+1)] == vars[view_assign[original_grammar[r][0]]], 'input x%d'%(r*(size_rules+1)+1))
		constdict['input x%d'%(r*(size_rules+1)+1)] = vars['x%d'%(r*(size_rules+1)+1)] == vars[view_assign[original_grammar[r][0]]]
		
		print('x%d %s %d'%((r*(size_rules+1)+1),view_assign[original_grammar[r][0]], i))
		i += 1
		
		for j in range(1,size_rules+1):
			
			if original_grammar[r][j] == 'eps':
				pass
				# if (r*(size_rules+1)+j+1) == 5:
				# 	s.assert_and_track(vars['x%d'%(r*(size_rules+1)+j+1)] == vars['eps'], '%d'%(r*(size_rules+1)+j+1))
				# 	i += 1	
				# 	continue
				# s.assert_and_track(vars['x%d'%(r*(size_rules+1)+j+1)] == vars['eps'], 'K%d'%i)
				
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


def repair(solver, original_grammar, num_rules, size_rules):
	view_assign = {}
	non_tokens = discover(original_grammar)
	i = 1
	for ch in non_tokens:
		view_assign[ch] = 'N%d'%(i)
		i += 1

	i = 1
	for ch in tokens:
		view_assign[ch] = 't%d'%(i)
		i += 1
	parse_table = get_parse_table()
	view_assign['dol'] = 'dol'
	view_assign['$'] = 'dol'
	print('view_assign-',view_assign)
	add_constraints(solver,view_assign,original_grammar,num_rules, size_rules)
	add_parse_table_constraints(solver,parse_table,view_assign)

