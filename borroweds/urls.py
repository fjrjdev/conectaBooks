from django.urls import path

from rest_framework.authtoken import views

from . import views

urlpatterns = [
    path(
        "borrowed/<pk>/book/",
        views.BorrrowedCreateView.as_view(),
        name="borrowed",
    ),
    path(
        "borrowed/<pk>/devolution/",
        views.BorrrowedDevolutionView.as_view(),
    ),
    path(
        "borrowed/",
        views.BorrrowedListView.as_view(),
    ),
    path(
        "borrowed/<pk>/",
        views.BorrrowedDatailView.as_view(),
    ),
]
