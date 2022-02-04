from .models import Question, Board, Answer
from django.forms import ModelForm

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'body']

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['course', 'name', 'tutors', 'viewers']

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['body']