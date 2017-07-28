from django.contrib import admin
from django.utils.safestring import mark_safe

from registration.models import Faculty, Student
from registration.forms import StudentSignupForm

class StudentAdmin(admin.ModelAdmin):
    readonly_fields=('application_id',)
    search_fields = ['roll_no']
    def application_id(self, obj):
    	return mark_safe('<a href="/accounts/pdf/%d/%s">%d</a>' %(obj.pk, obj.phone_no ,obj.pk))

# class FacultyAdmin(admin.ModelAdmin):
#     search_fields = ['name',]

admin.site.register(Student, StudentAdmin)
admin.site.register(Faculty)