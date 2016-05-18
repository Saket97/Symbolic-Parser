from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
# from ...input_specs import * 
# from ...synth import * 
from .models import Game
from .forms import GameForm
import copy


def fill_response(request):
	form = GameForm(request.POST or None)
	x,y,z = 2,3,4
	x_done, y_done, z_done = False, False, False
	

	check=['blank']
	if form.is_valid():
		instance = 	form.save(commit = False)
		instance.save()
		#changing blank in original_grammar with filled responses
		global original_grammar
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
		
	b = [1,2,3]
	accept_strings = ['a b c']
	reject_strings = ['a c']
	context = {
	'b':b,'form':form,'original_grammar':original_grammar,'Response1':x,'Response2':y,'Respons3':z,'size_rules':2, 'check':check, 'accept_strings':accept_strings, 'reject_strings':reject_strings}
	return render(request,'game_form.html',context)

def get_original_grammar():
	return original_grammar


original_grammar = [['S', 'blank', 'blank'], ['blank', 'A', 'B']]



