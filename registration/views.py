from django.shortcuts import render, get_object_or_404
from allauth.account.views import SignupView, LoginView
from .forms import StudentSignupForm
from django.views import View
from django.views.generic.detail import DetailView
from easy_pdf.views import PDFTemplateResponseMixin
from .models import Student, Faculty
from django.http import HttpResponseRedirect, Http404
from allauth.account.forms import LoginForm


class StudentSignupView(SignupView):
    form_class = StudentSignupForm
    view_name = 'student_signup'
    redirect_field_name = 'next'
    def get(self, request, *args, **kwargs):
        return super(StudentSignupView, self).get(request, **kwargs)

    def form_valid(self, form, **kwargs):
        resp = super(StudentSignupView, self).form_valid(form)
        student = Student.objects.get(user=self.user)
        return HttpResponseRedirect("/accounts/pdf/%d/%s" %(student.pk, student.phone_no))

    def get_context_data(self, **kwargs):
        context = super(StudentSignupView, self).get_context_data(**kwargs)
        context['form2'] = LoginForm()
        return context


class NewLoginView(LoginView):
    form_class = LoginForm
    view_name = 'accounts_login'
    redirect_field_name = 'next'
    def get(self, request, *args, **kwargs):
        return super(NewLoginView, self).get(request, **kwargs)

    

    def get_context_data(self, **kwargs):
        context = super(NewLoginView, self).get_context_data(**kwargs)
        context['form2'] = StudentSignupForm()
        return context

class PDFDetailView(PDFTemplateResponseMixin, DetailView):
    model = Student
    template_name = 'genpdf.html'
    pk_url_kwarg = 'pk'
    title="UI-E-TEST Registration Form"
    def get_object(self):
        student = get_object_or_404(Student, phone_no__iexact=self.kwargs['phone'])

        #self.download_filename = student.name.lower().replace(" ","_")+".pdf"
        
        return student

class LandingView(View):
    def get(self, request, **kwargs):
        student = Student.objects.filter(user=request.user)
        if student.exists():
            return render(request, "landing_student.html", {"student": student[0],})
        
        faculty = Faculty.objects.filter(user=request.user)
        if faculty.exists():
            return render(request, "landing_faculty.html", {"faculty": faculty[0], "tests": faculty[0].test_set.all()})
        if request.user.is_superuser:
            return HttpResponseRedirect("/admin/")
        raise Http404

class ActivateStudentAccountView(View):
    def get(self, request, pk, phone, **kwargs):
        try:
            if request.user.is_superuser:
                student = Student.objects.get(pk=pk, phone_no = phone)
                print(student)
                if student.user.is_active:
                    student.user.is_active = False
                else:
                    student.user.is_active = True
                student.user.save()
                return HttpResponseRedirect("/admin/registration/student/%d/change/" %(student.pk))
            else:
                raise Http404
        except:
            raise Http404

