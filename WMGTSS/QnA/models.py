from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    univeristy_id = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True) 
    
class Course(models.Model):
    name = models.CharField(max_length=100)

class Person(models.Model):
    courses = models.ManyToManyField(Course)

class Student(Person):
    pass

class Tutor(Person):
    pass

class Question(models.Model):
    submitted_by = models.ForeignKey(Student)
    title = models.CharField(max_length=99)
    body = models.TextField(max_length=999)


class Answer(models.Mode):
    question = models.OneToOneField(Question)
    answered_by = models.ForeignKey(Tutor)
    body = models.TextField(max_length=999)