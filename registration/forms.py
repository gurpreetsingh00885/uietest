from .models import Faculty, Student
from django import forms
from allauth.account.forms import SignupForm

class StudentSignupForm(SignupForm):
    name = forms.CharField(max_length=50, required=True, strip=True)
    phone_no = forms.CharField(max_length=10, required=True, strip=True)
    roll_no = forms.CharField(max_length=10, required=True, strip=True)

    # Override the save method to save the extra fields
    # (otherwise the form will save the User instance only)
    def save(self, request):
        # Save the User instance and get a reference to it
        user = super(StudentSignupForm, self).save(request)
        # Create an instance of your model with the extra fields
        # then save it.
        # (N.B: the are already cleaned, but if you want to do some
        # extra cleaning just override the clean method as usual)
        student_user = Student(
            user=user,
            name=name
        )
        student_user.save()

        return student_user.user