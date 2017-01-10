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
	attrs = dict((f,forms.CharField(widget = forms.TextInput(attrs={'class':'my_custom_class','max_length':3}))) for f in iterate_order)
	attrs['__module__'] = GrammarForm.__module__
	attrs['Meta'] = type('Meta', (), dict(attrs={"class":"Grammar_form"}))
	ogrammar = type('Grammar',(GrammarForm,forms.Form),attrs)
	return ogrammar

def define_table_form():
	parse_table = [OrderedDict([('non_term','S'),('(',1),(')',2),('$',2)])]
	attrs = OrderedDict()
	
	for i in range(len(parse_table)):
		attrs.update({'%d%s'%(i,'non_term'):forms.CharField(widget=forms.TextInput(attrs={'class':'my_custom_class','max_length':3}))})

		for k,t in parse_table[i].items():
			if k == 'non_term':
				continue;
			attrs.update({'%d%s'%(i,k):forms.IntegerField(widget=forms.NumberInput(attrs={'class':'my_custom_class','max_length':3}))})

	attrs['__module__'] = TableForm.__module__
	attrs['Meta'] = type('Meta',(),{})
	return type('Table',(TableForm,forms.Form),attrs)

def define_first_form():
	# parse_table = [OrderedDict([('non_term','S'),('(',1),(')',2),('$',2)])]
	first_set = [OrderedDict([('non_term','S'), ('(',1), (')',0), ('eps',1)])]
	attrs = OrderedDict()
	
	for i in range(len(first_set)):
		attrs.update({'%d%sfirst'%(i,'non_term'):forms.CharField(widget=forms.TextInput(attrs={'class':'my_custom_class','max_length':3}))})

		for k,t in first_set[i].items():
			if k == 'non_term':
				continue;
			attrs.update({'%d%sfirst'%(i,k):forms.IntegerField(widget=forms.NumberInput(attrs={'class':'my_custom_class','max_length':3}))})

	attrs['__module__'] = TableForm.__module__
	attrs['Meta'] = type('Meta',(),{})
	return type('First',(forms.Form,),attrs)

def define_follow_form():
	# parse_table = [OrderedDict([('non_term','S'),('(',1),(')',2),('$',2)])]
	follow_set = [OrderedDict([('non_term','S'), ('(',0), (')',1), ('$',1)])]
	attrs = OrderedDict()
	
	for i in range(len(follow_set)):
		attrs.update({'%d%sfollow'%(i,'non_term'):forms.CharField(widget=forms.TextInput(attrs={'class':'my_custom_class','max_length':3}))})

		for k,t in follow_set[i].items():
			if k == 'non_term':
				continue;
			attrs.update({'%d%sfollow'%(i,k):forms.IntegerField(widget=forms.NumberInput(attrs={'class':'my_custom_class','max_length':3}))})

	attrs['__module__'] = TableForm.__module__
	attrs['Meta'] = type('Meta',(),{})
	return type('Follow',(forms.Form,),attrs)


class GrammarForm(forms.Form):
	# original_grammar = get_original_grammar()
	original_grammar = [['S', '(', 'S',')','S'], ['S', 'eps', 'eps','eps','eps']]
	# __metaclass__ = define_grammar
class TableForm(forms.Form):
	pass



grammar = define_grammar()
table = define_table_form()
first = define_first_form()
follow = define_follow_form()