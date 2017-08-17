from django.forms.formsets import formset_factory
from django.shortcuts import redirect, render, Http404, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from .forms import TestForm, BaseOptionFormSet, QuestionForm, OptionForm, ImageForm
from .models import Test, Option, Question, Image, TestResponse, Answer
from registration.models import Faculty, Student
from django.forms.formsets import INITIAL_FORM_COUNT
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string
from django.views.generic.edit import UpdateView
from django.views import View
import datetime, json


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
            print("Valid")
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
        context['images'] = self.object.image_set.all()
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



class TestView(View):
    def get(self, request, *args, **kwargs):
        student = None
        try:
            student = Student.objects.get(user=request.user)
            return render(request, "exams/entertest.html", {"student":student})
        except:
            raise Http404
        

    def post(self, request, *args, **kwargs):
        student = None
        try:
            student = Student.objects.get(user=request.user)
        except:
            raise Http404
        testcode = request.POST['testcode']
        try:
            test = Test.objects.get(pk=int(testcode))

            dateandtime = datetime.datetime(test.date.year, test.date.month, test.date.day, test.time.hour, test.time.minute, test.time.second)
            seconds_left = (dateandtime - datetime.datetime.now()).total_seconds()
            print(seconds_left)
            # if seconds_left>0:
            #     return render(request, "exams/timetotest.html", {"seconds_left": seconds_left})
            response = None
            resp = TestResponse.objects.filter(student=student, test=test)
            questions = test.question_set.all()
            total_questions = questions.count()
            if resp.exists():
                response = resp[0]
            else:
                response = TestResponse.objects.create(student=student, test=test)
                for question in questions:
                    Answer.objects.create(response=response, question=question)
            time_left = test.duration.total_seconds()+(dateandtime - datetime.datetime.now()).total_seconds()
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

            return render(request, "exams/test.html", {"images":imgs, "time": int(time_left),"test": test,"question_list":json.dumps(data),"questions": questions, "totalques": total_questions, "student":student, "response":response})

        except:
            return HttpResponse("Invalid Testcode!")

class MarkQuestionView(View):
    def post(self, request, *args, **kwargs):
        print(request.POST)
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
                    answer.status = request.POST['status']
                    selected_option=None
                except:
                    pass
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
