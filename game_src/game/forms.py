from django import forms
from .models import Game
from .views import *
from itertools import *
from collections import *
import pdb

class GameForm(forms.Form):
	Response1 = forms.CharField(widget = forms.TextInput(attrs={'class':'my_custom_class','max_length':3}))
	Response2 = forms.CharField(widget = forms.TextInput(attrs={'class':'my_custom_class','max_length':3}))
	Response3 = forms.CharField(widget = forms.TextInput(attrs={'class':'my_custom_class','max_length':3}))
	# class Meta:
	# 	model = Game
	# 	fields = [
	# 	'Response1','Response2','Response3
	# 	]
	# def __init__(self, *args, **kwargs):
		# super(GameForm, self).__init__(*args, **kwargs)
		# self.fields['Response1'].widget.attrs.update({
		# 	'autocomplete': 'off','class':"my_custom_class"
		# })
		# self.fields['Response2'].widget.attrs.update({
		# 	'class':"my_custom_class"
		# })
		# self.fields['Response3'].widget.attrs.update({
		# 	'class':"my_custom_class"
		# })
		# fields = ['Response1','Response2','Response3']
		# for j in fields:
			# self.fields[j].widget.attrs.update({
				# 'class':"my_custom_class"
			# })



def define_grammar():
	original_grammar = [['S', '(', 'S',')','S'], ['S', 'eps', 'eps','eps','eps']]
	n_rules = len(original_grammar)
	size_rules = len(original_grammar[0])
	fields = {}
	iterate_order = []
	for i in range(n_rules):
		for j in range(1,size_rules+1):
			iterate_order.append('X%d'%(i*size_rules+j))
			tmp = {'X%d'%(i*size_rules + j):[i,j-1]}
			fields.update(tmp)
	attrs = dict((f,forms.CharField(widget = forms.TextInput(attrs={'class':'my_custom_class','max_length':3,'value':original_grammar[fields[f][0]][fields[f][1]]}))) for f in iterate_order)
	attrs['__module__'] = GrammarForm.__module__
	attrs['Meta'] = type('Meta', (), dict(attrs={"class":"Grammar_form"}))
	ogrammar = type('Grammar',(GrammarForm,),attrs)
	return ogrammar

def define_table_form():
	parse_table = [OrderedDict([('non_term','S'),('(',1),(')',2),('$',2)])]
	attrs = OrderedDict()
	for i in range(len(parse_table)):
		for k,t in parse_table[i].items():
			attrs.update({'%d%s'%(i,k):forms.CharField(widget=forms.TextInput(attrs={'class':'my_custom_class','max_length':3}))})

	attrs['__module__'] = TableForm.__module__
	attrs['Meta'] = type('Meta',(),{})
	return type('Table',(TableForm,),attrs)

class GrammarForm(forms.Form):
	# original_grammar = get_original_grammar()
	original_grammar = [['S', '(', 'S',')','S'], ['S', 'eps', 'eps','eps','eps']]
	# __metaclass__ = define_grammar
class TableForm(forms.Form):
	pass

grammar = define_grammar()
table = define_table_form()