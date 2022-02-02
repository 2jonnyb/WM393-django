from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='QnA-home'),
    path('create-board/', views.create_board, name='QnA-create-board')
    #path('about/', views.about, name='QnA-about'),
]