from django import forms
from .models import Game

# class GameForm(forms.ModelForm):
# 	class Meta:
# 		model = Game
# 		fields = [
# 		'Response1','Response2','Response3'
# 		]
# 		# widgets={
# 		# 'Response1':Textarea(attrs={'col':80,'rows':20})
# 		# }

class GameForm(forms.ModelForm):
	# Response1 = forms.CharField(max_length = 3)
	# Response2 = forms.CharField(max_length = 3)
	# Response3 = forms.CharField(max_length = 3)
	class Meta:
		model = Game
		fields = [
		'Response1','Response2','Response3'
		]
	def __init__(self, *args, **kwargs):
		super(GameForm, self).__init__(*args, **kwargs)
		self.fields['Response1'].widget.attrs.update({
			'autocomplete': 'off','class':"my_custom_class"
		})
		self.fields['Response2'].widget.attrs.update({
			'class':"my_custom_class"
		})
		self.fields['Response3'].widget.attrs.update({
			'class':"my_custom_class"
		})
		# for j in forms.fields:
		# 	self.fields[j].widget.attrs.update({
		# 		'class':"my_custom_class"
		# 	})
