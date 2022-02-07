from django.urls import path
from . import views


urlpatterns = [ # this list serves as a lookup for the user. the url is the the first term and the served view is the second
    path('', views.home, name='QnA-home'), # the homepage, for the url that is just the site url
    path('create-board/', views.create_board, name='QnA-create-board'), # board creation url
    path('boards/<slug:board_slug>/submit-question', views.SubmitQuestionView.as_view(), name='QnA-question'), # submit question url
    path('boards/<slug:board_slug>', views.BoardView.as_view(), name='board_detail')] # urls for boards. the slug part makes a unique view for each board with the board's name in the url