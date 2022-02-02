from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='QnA-home'),
    path('create-board/', views.create_board, name='QnA-create-board'),
    path('boards/<slug:slug>', views.BoardView.as_view(), name='board_detail')
    #path('about/', views.about, name='QnA-about'),
]