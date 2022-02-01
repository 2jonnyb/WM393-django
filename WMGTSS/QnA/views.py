from django.shortcuts import render

# Create your views here.
def home(request):
    context = {
        #'posts': posts
    }
    return render(request, 'QnA/home.html', {})# {context})