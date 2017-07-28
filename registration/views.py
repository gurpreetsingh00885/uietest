from django.shortcuts import render, get_object_or_404
from allauth.account.views import SignupView
from .forms import StudentSignupForm
from django.views import View
from django.views.generic.detail import DetailView
from easy_pdf.views import PDFTemplateResponseMixin
from .models import Student
from django.http import HttpResponseRedirect

class StudentSignupView(SignupView):
    form_class = StudentSignupForm
    view_name = 'student_signup'
    redirect_field_name = 'next'


    def form_valid(self, form, **kwargs):
        resp = super(StudentSignupView, self).form_valid(form)
        return HttpResponseRedirect("/accounts/pdf/%d" %(Student.objects.get(user=self.user).pk))

class PDFDetailView(PDFTemplateResponseMixin, DetailView):
    model = Student
    template_name = 'genpdf.html'
    pk_url_kwarg = 'pk'
    title="UI-E-TEST Registration Form"
    def get_object(self):
        student = get_object_or_404(Student, phone_no__iexact=self.kwargs['phone'])

        self.download_filename = student.name.lower().replace(" ","_")+".pdf"
        
        return student