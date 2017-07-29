from django.shortcuts import render, get_object_or_404
from allauth.account.views import SignupView
from .forms import StudentSignupForm
from django.views import View
from django.views.generic.detail import DetailView
from easy_pdf.views import PDFTemplateResponseMixin
from .models import Student
from django.http import HttpResponseRedirect, Http404

class StudentSignupView(SignupView):
    form_class = StudentSignupForm
    view_name = 'student_signup'
    redirect_field_name = 'next'


    def form_valid(self, form, **kwargs):
        resp = super(StudentSignupView, self).form_valid(form)
        student = Student.objects.get(user=self.user)
        return HttpResponseRedirect("/accounts/pdf/%d/%s" %(student.pk, student.phone_no))

class PDFDetailView(PDFTemplateResponseMixin, DetailView):
    model = Student
    template_name = 'genpdf.html'
    pk_url_kwarg = 'pk'
    title="UI-E-TEST Registration Form"
    def get_object(self):
        student = get_object_or_404(Student, phone_no__iexact=self.kwargs['phone'])

        #self.download_filename = student.name.lower().replace(" ","_")+".pdf"
        
        return student

class StudentLandingView(View):
	def get(self, request, **kwargs):
		student = Student.objects.get(user=request.user)
		return render(request, "landing_student.html", {"student": student,})

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

