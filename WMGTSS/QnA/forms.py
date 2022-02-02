from .models import Question, Board
from django.forms import ModelForm

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'body']

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['course', 'name', 'owner', 'tutors', 'viewers']