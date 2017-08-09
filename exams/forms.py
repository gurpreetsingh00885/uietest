from django import forms
from django.forms.formsets import BaseFormSet

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

class BaseQuestionFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

        for form in self.forms:
            if form.cleaned_data:
                print("question: ",form.cleaned_data)



class BaseOptionFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

        for form in self.forms:
            if form.cleaned_data:
                print(form.cleaned_data)