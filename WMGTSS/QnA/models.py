from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return(self.name)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university_id = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True) 
    courses = models.ManyToManyField(Course, blank=True)
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
        #return(self.user.username)

    
class Student(Profile):
    pass


class Tutor(Profile):
    pass


class Board(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=99, blank=True)
    owner = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="owned_by_tutor", blank=True)
    tutors = models.ManyToManyField(Tutor, related_name="viewable_by_tutor")
    viewers = models.ManyToManyField(Profile)
    slug = models.SlugField(null=False, unique=True)
    def __str__(self):
        return(self.name)
    def get_absolute_url(self):
        return reverse('board_detail', kwargs={'slug': self.slug})
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Question(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=99)
    body = models.TextField(max_length=999)
    likes = models.IntegerField()
    submit_date = models.DateField()

class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    answered_by = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)
    body = models.TextField(max_length=999)
    answered_date = models.DateField()
