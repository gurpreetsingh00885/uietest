from django.conf.urls import url, include

from .views import add_question, add_test, edit_test, edit_question

urlpatterns = [
	url(r'^add/', add_test),
	url(r'^(?P<pk>[-\w]+)/question/add/', add_question),
	url(r'^edit/question/(?P<pk>[-\w]+)/', edit_question),
	url(r'^edit/(?P<pk>[-\w]+)/', edit_test),
]