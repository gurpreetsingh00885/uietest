from django.db import models
from registration.models import Faculty



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