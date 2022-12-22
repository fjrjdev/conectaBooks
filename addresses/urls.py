from django.urls import path
from . import views

urlpatterns = [
    path("address/<pk>/", views.AddressDetailView.as_view(), name="address"),
]
