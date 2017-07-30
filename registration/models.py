from django.db import models
from django.contrib.auth.models import User

#############3
class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)
#############3



class StudyGroup(models.Model):
    BRANCH_CHOICES = (  
        ('CS', 'Computer Science & Engineering'),
        ('IT', 'Information Technology'),
        ('BT', 'Biotechnology'),
        ('EC', 'Electronics and Communication Engineering'),
        ('EE', 'Electrical and Electronics Engineering'),
        ('ME', 'Mechanical Engineering'),
    )
    YEAR_CHOICES = (
        ('1', '1st'),
        ('2', '2nd'),
        ('3', '3rd'),
        ('4', '4th'),
    )

    SECTION_CHOICES = (
        ('1', 'A'),
        ('2', 'B'),
    )

    NUMBER_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    )
    year = models.CharField(max_length=1, choices=YEAR_CHOICES, blank=False)
    branch = models.CharField(max_length=2, choices=BRANCH_CHOICES, blank=False)
    section = models.CharField(max_length=2, choices=SECTION_CHOICES, blank=False)
    number = models.CharField(max_length=2, choices=NUMBER_CHOICES, blank=False)


    def __str__(self):
        return self.branch+ ("E " if self.branch not in 'BT ME IT' else " ") + ['', '1st', '2nd', '3rd', '4th'][int(self.year)] + " year (G" + str(self.number) + ")" + " (Sec." + ["","A","B"][int(self.section)] + ") "
    
    class Meta:
        verbose_name_plural = "Study Groups"
        unique_together = ('number', 'section', 'year', 'branch')

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

    SECTION_CHOICES = (
        ('1', 'A'),
        ('2', 'B'),
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
    section = models.CharField(max_length=2, choices=SECTION_CHOICES)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


    def delete(self, *args, **kwargs):
        self.user.delete()
        return super(Student, self).delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Student Accounts"