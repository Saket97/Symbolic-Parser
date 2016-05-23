from django.db import models

# Create your models here.
class Game(models.Model):
	Response1 = models.CharField(max_length=3,verbose_name="Response1")
	Response2 = models.CharField(max_length=3,verbose_name="Response2")
	Response3 = models.CharField(max_length=3,verbose_name="Response3")

	def __str__(self):
		return 'Player'
