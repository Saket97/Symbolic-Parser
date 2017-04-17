from finalTestFilesOOPSLA.input_specs_tiger0 import *
from init import *
from z3 import *
import datetime
import calendar
import time
def add_constraints(solver, view_assign, original_grammar, num_rules, size_rules):
	print "asserting grammar in %s"%str(datetime.timedelta(seconds=(calendar.timegm(time.gmtime()))))

	s = solver['constraints']
	vars = solver['vars']
	i = 1
	size_rules = len(original_grammar[0])-1
	constdict = solver["dictconst"]
	for r in range(num_rules):
		# print "Asserting rule: ",r
		s.add(vars['x%d'%(r*(size_rules+1)+1)] == vars[view_assign[original_grammar[r][0]]])
		i += 1
		
		for j in range(1,size_rules+1):
			# print "j:",j
			if original_grammar[r][j] == 'eps':
				# print 'x%d = eps'%(r*(size_rules+1)+j+1)
				s.add(vars['x%d'%(r*(size_rules+1)+j+1)] == vars['eps'])
				i += 1
			else:
				# constdict['input x%d'%(r*(size_rules+1)+j+1)] = vars['x%d'%(r*(size_rules+1)+j+1)] == vars[view_assign[original_grammar[r][j]]]
				# print 'x%d = %s'%(r*(size_rules+1)+j+1,original_grammar[r][j])
				s.add(vars['x%d'%(r*(size_rules+1)+j+1)] == vars[view_assign[original_grammar[r][j]]])
				i += 1
	
	print "asserting grammar in %s"%str(datetime.timedelta(seconds=(calendar.timegm(time.gmtime()))))


def add_parse_table_constraints(solver,parse_table,view_assign):
	print "asserting ptable in %s"%str(datetime.timedelta(seconds=(calendar.timegm(time.gmtime()))))

	print "adding parse table..."
	s = solver["constraints"]
	vars = solver['vars']
	functions = solver['functions']
	constdict = solver["dictconst"]
	# print "parse_table: ",parse_table
	for i in range(len(parse_table)):
		non_terminal = parse_table[i]['non_term']
		for k,t in parse_table[i].items():
			if k == 'non_term':
				continue
			if t:	
				s.add(functions['parseTable'](vars[view_assign[non_terminal]],vars[view_assign[k]]) == vars['rule%d'%(t)])
				constdict['%s %s parse table input'%(non_terminal,k)] = functions['parseTable'](vars[view_assign[non_terminal]],vars[view_assign[k]]) == vars['rule%d'%(t)]
			else:
				s.add(functions['parseTable'](vars[view_assign[non_terminal]],vars[view_assign[k]]) == 0)
				constdict['%s %s parse table input'%(non_terminal,k)] = functions['parseTable'](vars[view_assign[non_terminal]],vars[view_assign[k]]) == 0
	print "asserting ptable in %s"%str(datetime.timedelta(seconds=(calendar.timegm(time.gmtime()))))


def add_first_set_constraints(solver, first_set, follow_set, view_assign):
	s = solver["constraints"]
	vars = solver["vars"]
	functions = solver["functions"]
	constdict = solver["dictconst"]
	# print "first set:",first_set
	# print "follow set:",follow_set

	for i in range(len(first_set)):
		non_terminal = str(first_set[i]['non_term'])
		for k,t in first_set[i].items():
			if k == 'non_term':
				continue;
			if t != 0:
				s.add(functions["first"](vars[view_assign[non_terminal]], vars[view_assign[str(k)]]))
				constdict['first set input %s %s'%(non_terminal,k)] = functions["first"](vars[view_assign[non_terminal]], vars[view_assign[str(k)]])
			else:
				s.add(Not(functions["first"](vars[view_assign[non_terminal]], vars[view_assign[str(k)]])))
				constdict['first set input %s %s'%(non_terminal,k)] = Not(functions["first"](vars[view_assign[non_terminal]], vars[view_assign[str(k)]]))

	for i in range(len(follow_set)):
		non_terminal = str(follow_set[i]['non_term'])
		for k,t in follow_set[i].items():
			if k == 'non_term':
				continue;
			if t != 0:
				s.add(functions["follow"](vars[view_assign[non_terminal]], vars[view_assign[str(k)]]))
				constdict['follow set input %s %s'%(non_terminal, k)] = functions["follow"](vars[view_assign[non_terminal]], vars[view_assign[str(k)]])
			else:
				s.add(Not(functions["follow"](vars[view_assign[non_terminal]], vars[view_assign[str(k)]])))
				constdict['follow set input %s %s'%(non_terminal, str(k))] = Not(functions["follow"](vars[view_assign[non_terminal]], vars[view_assign[str(k)]]))

def repair(solver, original_grammar, num_rules, size_rules):
	view_assign = {}
	view_assign_t = {}
	i = 1
	for ch in non_tokens:
		view_assign[ch] = 'N%d'%(i)
		i += 1

	i = 1
	for ch in tokens:
		view_assign[ch] = 't%d'%(i)
		view_assign_t['t%d'%i] = ch
		i += 1
	view_assign['eps'] = 'eps'
	print "view_assign",view_assign
	solver["view_assign"] = view_assign
	solver["view_assign_t"] = view_assign_t
	parse_table = get_parse_table()
	# print "PARSE TABLE:", parse_table
	view_assign['dol'] = 'dol'
	view_assign['$'] = 'dol'
	add_constraints(solver,view_assign,original_grammar,num_rules, size_rules)
	# print view_assign
	add_parse_table_constraints(solver,parse_table,view_assign)
	# add_first_set_constraints(solver, first_set, follow_set, view_assign)

