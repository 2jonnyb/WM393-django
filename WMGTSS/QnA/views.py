from re import template
from django.shortcuts import get_object_or_404, redirect, render
from .models import Board, Tutor, Question, Like
from .forms import AnswerForm, BoardForm, QuestionForm, LikeForm
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.edit import ModelFormMixin
from django.db.models import Count, Exists, OuterRef

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
        return redirect('/')
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
    
class SubmitAnswerView(FormView):
    template_name = 'QnA/answer-form.html'
    form_class = AnswerForm
    success_url = '/'
    #slug_url_kwarg = 'board_slug'
    def form_valid(self, form):
        form.instance.board = Question.objects.get(slug=self.kwargs['board_slug'])
        form.instance.submitted_by = self.request.user.profile
        form.save()
        return super().form_valid(form)

class BoardView(DetailView, ModelFormMixin):
    model = Board
    template_name = 'QnA/board_detail.html'
    slug_url_kwarg = 'board_slug'
    form_class = AnswerForm
    def liked_by_current_user(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        return question.like_set.filter(user=request.user.profile) and True or False
    def get_context_data(self, *args, **kwargs):
        context = super(BoardView, self).get_context_data(*args, **kwargs)
        board_questions = Question.objects.filter(board=context['board']).annotate(number_of_likes=Count('like'))
        context['questions'] = board_questions.annotate(liked=Exists(Like.objects.filter(user=self.request.user.profile, question=OuterRef('pk'))))
        return context
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            answer_form = AnswerForm(request.POST)
            like_form = LikeForm(request.POST)
            if answer_form.is_valid():
                answered_question = Question.objects.get(pk=int(request.POST['question_answered']))
                answer_form.instance.question = answered_question
                answer_form.instance.answered_by = request.user.profile
                answer_form.save()
                Question.objects.filter(pk=int(request.POST['question_answered'])).update(answered=True)
                return redirect(request.path)
            elif like_form.is_valid():
                answered_question = Question.objects.get(pk=int(request.POST['question_answered']))
                existing_like = Like.objects.filter(user=request.user.profile, question=answered_question).first()
                if existing_like:
                    existing_like.delete()
                else:
                    like_form.instance.question = answered_question
                    like_form.instance.user = request.user.profile
                    like_form.save()
                return redirect(request.path)


class QuestionView(DetailView):
    model = Question
    def get_object(self):
        return get_object_or_404(Question, Board__slug=self.kwargs['board_slug'], slug=self.kwargs['slug'])
