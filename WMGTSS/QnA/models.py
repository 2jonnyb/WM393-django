from tkinter import CASCADE
from trace import Trace
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.db.models import Count

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return(self.name)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    university_id = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True) 
    courses = models.ManyToManyField(Course, blank=True)
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
        #return(self.user.username)
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    def profile_type(self):
        if hasattr(self, 'student'):
            return self.student.__class__.__name__
        elif hasattr(self, 'tutor'):
            return self.tutor.__class__.__name__
        else:
            return self.__class__.__name__


    
class Student(Profile):
    def profile_type(self):
        return('Student')

class Tutor(Profile):
    def profile_type(self):
        return('Tutor')


class Board(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=99, blank=True)
    owner = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="owned_by_tutor", blank=True)
    tutors = models.ManyToManyField(Tutor, related_name="viewable_by_tutor")
    viewers = models.ManyToManyField(Profile, related_name="viewable_by")
    slug = models.SlugField(null=False, unique=True)
    def __str__(self):
        return(self.name)
    def get_absolute_url(self):
        return reverse('board_detail', kwargs={'board_slug': self.slug})
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    def get_all_questions(self):
        questions = self.posted_on_board.filter()
        return questions.annotate(number_of_likes=Count('like'))


class Question(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="posted_on_board")
    submitted_by = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=99)
    body = models.TextField(max_length=999)
    #likes = models.IntegerField(default=0)
    submit_date = models.DateField(auto_now_add=True)
    answered = models.BooleanField(default=False)



class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name="answer")
    answered_by = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, related_name="answered_by")
    body = models.TextField(max_length=999)
    answered_date = models.DateField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)