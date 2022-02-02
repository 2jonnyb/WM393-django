from django.shortcuts import redirect, render
from .models import Board
from .forms import BoardForm
from django.contrib import messages

# Create your views here.
def home(request):
    if request.method == "POST":
        board_form = BoardForm(request.POST)
        if board_form.is_valid():
            board_form.save()
            messages.success(request, ('Board successfully created!'))
        else:
            messages.error(request, 'Error saving form')
        return redirect('#')
    board_form = BoardForm()
    boards = Board.objects.all()
    context = {
        'boards':boards,
        'board_form':board_form
    }
    return render(request, 'QnA/home.html', context)