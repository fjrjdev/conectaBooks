from django.urls import path
from . import views


urlpatterns = [
    path("payment/<pk>/", views.Payment.as_view()),
    path("payment/<book_id>/<user_id>/", views.home, name="home"),
]
