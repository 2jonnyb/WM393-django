from re import template
from django.shortcuts import redirect, render
from .models import Board, Tutor, Question
from .forms import BoardForm, QuestionForm
from django.views.generic.detail import DetailView

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
        return redirect('create-board/')
    board_form = BoardForm()
    boards = Board.objects.all()
    questions = Board
    context = {
        'boards':boards,
        'board_form':board_form,
    }
    return render(request, 'QnA/board-form.html', context)

def submit_question(request):
    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question_form.instance.board = Board.objects.get(pk=request.user.id)
            question_form.save()
        return redirect('/')

class BoardView(DetailView):
    model = Board
    template_name = 'QnA/board_detail.html'