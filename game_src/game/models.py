from django.db import models

# Create your models here.
class Game(models.Model):
	Response1 = models.CharField(max_length=3,verbose_name="Response1")
	Response2 = models.CharField(max_length=3,verbose_name="Response2")
	Response3 = models.CharField(max_length=3,verbose_name="Response3")
	Response4 = models.TextField(null = True)
	def __str__(self):
		return str(self.id)

	def __unicode__(self):
		return str(self.id)


class questions(models.Model):
	
	name = models.CharField(null = False, max_length=15, default="question")
	grammar = models.TextField(null = True)
	parsetable = models.TextField(null = True)
	firstset = models.TextField(null = True)
	followset = models.TextField(null = True)

	def __unicode__(self):
		return self.name


