from django.contrib import admin
from django.utils.safestring import mark_safe

from registration.models import Faculty, Student
from registration.forms import StudentSignupForm

class StudentAdmin(admin.ModelAdmin):
    readonly_fields=('application_id', 'status')
    search_fields = ['roll_no']
    def application_id(self, obj):
    	print(obj.user)
    	return mark_safe('<a href="/accounts/pdf/%d/%s">%d</a> *click to download registraton form' %(obj.pk, obj.phone_no ,obj.pk))
    def status(self, obj):
    	return mark_safe(("Active | %sDeactivate</a>" if obj.user.is_active else "Inactive | %sActivate</a>") %('<a href="/admin/changestatus/student/%d/%s">' %(obj.pk, obj.phone_no)))


# class FacultyAdmin(admin.ModelAdmin):
#     search_fields = ['name',]

admin.site.register(Student, StudentAdmin)
admin.site.register(Faculty)