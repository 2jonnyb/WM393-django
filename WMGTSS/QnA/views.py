from re import template
from django.shortcuts import get_object_or_404, redirect, render
from .models import Board, Tutor, Question
from .forms import BoardForm, QuestionForm
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.db.models import Count

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
    context = {
        'boards':boards,
        'board_form':board_form,
    }
    return render(request, 'QnA/board-form.html', context)

# def submit_question(request):
#     if request.method == "POST":
#         question_form = QuestionForm(request.POST)
#         if question_form.is_valid():
#             question_form.instance.board = Board.objects.get(pk=request.user.id)
#             question_form.save()
#         return redirect('/')
class SubmitQuestionView(FormView):
    template_name = 'QnA/question-form.html'
    form_class = QuestionForm
    success_url = '/'
    slug_url_kwarg = 'board_slug'
    def form_valid(self, form):
        form.instance.board = Board.objects.get(slug=self.kwargs['board_slug'])
        form.instance.submitted_by = self.request.user.profile
        form.save()
        return super().form_valid(form)

class BoardView(DetailView):
    model = Board
    template_name = 'QnA/board_detail.html'
    slug_url_kwarg = 'board_slug'

class QuestionView(DetailView):
    model = Question
    def get_object(self):
        return get_object_or_404(Question, Board__slug=self.kwargs['board_slug'], slug=self.kwargs['slug'])
