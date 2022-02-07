from re import template
from django.shortcuts import get_object_or_404, redirect, render
from .models import Board, Tutor, Question, Like
from .forms import AnswerForm, BoardForm, QuestionForm, LikeForm
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.edit import ModelFormMixin
from django.db.models import Count, Exists, OuterRef

# Create your views here.
def home(request): # home view
    boards = Board.objects.all() # get all board objects that exist
    context = {
        'boards':boards, # add boards to context, this is a dict accessible in the template
    }
    return render(request, 'QnA/home.html', context) # render the template with the given context, serve it

def create_board(request): # board creation view
    if request.method == "POST": # if request is a post request...
        board_form = BoardForm(request.POST) # ...instantiate a new BoardForm with the data from the request
        if board_form.is_valid(): # validate the form, if valid ...
            board_form.instance.owner = Tutor.objects.get(pk=request.user.profile.tutor.id) # ...add a field to the form, the owner should be the tutor that is sending the request
            board_form.save() # save the form, create the new board object
        return redirect('/') # return the user to the homepage
    board_form = BoardForm()
    boards = Board.objects.all()
    context = { # context for template
        'boards':boards,
        'board_form':board_form,
    }
    return render(request, 'QnA/board-form.html', context) 

class SubmitQuestionView(FormView): # class based view - inherits django FormView 
    template_name = 'QnA/question-form.html' # use this template to generate response
    form_class = QuestionForm # use this form in the template
    success_url = '/' # return the user to the homepage
    slug_url_kwarg = 'board_slug' # the name of the board slug in the model- how is it referred to in the request
    def form_valid(self, form): # validate the form, if valid...
        form.instance.board = Board.objects.get(slug=self.kwargs['board_slug']) #/... get the board with the current slug
        form.instance.submitted_by = self.request.user.profile # add the profile from the request as the submitter
        form.save() # save the form, creating the new question object
        return super().form_valid(form)
    
class SubmitAnswerView(FormView): # similar to question view
    template_name = 'QnA/answer-form.html'
    form_class = AnswerForm
    success_url = '/'
    #slug_url_kwarg = 'board_slug'
    def form_valid(self, form):
        form.instance.board = Question.objects.get(slug=self.kwargs['board_slug'])
        form.instance.submitted_by = self.request.user.profile
        form.save()
        return super().form_valid(form)

class BoardView(DetailView, ModelFormMixin): # the class-based BoardView uses parts from DetailView and ModelView so the ModelFormMixin allows access to the form handling
    model = Board # what model is being detailed?
    template_name = 'QnA/board_detail.html' # what template to render?
    slug_url_kwarg = 'board_slug' 
    form_class = AnswerForm # what form is being used?
    def get_context_data(self, *args, **kwargs): # used to add context in class based views. override method to input context values.
        context = super(BoardView, self).get_context_data(*args, **kwargs) # get existing context
        # annotate allows adding temporary fields with values based on the outputs of queries
        board_questions = Question.objects.filter(board=context['board']).annotate(number_of_likes=Count('like')) # filter to only questions for this board + add a temporary field to questions in context, with how many likes each question has
        context['questions'] = board_questions.annotate(liked=Exists(Like.objects.filter(user=self.request.user.profile, question=OuterRef('pk')))) # also add a flag to say if the user has liked the question.
        return context
    def post(self, request, *args, **kwargs): # handle post requests for forms
        if request.method == 'POST':
            answer_form = AnswerForm(request.POST) # create an answer form with the request
            like_form = LikeForm(request.POST) # create a like form with the request
            if answer_form.is_valid(): # if the answer form is valid (like form wont pass)...
                answered_question = Question.objects.get(pk=int(request.POST['question_answered'])) # add field for which question the answer was for
                answer_form.instance.question = answered_question
                answer_form.instance.answered_by = request.user.profile # add field for who answered
                answer_form.save() # save form and create answer object
                Question.objects.filter(pk=int(request.POST['question_answered'])).update(answered=True) # flag the question as answered
                return redirect(request.path) # return the user to the board page
            elif like_form.is_valid(): # if the form is a like form
                answered_question = Question.objects.get(pk=int(request.POST['question_answered'])) # find the question that was liked
                existing_like = Like.objects.filter(user=request.user.profile, question=answered_question).first() # find if the user already liked the question
                if existing_like: # if the user already liked it, pressing the button should remove the like
                    existing_like.delete() # remove the like from the database
                else:
                    like_form.instance.question = answered_question # populate hidden fields
                    like_form.instance.user = request.user.profile
                    like_form.save() # save like form and create like object
                return redirect(request.path) # return to board