from django.contrib import admin

# Register your models here.
from .models import Game
class GameModelAdmin(admin.ModelAdmin):
	class Meta:
		model = Game
	

admin.site.register(Game,GameModelAdmin)