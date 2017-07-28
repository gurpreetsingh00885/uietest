from django.shortcuts import render

from allauth.account.views import SignupView
from .forms import StudentSignupForm
from django.views import View
from django.views.generic.detail import DetailView
from easy_pdf.views import PDFTemplateResponseMixin
from .models import Student

class StudentSignupView(SignupView):
    form_class = StudentSignupForm
    view_name = 'student_signup'


class PDFDetailView(PDFTemplateResponseMixin, DetailView):
    model = Student
    template_name = 'genpdf.html'
    pk_url_kwarg = 'pk'