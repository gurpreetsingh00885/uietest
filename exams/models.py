from django.db import models
from registration.models import Faculty, Student



class Test(models.Model):
    title = models.CharField(max_length=100, blank=False)
    owner = models.ForeignKey(Faculty, blank=False)
    duration = models.DurationField(blank=False)
    date = models.DateField(blank=False)
    time = models.TimeField(blank=False)

    def __str__(self):
    	return self.title + " (by " + self.owner.name + ")"


class Question(models.Model):
	statement = models.CharField(max_length=1000, blank=False)
	test = models.ForeignKey(Test, on_delete=models.CASCADE, blank=False)
	def __str__(self):
		return self.statement[:20]+("..." if len(self.statement)>20 else "")+" ("+self.test.title+") "

class Option(models.Model):
    value = models.CharField(max_length=100, blank=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=False)
    is_correct = models.BooleanField(blank=False)


def get_image_filename(instance, filename):
    print("dlfkgl")
    return "%s/%s-%s" % (instance.user.username, filename)  



class Image(models.Model):
    question = models.ForeignKey(Question, default=None)
    image = models.ImageField(upload_to='images/%Y/%m/%d',)



class TestResponse(models.Model):
    student = models.OneToOneField(Student, default=None, on_delete=models.CASCADE, blank=False)
    test = models.OneToOneField(Test, on_delete=models.CASCADE, blank=False)

class Answer(models.Model):

    STATUS_CHOICES = ( 
        ('U', 'unanswered'),
        ('R', 'review'),
        ('L', 'locked'),
        ('N', 'not_visited'),
    )


    response = models.ForeignKey(TestResponse, default=None, on_delete=models.CASCADE, blank=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="not_visited")
    question = models.OneToOneField(Question, default=None, on_delete=models.CASCADE, blank=False)
    selected_option = models.OneToOneField(Option, on_delete=models.CASCADE, blank=True, null=True)


