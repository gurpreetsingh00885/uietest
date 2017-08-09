from django.forms.formsets import formset_factory
from django.shortcuts import redirect, render, Http404, HttpResponseRedirect
from django.http import HttpResponse
from .forms import TestForm, BaseOptionFormSet, QuestionForm, OptionForm
from .models import Test, Option, Question
from registration.models import Faculty, Student
from django.forms.formsets import INITIAL_FORM_COUNT
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string
from django.views.generic.edit import UpdateView

def add_question(request, pk):
    try:
        if not Faculty.objects.filter(user=request.user).exists():
            raise PermissionDenied
    except TypeError:
        raise PermissionDenied

    test = None
    try:
        test = Test.objects.get(pk=pk)
    except:
        raise Http404

    if not test.owner == Faculty.objects.get(user=request.user):
        raise PermissionDenied
    # Create the formset, specifying the form and formset we want to use.
    OptionFormSet = formset_factory(OptionForm, formset=BaseOptionFormSet)
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        option_formset = OptionFormSet(request.POST)

        if question_form.is_valid() and option_formset.is_valid():
            question = Question.objects.create(statement=question_form.cleaned_data.get('statement'), test=test)
            question.save()

            for option_form in option_formset:
                correct = True if request.POST['correct']==option_form.prefix else False
                value = option_form.cleaned_data.get('value')
                Option.objects.create(question=question, value=value, is_correct=correct)

            return HttpResponseRedirect("/tests/edit/"+str(test.pk))
               
    else:
        question_form = QuestionForm()
        option_formset = OptionFormSet()

    context = {
        'question_form': question_form,
        'option_formset': option_formset,
        'test': test,
    }
    if request.is_ajax():
        return render_to_string('exams/addquestion.html', context)
    return render(request, 'exams/addquestion.html', context)


def add_test(request):
    owner = None
    try:
        if not Faculty.objects.filter(user=request.user).exists():
            raise PermissionDenied
        else:
            owner = Faculty.objects.get(user=request.user)
    except TypeError:
        raise PermissionDenied
    # Create the formset, specifying the form and formset we want to use

    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            Test.objects.create(title=form.cleaned_data['title'], owner=owner, duration=form.cleaned_data['duration'], time=form.cleaned_data['time'], date=form.cleaned_data['date']).save()
            return HttpResponse("Added Test")           
    else:
        form = TestForm()

    context = {
        "form": form,
    }

    return render(request, 'exams/addexam.html', context)


def edit_test(request, pk):
    owner = None
    test = None
    try:
        if not Faculty.objects.filter(user=request.user).exists():
            raise PermissionDenied
        else:
            owner = Faculty.objects.get(user=request.user)
    except TypeError:
        raise PermissionDenied

    try:
        test = Test.objects.get(pk=pk)
    except:
        raise Http404

    if not test.owner == owner:
        raise PermissionDenied

    if request.method == 'GET':
        
        return render(request, 'exams/edittest.html', {"test":test, "questions": test.question_set.all()})


class QuestionUpdate(UpdateView):
    model = Question
    fields = "__all__"
    template_name = 'exams/editquestion.html'
    def get_success_url(self, **kwargs):
        return "/tests/edit/"+str(self.object.test.pk)
    def get_context_data(self, **kwargs):
        context = super(QuestionUpdate, self).get_context_data(**kwargs)
        initial = [{'value': option.value, 'correct': option.is_correct} for option in self.object.option_set.all()]
        OptionFormSet = formset_factory(OptionForm, formset=BaseOptionFormSet)
        option_formset = OptionFormSet(initial=initial)
        option_formset.extra_forms.clear()
        context['option_formset'] = option_formset
        return context

    #def post(self, request, *args, **kwargs):
        # OptionFormSet = formset_factory(OptionForm, formset=BaseOptionFormSet)
        # option_formset = OptionFormSet(request.POST)
        # form = QuestionForm(request.POST)
        # print(form)
        # if option_formset.is_valid():
        #     return super(QuestionUpdate, self).post(request, *args, **kwargs)
        # else:
        #     return render(request, "exams/editquestion.html", {'option_formset':option_formset, "form":form})
    def form_valid(self, form):
        OptionFormSet = formset_factory(OptionForm, formset=BaseOptionFormSet)
        option_formset = OptionFormSet(self.request.POST)
        if not option_formset.is_valid():
            return render(self.request, "exams/editquestion.html", {'option_formset':option_formset, "form":form})
        return super(QuestionUpdate, self).form_valid(form)
edit_question = QuestionUpdate.as_view()