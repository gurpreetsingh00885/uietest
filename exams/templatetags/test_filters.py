from django import template

register = template.Library()

@register.filter
def get_option_alpha(code):
	return list(" ABCDEFGHIJKLMNOPQRSTUVWXYZ")[code]

@register.filter
def reverseset(queryset):
        return queryset.order_by("pk")




