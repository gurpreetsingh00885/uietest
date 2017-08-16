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
    list_display=['name', 'roll_no', 'email']
    inline_reverse = [('user', {
    'form': UserCreationForm,
    'fields': ('username', 'email', 'password1', 'password2',)
        }),]
    inline_type='stacked'
    
    def email(self, obj):
        return obj.user.email

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return self.readonly_fields
        return ("application_id", "status", "email", "password",)
    
    def get_formsets_with_inlines(self, request, obj=None):
        if obj is None:
            return super(StudentAdmin, self).get_formsets_with_inlines(request, obj)
        return ()

    def password(self, obj):
        return mark_safe('Cannot view the password but you can change it <a href="/admin/auth/user/%d/password/" target="_blank">here</a>.' %(obj.user.pk))

    def application_id(self, obj):
        return mark_safe('<a href="/accounts/pdf/%d/%s">%d</a> *click to download registraton form' %(obj.pk, obj.phone_no ,obj.pk))
    

    def status(self, obj):
        return mark_safe(("Active | %sDeactivate</a>" if obj.user.is_active else "Inactive | %sActivate</a>") %('<a href="/admin/changestatus/student/%d/%s">' %(obj.pk, obj.phone_no)))
    

    # def render_change_form(self, request, context, **kwargs):
    #     print(context['inline_admin_formsets'][0].forms)
    #     return super(StudentAdmin, self).render_change_form(request, context, **kwargs)
        


class FacultyAdmin(ReverseModelAdmin):
    search_fields = ['name', 'department', 'email', 'phone_no']
    list_display=["name", "department"]
    inline_reverse = [('user', {
    'form': UserCreationForm,
    'fields': ('username', 'email', 'password1', 'password2',)
}),]
    inline_type='stacked'

    def get_formsets_with_inlines(self, request, obj=None):
        if obj is None:
            return super(FacultyAdmin, self).get_formsets_with_inlines(request, obj)
        return ()

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return self.readonly_fields
        return ("password", )

    def email(self, obj):
        return obj.user.email

    def password(self, obj):
        return mark_safe('Cannot view the password but you can change it <a href="/admin/auth/user/%d/password/" target="_blank">here</a>.' %(obj.user.pk))


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
