from django.contrib import admin
from registration.models import Faculty, Student
from registration.forms import StudentSignupForm

class StudentAdmin(admin.ModelAdmin):
    search_fields = ['roll_no',]

# class FacultyAdmin(admin.ModelAdmin):
#     search_fields = ['name',]

admin.site.register(Student, StudentAdmin)
admin.site.register(Faculty)