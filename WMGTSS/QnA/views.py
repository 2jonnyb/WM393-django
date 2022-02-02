from django.shortcuts import redirect, render
from .models import Board, Tutor, Profile
from .forms import BoardForm
from django.contrib import messages

# Create your views here.
def home(request):
    boards = Board.objects.all()
    context = {
        'boards':boards,
    }
    return render(request, 'QnA/home.html', context)

def create_board(request):
    if request.method == "POST":
        board_form = BoardForm(request.POST)
        if board_form.is_valid():
            board_form.instance.owner = Tutor.objects.get(pk=request.user.id)
            board_form.save()
            messages.success(request, ('Board successfully created!'))
        else:
            messages.error(request, 'Error saving form')
        return redirect('/')
    board_form = BoardForm()
    boards = Board.objects.all()
    context = {
        'boards':boards,
        'board_form':board_form
    }
    return render(request, 'QnA/board-form.html', context)