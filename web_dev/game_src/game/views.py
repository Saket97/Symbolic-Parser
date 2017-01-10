from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
# from django.core import serializers
import json
from django import forms
# from ...input_specs import * 
# from ...synth import * 
from .models import Game,questions
from .forms import GameForm,GrammarForm,TableForm,grammar,table,first,follow
from synth import *
from itertools import *
from collections import *
import copy
import pdb

accept_strings = ['a b c']
reject_strings = ['a c']
def get_original_grammar():
	original_grammar = [['S', '(', 'S',')','S'], ['S', 'eps', 'eps','eps','eps']]
	return ogrammar

def get_parse_table():
	parse_table = {'non_terms':'S','(':{'S':1},')':{'S':2},'$':{'S':2}}
	return table_parse

def fill_grammar_form(original_grammar):
	grammarData = {}
	n_rules = len(original_grammar)
	size_rules = len(original_grammar[0])
	for i in range(n_rules):
		for j in range(size_rules):
			grammarData['X%d'%(i*(size_rules)+1+j)] = original_grammar[i][j]
	return grammarData	


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
	
	context = {
	'Game':Game.objects.all(),'b':b,'form':form,'gform':gform,'original_grammar':original_grammar,'Response1':x,'Response2':y,'Respons3':z,'total_line':5, 'accept_strings':accept_strings, 'reject_strings':reject_strings}
	#pdb.set_trace()
	return render(request,'game_form.html',context)


def ParseTable(request, username):

	question_instance = questions.objects.get(name=username)
	original_grammar = json.loads(question_instance.grammar)
	print "original_grammar: ",original_grammar
	# original_grammar = [['S', '(', 'S',')','S'], ['S', 'eps', 'eps','eps','eps']]
	# data = serializers.serialize("xml",original_grammar)
	# gameinstance = Game()
	# gameinstance.Response4 = json.dumps(original_grammar)
	# parse_table = [OrderedDict([('non_term','S'),('(',1),(')',2),('$',2)])]
	# ptable_entries = ['non_term','(',')','$']
	ptable_entries = []
	parse_table = json.loads(question_instance.parsetable)
	for i in range(len(parse_table)):
		parse_table[i] = OrderedDict(parse_table[i])
	for k,t in parse_table[0].items():
		ptable_entries.append(str(k))
	print "parse_table: ",parse_table


	n_rules = len(original_grammar)
	size_rules = len(original_grammar[0])-1
	
	n_table = len(parse_table)
	n_elements = len(parse_table[0])

	############## used for table headers ################## 
	tokens = []
	# for i in range(len(parse_table)):
	# 	for k,t in parse_table[i].items():
	# 		if k == 'non_term':
	# 			continue;
	# 		tokens.append(k)

	for k,t in parse_table[0].items():
		if k == 'non_term':
			continue;
		else:
			tokens.append(str(k))
	########################################################
	
	takingParseTableAsInput = False
	################ binding initial data to parse table on the basis of takingPaseTableAsInput ###############
	###Fields are named as row_number starting from 0 and corresponding table header which are terms+'non_term'
	
	if not takingParseTableAsInput:
		parseTableData = {}
		for i in range(len(parse_table)):
			for k,t in parse_table[i].items():
				parseTableData['%d%s'%(i,str(k))] = t
		print "ptable data: ",parseTableData

	###########################################################################################################
	
	############## binding data to grammar form ########################
	if takingParseTableAsInput:
		grammarData = fill_grammar_form(original_grammar)
	
	######################################################################
	total_line = len(original_grammar[0])

	if request.method == 'POST':
		gform = grammar(request.POST or None)
		tform = table(request.POST or None)
		if  tform.is_valid() and gform.is_valid():
			################SAVING IN DATABASE ###############

			forminstance = Game(Response1=gform.cleaned_data['X1'], Response2=gform.cleaned_data['X2'], Response3=gform.cleaned_data['X3'])
			forminstance.save()
			jsondec = json.decoder.JSONDecoder()
			q = jsondec.decode(Game.objects.get(id=33).Response4)
			print "saket"
			print "q",q
			##################################################
			ogrammar = []
			table_parse = []
			for r in range(n_rules):
				tmp = []
				var = 'X%d'%(r*total_line+1)
				tmp.append(str(gform.cleaned_data[var]))
				for i in range(1,size_rules+1):
					var = 'X%d'%(r*total_line+1+i)
					tmp.append(str(gform.cleaned_data[var]))
				ogrammar.append(tmp)

			for i in range(n_table):
				tmp = OrderedDict()
				for k in ptable_entries:
					var = '%d%s'%(i,k)
					if k=="non_term":
						tmp[str(k)] = str(tform.cleaned_data[var])
					else:
						tmp[str(k)] = int(tform.cleaned_data[var])
				table_parse.append(tmp)
			answer = main(ogrammar,table_parse,parsetablegrammar = True)
			if answer[1]:
				return render(request,"correct.html",{})
			else:
				print answer[0]
				return render(request,"incorrect.html",{})

		else:
			return render(request,"notvalid.html",{})
	else:
		if takingParseTableAsInput:
			gform = grammar(grammarData)
			tform = table()
			
		else:
			gform = grammar()
			tform = table(parseTableData)
	accept_strings = ["( )","( ) ( )", "( ( ) )","( ) ( ( ) )"]
	reject_strings = ["(",")","( ) ("]
	qset = questions.objects.all()
	context = {'qset':qset,'tokens':tokens,'length':len(parse_table[0]),'tform':tform,'gform':gform,'total_line':total_line,'accept_strings':accept_strings,'reject_strings':reject_strings,'parse_table':parse_table}
	# pdb.set_trace()
	return render(request,"parse.html",context)

def FirstFollow(request, username):
	question_instance = questions.objects.get(name=username)
	original_grammar = json.loads(question_instance.grammar)
	# original_grammar = [['S', '(', 'S',')','S'], ['S', 'eps', 'eps','eps','eps']]
	first_set = [OrderedDict([('non_term','S'),('(',1), (')',0), ('eps',1)])]
	follow_set = [OrderedDict([('non_term','S'), ('(',0), (')',1), ('$',1)])]
	first_set = json.loads(question_instance.firstset)
	for i in range(len(first_set)):
		first_set[i] = OrderedDict(first_set[i])
	follow_set = json.loads(question_instance.followset)
	for i in range(len(follow_set)):
		follow_set[i] = OrderedDict(follow_set[i])

	first_set_data = {}
	follow_set_data = {}

	takingfirstasinput = False

	first_tokens = []
	########## first set table header #################################
	for k,t in first_set[0].items():
		if k == 'non_term':
			continue
		first_tokens.append(str(k))
	###################################################################

	########## follow set table header ################################
	follow_tokens = []
	for k,t in follow_set[0].items():
		if k=='non_term':
			continue
		follow_tokens.append(str(k))
	###################################################################
	########## binding data to first/follow set form ###################

	for i in range(len(first_set)):
		for k,t in first_set[i].items():
			var = '%d%sfirst'%(i,k)
			if k=="non_term":
				first_set_data[str(var)] = str(t)
			else:
				first_set_data[str(var)] = int(t)
	
	for i in range(len(follow_set)):
		for k,t in follow_set[i].items():
			var = '%d%sfollow'%(i,k)
			if k == 'non_term':
				follow_set_data[str(var)] = str(t)
			else:
				follow_set_data[str(var)] = int(t)


	####################################################################	

	########binding data to grammar form ###############################
	grammarData = {}
	grammarData = fill_grammar_form(original_grammar)
	####################################################################

	total_line = len(original_grammar[0])

	if request.method == 'POST':
		gform = grammar(request.POST or None)
		firstform = first(request.POST or None)
		followform = follow(request.POST or None)
		# pdb.set_trace()
		if gform.is_valid() and firstform.is_valid() and followform.is_valid() :
			ogrammar = []
			set_first = []
			set_follow = []
			n_rules = len(original_grammar)
			size_rules = len(original_grammar[0])-1
			
			##### recording grammar input ##########
			for i in range(n_rules):
				tmp = []
				for j in range(size_rules+1):
					tmp.append(str(gform.cleaned_data['X%d'%(i*total_line+j+1)]))
				ogrammar.append(tmp)
			#########################################

			##### recording first set input #############
			for i in range(len(first_set)):
				tmp = OrderedDict()
				for k,t in first_set[i].items():
					if k == 'non_term':
						tmp[str(k)] = str(firstform.cleaned_data['%d%sfirst'%(i,k)])
					else:
						tmp[str(k)] = int(firstform.cleaned_data['%d%sfirst'%(i,k)])

				set_first.append(tmp)
			print "first set in views: ",set_first
			print "first set form S(:",firstform.cleaned_data['0(first']
			#########################################

			##### recording follow set input #########
			for i in range(len(follow_set)):
				tmp = OrderedDict()
				for k,t in follow_set[i].items():
					if k == 'non_term':
						tmp[str(k)] = str(followform.cleaned_data['%d%sfollow'%(i,k)])
					else:
						tmp[str(k)] = int(followform.cleaned_data['%d%sfollow'%(i,k)])

				set_follow.append(tmp)

			##########################################

			answer = main(ogrammar,first_set=set_first,follow_set=set_follow,firstgrammar=True)
			if answer[1]:
				return render(request,"correct.html",{})
			else:
				print answer[0]
				return render(request,"incorrect.html",{})

		else:
			return render(request,"notvalid.html",{})
	else:
		gform = grammar(grammarData)
		firstform = first(first_set_data)
		followform = follow(follow_set_data)
		# pdb.set_trace()
	qset = questions.objects.all()
	accept_strings = ["( )","( ) ( )", "( ( ) )","( ) ( ( ) )"]
	reject_strings = ["(",")","( ) ("]
	context = {'qset':qset,'gform':gform, 'total_line':total_line, 'firstform':firstform,'followform':followform, 'length':len(first_set[0]), 'first_tokens':first_tokens, 'follow_tokens':follow_tokens, 'accept_strings':accept_strings, 'reject_strings':reject_strings}
	return render(request, "firstfollow.html", context)

def index(request):
	return render(request,"index.html", {})
ogrammar = []
table_parse = []