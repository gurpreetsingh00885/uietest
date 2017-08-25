from django import forms
from django.forms.formsets import BaseFormSet
from .models import Image
from registration.models import StudyGroup

class TestForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    date = forms.DateField(required=True)
    time = forms.TimeField(required=True)
    duration = forms.DurationField(required=True)

class QuestionForm(forms.Form):
    statement = forms.CharField(max_length=1000, required=True, strip=True, widget=forms.Textarea(attrs={"placeholder":"Question Statement",}))

class OptionForm(forms.Form):
    value = forms.CharField(max_length=100, strip=True, widget=forms.Textarea(attrs={"placeholder":"Option"}))
    def __init__(self, *args, **kwargs):
        super(OptionForm, self).__init__(*args, **kwargs)

        self.fields['correct'] = forms.BooleanField( widget = forms.RadioSelect(choices=((self.prefix, 'Correct'),)))

    def add_prefix(self, field):
        if field == 'correct':
        	return field
        else: 
        	return self.prefix and ('%s-%s' % (self.prefix, field)) or field


class AssignForm(forms.Form):
    group = forms.ModelChoiceField(queryset=StudyGroup.objects.all(), required=True, empty_label=None)


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')    
    class Meta:
        model = Image
        fields = ('image', )




class BaseQuestionFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return



class BaseOptionFormSet(BaseFormSet):

    def clean(self):
        if any(self.errors):
            return
        

    def total_form_count(self):
            if self.initial_form_count() > 0:
                total_forms = self.initial_form_count()
            else:
                total_forms = self.initial_form_count() + self.extra
            if total_forms > self.max_num > 0:
                total_forms = self.max_num
            return total_forms