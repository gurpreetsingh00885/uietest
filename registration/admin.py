from django.contrib import admin
from django.utils.safestring import mark_safe

from registration.models import Faculty, Student, StudyGroup
from registration.forms import StudentSignupForm
from django.contrib.auth import get_user_model

from django_reverse_admin import ReverseModelAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

User = get_user_model()

class UserInline(admin.StackedInline):
  model = Student
  fk_name = "user"


class StudentAdmin(ReverseModelAdmin):
    search_fields = ['roll_no']
    inline_reverse = [('user', {
    'form': UserCreationForm,
    'fields': ('username', 'email', 'password1', 'password2', 'is_active')
}),]
    inline_type='stacked'
    
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return self.readonly_fields
        return ("application_id", "status",)

    def application_id(self, obj):
        return mark_safe('<a href="/accounts/pdf/%d/%s">%d</a> *click to download registraton form' %(obj.pk, obj.phone_no ,obj.pk))
    def status(self, obj):
        return mark_safe(("Active | %sDeactivate</a>" if obj.user.is_active else "Inactive | %sActivate</a>") %('<a href="/admin/changestatus/student/%d/%s">' %(obj.pk, obj.phone_no)))



class FacultyAdmin(ReverseModelAdmin):
    search_fields = ['name', 'department',]
    inline_reverse = [('user', {
    'form': UserCreationForm,
    'fields': ('username', 'email', 'password1', 'password2', 'is_active')
}),]
    inline_type='stacked'

class StudyGroupAdmin(admin.ModelAdmin):
    readonly_fields=('students',)

    def students(self, obj):
        student_list = obj.student_set.all()
        x = "<ol>"
        for student in student_list:
            x+="<li><a href='/admin/registration/student/%d/change/'>%s</a></li>"%(student.pk , student.roll_no)
        return mark_safe(x+"</ol>")



admin.site.register(Student, StudentAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(StudyGroup, StudyGroupAdmin)