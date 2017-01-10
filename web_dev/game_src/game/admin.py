from django.contrib import admin

# Register your models here.
from .models import Game,questions
class GameModelAdmin(admin.ModelAdmin):
	class Meta:
		model = Game
	
class QuestionModelAdmin(admin.ModelAdmin):
	class Meta:
		model = questions
admin.site.register(Game,GameModelAdmin)
admin.site.register( questions, QuestionModelAdmin)