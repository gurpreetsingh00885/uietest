from django.db import models
from django.contrib.auth.models import User

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=50)

class Student(models.Model):
    YEAR_CHOICES = (
        ('1', '1st'),
        ('2', '2nd'),
        ('3', '3rd'),
        ('4', '4th'),
    )

    BRANCH_CHOICES = (  
        ('CS', 'Computer Science & Engineering'),
        ('IT', 'Information Technoology'),
        ('BT', 'Biotechnology'),
        ('EC', 'Electronics and Communication Engineering'),
        ('EE', 'Electrical and Electronics Engineering'),
        ('ME', 'Mechanical Engineering'),
    )
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=8)
    phone_no = models.CharField(max_length=10)
    year = models.CharField(max_length=1, choices=YEAR_CHOICES)
    branch = models.CharField(max_length=2, choices=YEAR_CHOICES)