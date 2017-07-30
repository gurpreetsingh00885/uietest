from django.contrib import admin
from django.utils.safestring import mark_safe

from registration.models import Faculty, Student, StudyGroup
from registration.forms import StudentSignupForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserInline(admin.StackedInline):
    model = Student

class StudentAdmin(admin.ModelAdmin):
    readonly_fields=('application_id', 'status')
    search_fields = ['roll_no']
    #inlines = [UserInline,]
    def application_id(self, obj):
        print(obj.user)
        return mark_safe('<a href="/accounts/pdf/%d/%s">%d</a> *click to download registraton form' %(obj.pk, obj.phone_no ,obj.pk))
    def status(self, obj):
        return mark_safe(("Active | %sDeactivate</a>" if obj.user.is_active else "Inactive | %sActivate</a>") %('<a href="/admin/changestatus/student/%d/%s">' %(obj.pk, obj.phone_no)))

# class FacultyAdmin(admin.ModelAdmin):
#     search_fields = ['name',]
class StudyGroupAdmin(admin.ModelAdmin):
    readonly_fields=('students',)

    def students(self, obj):
        student_list = obj.student_set.all()
        x = "<ol>"
        for student in student_list:
            x+="<li><a href='/admin/registration/student/%d/change/'>%s</a></li>"%(student.pk , student.roll_no)
        return mark_safe(x+"</ol>")

admin.site.register(Student, StudentAdmin)
admin.site.register(Faculty)
admin.site.register(StudyGroup, StudyGroupAdmin)