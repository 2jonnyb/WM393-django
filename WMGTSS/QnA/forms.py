from .models import Question, Board, Answer, Like
from django.forms import ModelForm
# import models and define forms for them, django handles most of the work
class QuestionForm(ModelForm): # inherit a ModelForm for each model...
    class Meta:
        model = Question # choose a model
        fields = ['title', 'body'] # select the fields required for the form

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['course', 'name', 'tutors', 'viewers']

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['body']

class LikeForm(ModelForm):
    class Meta:
        model = Like
        fields = [] # no fields because liking is handled through a hidden field