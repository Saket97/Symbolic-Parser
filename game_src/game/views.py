from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
import django_tables2 as tables
from django import forms
# from ...input_specs import * 
# from ...synth import * 
from .models import Game
from .forms import GameForm,GrammarForm,TableForm,grammar,table
from .tables import Parse_Table
from itertools import *
from collections import *
import copy
import pdb
#from test import printsaket
def get_original_grammar():
	original_grammar = [['S', '(', 'S',')','S'], ['S', 'eps', 'eps','eps','eps']]
	return original_grammar

def get_parse_table():
	parse_table = {'non_terms':'S','(':{'S':1},')':{'S':2},'$':{'S':2}}
	return parse_table

# def define_table(columns):
# 	attrs = dict((c,tables.Column()) for c in columns)
# 	attrs['__module__'] = Parse_Table.__module__
# 	attrs['Meta'] = type('Meta', (), dict(attrs={"class":"Parse_Table"}))
# 	klass = type('Dynamic Table',(Parse_Table,),attrs)
# 	return klass



def fill_response(request):
	
	x,y,z = 2,3,4
	x_done, y_done, z_done = False, False, False
	
	original_grammar = get_original_grammar()
	check=['blank']
	
	if request.method == 'POST':
		form = GameForm(request.POST or None)
		gform = grammar(request.POST or None)
		if form.is_valid():
			tmp = copy.deepcopy(original_grammar)
			for i in range(len(original_grammar)):
				for j in range(len(original_grammar[i])):
					if original_grammar[i][j] == 'blank':
						if not x_done:
							original_grammar[i][j] = form.cleaned_data['Response1']
							x_done = True
						else:
							if not y_done:
								original_grammar[i][j] = form.cleaned_data['Response2']
								y_done = True
							else:
								original_grammar[i][j] = form.cleaned_data['Response3']
								z_done = True

					else:
						pass
			original_grammar = copy.deepcopy(tmp)
			return HttpResponseRedirect('/game')


		# solver=main() #returns SP
		# s = solver['constraints']
		# if correct:
		# 	return HttpResponse(<h1>'Correct'</h1>)
		# else:
		# 	tmp = solver['unsat']
		# 	error = []
		# 	if x in tmp:
		# 		error.append('Response1')
		# 	else:
		# 		error.append('')
		# 	if y in tmp:
		# 		error.append('Response2')
		# 	else:
		# 		error.append('')
		# 	if z in tmp:
		# 		error.append('Response3')
		# 	else:
		# 		error.append('')
		# original_grammar = copy.deepcopy(tmp)
		# return HttpResponse(<b>'wrong Responses %s %s %s'%(error[0],error[1],error[2])</b>)
	else:
		form = GameForm()
		gform = grammar()
	b = [1,2,3]
	accept_strings = ['a b c']
	reject_strings = ['a c']
	
	context = {
	'Game':Game.objects.all(),'b':b,'form':form,'gform':gform,'original_grammar':original_grammar,'Response1':x,'Response2':y,'Respons3':z,'total_line':5,'n_rules':2,'size_rules':4, 'check':check, 'accept_strings':accept_strings, 'reject_strings':reject_strings}
	#pdb.set_trace()
	return render(request,'game_form.html',context)


def ParseTable(request):
	original_grammar = [['S', '(', 'S',')','S'], ['S', 'eps', 'eps','eps','eps']]

	parse_table = [OrderedDict([('non_term','S'),('(',1),(')',2),('$',2)])]

	n_rules = len(parse_table)
	size_rules = len(parse_table[0])
	
	############## used for table headers ################## 
	tokens = []
	for i in range(len(parse_table)):
		for k,t in parse_table[i].items():
			if k == 'non_term':
				continue;
			tokens.append(k)
	########################################################
	
	takingParseTableAsInput = False
	################ binding initial data to parse table on the basis of takingPaseTableAsInput ###############
	###Fields are named as row_number starting from 0 and corresponding table header which are terms+'non_term'
	if not takingParseTableAsInput:
		parseTableData = {}
		for i in range(len(parse_table)):
			for k,t in parse_table[i].items():
				parseTableData['%d%s'%(i,k)] = t

	###########################################################################################################
	
	if request.method == 'POST':
		gform = grammar(request.POST or None)
		tform = table(request.POST or None)
	else:
		gform = grammar()
		tform = table(parseTableData)
	total_line = len(original_grammar[0])
	
	context = {'tokens':tokens,'length':len(parse_table[0]),'tform':tform,'gform':gform,'total_line':total_line,'n_rules':n_rules,'size_rules':size_rules,'parse_table':parse_table}
	# pdb.set_trace()
	return render(request,"parse.html",context)

