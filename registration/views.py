from django.shortcuts import render

from allauth.account.views import SignupView
from .forms import StudentSignupForm

class StudentSignupView(SignupView):
    form_class = StudentSignupForm
    view_name = 'student_signup'