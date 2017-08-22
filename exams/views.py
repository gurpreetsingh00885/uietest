from django.forms.formsets import formset_factory
from django.shortcuts import redirect, render, Http404, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from .forms import TestForm, BaseOptionFormSet, QuestionForm, OptionForm, ImageForm, AssignForm
from .models import Test, Option, Question, Image, TestResponse, Answer
from registration.models import Faculty, Student, StudyGroup
from django.forms.formsets import INITIAL_FORM_COUNT
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string
from django.views.generic.edit import UpdateView
from django.views import View
import datetime, json
from django.forms.widgets import TextInput



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
    OptionFormSet = formset_factory(OptionForm)
    ImageFormSet = formset_factory(form=ImageForm, extra=2)
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        option_formset = OptionFormSet(request.POST)
        image_formset = ImageFormSet(request.POST, request.FILES)

        if question_form.is_valid() and option_formset.is_valid() and image_formset.is_valid():
            question = Question.objects.create(statement=question_form.cleaned_data.get('statement'), test=test)
            question.save()

            for option_form in option_formset:
                try:
                    correct = True if request.POST['correct']==option_form.prefix else False
                    value = option_form.cleaned_data.get('value')
                    Option.objects.create(question=question, value=value, is_correct=correct)
                except:
                    pass
            for image_form in image_formset:
                try:
                    Image.objects.create(question=question, image=request.FILES[image_form.prefix+"-image"])
                except:
                    pass
            return HttpResponseRedirect("/tests/edit/"+str(test.pk))
               
    else:
        question_form = QuestionForm()
        option_formset = OptionFormSet()
        image_formset = ImageFormSet()
    context = {
        'question_form': question_form,
        'option_formset': option_formset,
        'image_formset': image_formset,
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
            test = Test.objects.create(title=form.cleaned_data['title'], owner=owner, duration=form.cleaned_data['duration'], time=form.cleaned_data['time'], date=form.cleaned_data['date']).save()
            #dateandtime = datetime.datetime(test.date.year, test.date.month, test.date.day, test.time.hour, test.time.minute, test.time.second)
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
    fields=["statement",]
    template_name = 'exams/editquestion.html'

    def __init__(self, *args, **kwargs):
        super(QuestionUpdate, self).__init__(*args, **kwargs)
    def get_success_url(self, **kwargs):
        return "/tests/edit/"+str(self.object.test.pk)

    def get_context_data(self, **kwargs):
        context = super(QuestionUpdate, self).get_context_data(**kwargs)
        initial = [{'value': option.value, 'correct': option.is_correct} for option in self.object.option_set.all().order_by('pk')]
        OptionFormSet = formset_factory(OptionForm, formset=BaseOptionFormSet)
        option_formset = OptionFormSet(initial=initial)
        option_formset.extra_forms.clear()
        context['option_formset'] = option_formset
        context['images'] = self.object.image_set.all()
        self.object = self.get_object()
        context['correct_option']="form-"+str(list(self.object.option_set.all().order_by("pk")).index(self.object.option_set.get(is_correct=True)))
        return context

    def post(self, request, *args, **kwargs):
        OptionFormSet = formset_factory(OptionForm, formset=BaseOptionFormSet)
        option_formset = OptionFormSet(request.POST, self.get_object())
        form = QuestionForm(request.POST)
        
        self.object = self.get_object()
        if option_formset.is_valid():
            print(int(request.POST['correct'][5:]), "form")
            old_correct = self.object.option_set.get(is_correct=True)
            new_correct = self.object.option_set.all().order_by('pk')[int(request.POST['correct'][5:])]
            print(new_correct.value)
            old_correct.is_correct = False
            new_correct.is_correct = True
            old_correct.save()
            new_correct.save()
            for oform in option_formset:
                x = self.object.option_set.all().order_by("pk")[int(oform.prefix[5:])]
                x.value = oform.cleaned_data["value"]
                x.save()

            return HttpResponseRedirect(request.path)
        else:
            form.fields["statement"].widget=TextInput()
            return render(request, "exams/editquestion.html", {'option_formset':option_formset, "form":form})
    
    def form_valid(self, form):
        OptionFormSet = formset_factory(OptionForm, formset=BaseOptionFormSet)
        option_formset = OptionFormSet(self.request.POST)
        if not option_formset.is_valid():
            return render(self.request, "exams/editquestion.html", {'option_formset':option_formset, "form":form})
        return super(QuestionUpdate, self).form_valid(form)
edit_question = QuestionUpdate.as_view()



class TestView(View):
    def get(self, request, pk, *args, **kwargs):
        student = None
        try:
            student = Student.objects.get(user=request.user)
        except:
            raise Http404
        testcode = pk
        try:
            test = Test.objects.get(pk=int(testcode))

            dateandtime = datetime.datetime(test.date.year, test.date.month, test.date.day, test.time.hour, test.time.minute, test.time.second)
            seconds_left = (dateandtime - datetime.datetime.now()).total_seconds()
            if seconds_left>0:
                return render(request, "exams/timetotest.html", {"seconds_left": seconds_left})
            response = None
            resp = TestResponse.objects.filter(student=student, test=test)
            questions = test.question_set.all()
            total_questions = questions.count()
            time_left = test.duration.total_seconds()+(dateandtime - datetime.datetime.now()).total_seconds()
            if resp.exists():
                response = resp[0]
                if response.submitted:
                    if time_left>0:
                        return HttpResponse("Your response was recorded. Check again for scores after the test is over.")
            else:
                if time_left>0:
                    response = TestResponse.objects.create(student=student, test=test)
                    for question in questions:
                        Answer.objects.create(response=response, question=question)
            if(time_left<=0):
                if response and not response.submitted:
                    for response in TestResponse.objects.filter(test=Test.objects.get(pk=test.pk)):
                        response.submitted = True
                        marks = 0
                        for ans in response.answer_set.all():
                            ans.status="locked"
                            ans.save()
                            if ans.selected_option and ans.selected_option==Option.objects.get(question=ans.question, is_correct=True):
                                marks+=1
                        response.marks = marks
                        response.save()
                return HttpResponse("This test is over. You %s." %("were Absent" if not response else "scored %d/%d marks."%(response.marks, response.answer_set.all().count())))

            data = [
                {
                    'statement': question.statement,
                    'pk': question.pk,
                    'options':[
                        {
                            'value': option.value,
                            'pk': option.pk,
                        } for option in question.option_set.all()
                    ],
                } for question in questions
            ]

            imgs = {str(question.pk):[image.image.url for image in list(question.image_set.all())] for question in questions if question.image_set.all()}

            return render(request, "exams/test.html", {"accepted": response.accepted, "images":json.dumps(imgs), "time": int(time_left),"test": test,"question_list":json.dumps(data),"questions": questions, "totalques": total_questions, "student":student, "response":response})

        except:
            return HttpResponse("Invalid Testcode!")

class MarkQuestionView(View):
    def post(self, request, *args, **kwargs):
        data = {
            "detail": "None",
        }
        if request.is_ajax():
            response_pk = int(request.POST['responsepk'])
            question_pk = int(request.POST['questionpk'])
            test_pk = int(request.POST['testpk'])
            answer = Answer.objects.get(response=TestResponse.objects.get(pk=response_pk), question=Question.objects.get(pk=question_pk))
            if answer.status!="locked":
                try:
                    selected_option=int(request.POST['selected_option'])
                    answer.selected_option = Option.objects.get(pk=selected_option)
                    selected_option=None
                except:
                    pass
                answer.status = request.POST['status']
                answer.save()
            return JsonResponse(data)
        else:
            raise Http404


class AnswerStatus(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            response_pk = int(request.POST['responsepk'])
            question_pk = int(request.POST['questionpk'])
            answer = Answer.objects.get(response=TestResponse.objects.get(pk=response_pk), question=Question.objects.get(pk=question_pk))
            selected_option="none"
            if answer.selected_option:
                selected_option=answer.selected_option.pk
            return JsonResponse({"status":answer.status, "v":answer.question.statement, "selected":selected_option})
        else:
            raise Http404

class Accepted(View):       #send ajax request to determine if the candidate opened the test for the first time
    def get(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            response = TestResponse.objects.get(pk=pk)
            response.accepted=True
            response.save()
            return JsonResponse({"detail": "accepted"})

class AssignTestView(View):
    def get(self, request, pk, *args, **kwargs):
        test, faculty = None, None
        try:
            test = Test.objects.get(pk=pk)
            faculty = Faculty.objects.get(user=request.user)
        except:
            return Http404

        add = False

        try:
            if request.GET['add']=='true':
                add=True
        except:
            pass

        context = {
            "test": test,
            "add": add,
        }
        queryset = StudyGroup.objects.all()
        new = []
        for group in queryset:
            if group not in test.groups.all():
                new.append(group.pk)
        if add:
            context["form"] = AssignForm()
            context["form"].fields["group"].queryset=queryset.filter(pk__in=new)
        return render(request, "exams/assigntest.html", context)

    def post(self, request, pk, *args, **kwargs):
        test, faculty = None, None
        try:
            test = Test.objects.get(pk=pk)
            faculty = Faculty.objects.get(user=request.user)
        except:
            return Http404

        context={
            "test": test,
            "add": True
        }

        try:
            group=StudyGroup.objects.get(pk=int(request.POST['group']))
            test.groups.add(group)
            print(group)
            return HttpResponseRedirect("/tests/assign/"+str(test.pk))
        except:
            context["form"] = AssignForm(request.POST)
            queryset = StudyGroup.objects.all()
            new = []
            for group in queryset:
                if group not in test.groups.all():
                    new.append(group.pk)
            context["form"].fields["group"].queryset=queryset.filter(pk__in=new)
            return render(request, "exams/assigntest.html", context)

class DeAssignTestView(View):
    def get(self, request, testpk, grouppk, *args, **kwargs):
        try:
            test = Test.objects.get(pk=int(testpk))
            group = StudyGroup.objects.get(pk=int(grouppk))
            faculty = Faculty.objects.get(user=request.user)
            if test not in faculty.test_set.all():
                raise Http404
            else:
                test.groups.remove(group)
        except:
            return Http404
        return HttpResponseRedirect("/tests/assign/"+testpk)

class SubmitResponseView(View):
    def get(self, request, responsepk, *args, **kwargs):
        if(request.is_ajax()):
            response = TestResponse.objects.get(pk=responsepk)
            if response and not response.submitted:
                    response.submitted = True
                    marks = 0
                    for ans in response.answer_set.all():
                        ans.status="locked"
                        ans.save()
                        if ans.selected_option and ans.selected_option==Option.objects.get(question=ans.question, is_correct=True):
                            marks+=1
                    response.marks = marks
                    response.save()
            return JsonResponse({"submitted":True})