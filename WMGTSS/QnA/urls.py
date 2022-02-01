from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='QnA-home'),
    #path('about/', views.about, name='QnA-about'),
]