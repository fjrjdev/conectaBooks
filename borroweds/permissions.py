from rest_framework import permissions
from django.shortcuts import get_object_or_404
from books.models import Book
from utils.validation_error import CustomForbidenError


class isNotOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        book_instance = get_object_or_404(Book, id=view.kwargs["pk"])
        if book_instance.available is False:
            raise CustomForbidenError("This book is not available")
        if not book_instance.user.id == request.user.id:
            return True
        
class isNotOwnerDevolution(permissions.BasePermission):
    def has_permission(self, request, view):
        book_instance = get_object_or_404(Book, id=view.kwargs["pk"])
        
        if not book_instance.user.id == request.user.id:
            return True
