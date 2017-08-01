from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Test(models.Model):
    title = models.CharField(max_length=100, blank=False)
    owner = models.OneToOneField(User, blank=False)
    question = models.CharField(max_length=1000, blank=False)


class Option(models.Model):
    value = models.CharField(max_length=100, blank=False)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, blank=False)