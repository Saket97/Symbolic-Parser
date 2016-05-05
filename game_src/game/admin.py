from django.contrib import admin

# Register your models here.
from .models import Game
class GameModelAdmin(admin.ModelAdmin):
	# list_display = ['title', 'updated', 'timestamp']
	# list_display_links = ['updated']
	# list_display_filter = ['updated', 'timestamp']
	# search_fields = ['title', 'content']
	list_display = ['Response1', 'Response2', 'Response3']
	class Meta:
		model = Game
	# formfield_overrides = {
 #        models.CharField: {'widget': TextInput(attrs={'size':'20'})}
 #        # models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
 #    }


admin.site.register(Game,GameModelAdmin)