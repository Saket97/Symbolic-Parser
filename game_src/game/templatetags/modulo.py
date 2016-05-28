from django import template

register = template.Library()

@register.filter(name="modulo")
def modulo(m,n):
	return m%n == 0