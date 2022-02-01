from .models import Question
from django.forms import ModelForm

class Form(ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'body']