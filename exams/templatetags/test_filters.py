from django import template
import datetime


register = template.Library()

@register.filter
def get_option_alpha(code):
	return list(" ABCDEFGHIJKLMNOPQRSTUVWXYZ")[code]

@register.filter
def reverseset(queryset):
        return queryset.order_by("pk")
@register.filter
def is_over(test):
	dateandtime = datetime.datetime(test.date.year, test.date.month, test.date.day, test.time.hour, test.time.minute, test.time.second)        
	time_left = test.duration.total_seconds()+(dateandtime - datetime.datetime.now()).total_seconds()
	if time_left<0:
		return True
	return False

@register.filter
def count_test(queryset):
	for test in queryset:
		dateandtime = datetime.datetime(test.date.year, test.date.month, test.date.day, test.time.hour, test.time.minute, test.time.second)        
		time_left = test.duration.total_seconds()+(dateandtime - datetime.datetime.now()).total_seconds()
		if time_left>0:
			return True
	return False

@register.filter
def count_test_over(queryset):
	for test in queryset:
		dateandtime = datetime.datetime(test.date.year, test.date.month, test.date.day, test.time.hour, test.time.minute, test.time.second)        
		time_left = test.duration.total_seconds()+(dateandtime - datetime.datetime.now()).total_seconds()
		if time_left<0:
			return True
	return False
