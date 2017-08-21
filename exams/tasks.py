from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import TestResponse, Test, Option

@shared_task
def SubmitResponse(testpk):
	for test in TestResponse.objects.filter(test=Test.objects.get(pk=testpk)):
		test.submitted = True
		marks = 0
		for ans in test.answer_set.all():
			ans.status="locked"
			ans.save()
			if ans.selected_option is not None and ans.selected_option==Option.objects.get(question=ans.question, is_correct=True):
				marks+=1
		test.marks = marks
		test.save()
