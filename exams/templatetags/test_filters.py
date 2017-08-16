from django import template

register = template.Library()

@register.filter
def get_option_alpha(code):
	return list(" ABCDEFGHIJKLMNOPQRSTUVWXYZ")[code]



