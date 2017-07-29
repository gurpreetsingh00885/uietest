from django.db import models
from django.contrib.auth.models import User

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Faculty Accounts"

class Student(models.Model):
    YEAR_CHOICES = (
        ('1', '1st'),
        ('2', '2nd'),
        ('3', '3rd'),
        ('4', '4th'),
    )

    BRANCH_CHOICES = (  
        ('CS', 'Computer Science & Engineering'),
        ('IT', 'Information Technology'),
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
    branch = models.CharField(max_length=2, choices=BRANCH_CHOICES)
    created = models.DateField(auto_now_add = True)
    def __str__(self):
        return self.name


    def delete(self, *args, **kwargs):
        self.user.delete()
        return super(Student, self).delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Student Accounts"