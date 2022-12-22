from django.urls import path

from rest_framework.authtoken import views

from . import views

urlpatterns = [
    path('book/', views.BookView.as_view(), name="book"),
    path('book/<pk>/', views.BookGetPacthDeleteIdView.as_view()),
    path('book/<pk>/soft', views.BookDeleteView.as_view()),
]
