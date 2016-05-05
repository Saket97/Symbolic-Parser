from django.db import models

# Create your models here.
class Game(models.Model):
	Response1 = models.CharField(max_length=3)
	Response2 = models.CharField(max_length=3)
	Response3 = models.CharField(max_length=3)

	def __str__(self):
		return 'Player'
