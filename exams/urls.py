from django.conf.urls import url, include
from django.conf import settings
from .views import add_question, add_test, edit_test, edit_question, TestView, MarkQuestionView, AnswerStatus, Accepted, AssignTestView, DeAssignTestView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
	url(r'^add/', add_test),
	url(r'^(?P<pk>[-\w]+)/question/add/', add_question),
	url(r'^edit/question/(?P<pk>[-\w]+)/', edit_question),
	url(r'^edit/(?P<pk>[-\w]+)/', edit_test),
	url(r'^res/(?P<pk>[-\w]+)/', TestView.as_view()),
	url(r'^mark/', csrf_exempt(MarkQuestionView.as_view())),
	url(r'^status/', csrf_exempt(AnswerStatus.as_view())),
	url(r'^accepted/(?P<pk>[-\w]+)/', csrf_exempt(Accepted.as_view())),
	url(r'^assign/(?P<pk>[-\w]+)/', AssignTestView.as_view()),
	url(r'^deassign/(?P<testpk>[-\w]+)/(?P<grouppk>[-\w]+)/', DeAssignTestView.as_view()),
] 

