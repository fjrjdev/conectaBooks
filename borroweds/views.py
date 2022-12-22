from datetime import datetime as dt, timezone

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .serializers import BorrowedsSerializers, BorrowedsSerializersDevolution
from .models import Borrowed
from books.models import Book
from .permissions import isNotOwner, isNotOwnerDevolution
from utils.validation_error import CustomForbidenError


class BorrrowedCreateView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, isNotOwner]

    queryset = Borrowed.objects.all()
    serializer_class = BorrowedsSerializers

    def perform_create(self, serializer):
        book_instance = get_object_or_404(Book, id=self.kwargs["pk"])
        data_now = dt.now(timezone.utc).date()
        data = (
            dt.strptime(self.request.data["finish_date"], "%Y-%m-%d").date() - data_now
        )
        if data.days < 1:
            raise CustomForbidenError(
                f"Thats not a valid date, needs to be greater than {data_now}"
            )
        total_price = data.days * book_instance.price

        book_instance.available = False
        book_instance.save()

        data_now = dt.now(timezone.utc).date()
        data = (
            dt.strptime(self.request.data["finish_date"], "%Y-%m-%d").date() - data_now
        )
        total_price = data.days * book_instance.price

        return serializer.save(
            book=book_instance, user=self.request.user, total_price=total_price
        )



class BorrrowedDevolutionView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Borrowed.objects.all()
    serializer_class = BorrowedsSerializersDevolution

    def get_object(self):
        book_instance = get_object_or_404(Book, id=self.kwargs["pk"])

        if book_instance.available is True:
            raise CustomForbidenError("Books is available")

        book_instance.available = True

        book_instance.save()

        return book_instance


class BorrrowedListView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Borrowed.objects.all()
    serializer_class = BorrowedsSerializers


class BorrrowedDatailView(RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Borrowed.objects.all()
    serializer_class = BorrowedsSerializers
