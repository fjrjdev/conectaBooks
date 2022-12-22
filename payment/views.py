from django.shortcuts import render
import uuid
from django.contrib import messages
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from rest_framework.views import APIView, Request, Response, status
from books.models import Book
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from borroweds.permissions import isNotOwner


def home(request, book_id, user_id):
    book = get_object_or_404(Book, id=book_id)
    host = request.get_host()
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": book.price,
        "item_name": book.title,
        "invoice": str(uuid.uuid4()),
        "currency_code": "USD",
        "notify_url": f'http://{host} { reverse("paypal-ipn")}',
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "home.html", context)


class Payment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, pk) -> Response:
        host = request.get_host()
        book = get_object_or_404(Book, id=pk)
        if book.available is False:
            return Response(
                {"mensagem": "This book is not available"},
                status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"payment link": f"http://{host}/payment/{pk}/{request.user.id}/"}
        )
