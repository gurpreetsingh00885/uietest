from .models import Faculty, Student
from django import forms
from allauth.account.forms import SignupForm

class StudentSignupForm(SignupForm):
    name = forms.CharField(max_length=50, required=True, strip=True)
    phone_no = forms.CharField(max_length=10, required=True, strip=True)
    roll_no = forms.CharField(max_length=10, required=True, strip=True)


    YEAR_CHOICES = (  
    ('1', '1st'),
    ('2', '2nd'),
    ('3', '3rd'),
    ('4', '4th'),
)

    BRANCH_CHOICES = (  
    ('CS', 'Computer Science & Engineering'),
    ('IT', 'Information Technoology'),
    ('BT', 'Biotechnology'),
    ('EC', 'Electronics and Communication Engineering'),
    ('EE', 'Electrical and Electronics Engineering'),
    ('ME', 'Mechanical Engineering'),
)

    branch = forms.ChoiceField(choices=BRANCH_CHOICES, required=True )
    year = forms.ChoiceField(choices=YEAR_CHOICES, required=True )
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
            name=self.cleaned_data['name'],
            branch = self.cleaned_data['branch'],
            year = self.cleaned_data['year']
        )
        student_user.save()

        return student_user.user

    def clean(self):
        form_data = self.cleaned_data
        print(self._errors)
        if (len(form_data['roll_no'])!=8 or form_data['roll_no'][:2].lower()!="ue" or not form_data['roll_no'][2:].isdigit()):
            self.add_error("roll_no","Roll No. is not valid!")

        if len(form_data['phone_no'])!=10 or not form_data['phone_no'].isdigit():
            self.add_error("phone_no","Phone No. is not valid!")

        return form_data