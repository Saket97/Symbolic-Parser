import django_tables2 as tables
from itertools import *
from .views import *
class Parse_Table(tables.Table):
	class Meta:
		attrs = {'class':'Parse_Table'}