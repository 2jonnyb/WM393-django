from tkinter import CASCADE
from trace import Trace
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify

# Create your models here.
# Models are the objects in the database that django refers to.

class Course(models.Model): # Course: a university course with students and tutors, such as WM393
    name = models.CharField(max_length=200) # name is restricted to 200 characters. since there is nothing stating otherwise, there is a NOT NULL constraint on this field.
    def __str__(self):
        return(self.name) # if we refer to the string of a course object it should return the name of the course


class Profile(models.Model): # Profile: an extension of the built in django user model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile") # one to one relationship with the django built in user model
    #on_delete cascade means that when a user is deleted, so is the profile associated with it
    university_id = models.CharField(max_length=20, blank=True) # a few misc fields
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)  # date field to handle a date
    courses = models.ManyToManyField(Course, blank=True) # the courses the user is on, this a many to many relationship - many users on each course and many courses for a user
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}' # format the full name
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    def profile_type(self): # check what type of account this is, used in templates to distinguish what page should be rendered for which user
        if hasattr(self, 'student'): # if there is a child student object of this object the account is a student account.
            return self.student.__class__.__name__
        elif hasattr(self, 'tutor'): # same for tutor
            return self.tutor.__class__.__name__
        else: # will return Profile if no student or tutor child but this shouldn't be possible
            return self.__class__.__name__


    
class Student(Profile):
    pass # student and tutor child classes of profile only act to make different views.
         # rather than being a field on the profile model, having subclasses allows future work with specific methods for one type of profile.

class Tutor(Profile):
    pass


class Board(models.Model): # board model, a board is not the whole QnA board but is one page of questions for a course.
    course = models.ForeignKey(Course, on_delete=models.CASCADE) # many to one with courses, one course has many boards
    name = models.CharField(max_length=99, blank=True)
    owner = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="owned_by_tutor", blank=True) # the user that made the board
    tutors = models.ManyToManyField(Tutor, related_name="viewable_by_tutor") # tutors that can answer questions
    viewers = models.ManyToManyField(Profile, related_name="viewable_by") # users that can view questions and answers
    slug = models.SlugField(null=False, unique=True) # slug used in url - unique slug based on name to go in url
    def __str__(self):
        return(self.name)
    def get_absolute_url(self): # get the whole url with the slug to make links
        return reverse('board_detail', kwargs={'board_slug': self.slug})
    def save(self, *args, **kwargs): # when a board is created, make the slug the name
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class Question(models.Model): # a question on a board
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="posted_on_board") # many to one - what board is it posted on
    submitted_by = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True) # who asked? displayed in view
    title = models.CharField(max_length=99)
    body = models.TextField(max_length=999)
    submit_date = models.DateField(auto_now_add=True) # date submitted, is added as the current time when it is instantiated
    answered = models.BooleanField(default=False) # is the question answered? used to determine if an answer box is needed and if students can see question


class Answer(models.Model): # answer to a question
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name="answer") # one to one - each question and answer have a corresponding counterpart
    answered_by = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, related_name="answered_by") # who answered?
    body = models.TextField(max_length=999)
    answered_date = models.DateField(auto_now_add=True)

class Like(models.Model): # representation of a like, for liking questions. must be done as a model to track who has liked what. otherwise a user could like a question multiple times
    user = models.ForeignKey(Profile, on_delete=models.CASCADE) # who performed the like?
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # what did they like?