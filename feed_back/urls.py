from django.urls import path

from . import views

urlpatterns = [
    path(
        "feedback/<str:borrowed_id>/borrowed/",
        views.PostFeedBack.as_view(),
    ),
    path(
        "feedback/",
        views.GetFeedBack.as_view(),
    ),
    path(
        "feedback/<str:user_id>/user/",
        views.GetUserFeedBack.as_view(),
    ),
    path(
        "feedback/<str:book_id>/book/",
        views.GetBookFeedBack.as_view(),
    ),
    path(
        "feedback/<pk>/",
        views.GetFeedBackDatail.as_view(),
    ),
]
