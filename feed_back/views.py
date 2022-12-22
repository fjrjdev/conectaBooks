from rest_framework import generics
from rest_framework.views import Response, status, APIView, Request
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from borroweds.models import Borrowed
from feed_back.models import FeedBack
from books.models import Book
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from feed_back.serializers import (
    GetOrUpdateFeedBackSerializers,
    PostFeedBackOwnerSerializers,
    PostFeedBackRenterSerializers,
)
from users.models import User


class PostFeedBack(APIView):
    queryset = FeedBack
    serializer_class = PostFeedBackRenterSerializers

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request: Request, borrowed_id) -> Response:
        borrowed = get_object_or_404(Borrowed, id=borrowed_id)
        feed_back = FeedBack.objects.filter(borrowed=borrowed.id)
        serializer = ""
        if request.user.id == borrowed.book.user.id:
            serializer = PostFeedBackOwnerSerializers
        elif request.user.id == borrowed.user.id:
            serializer = PostFeedBackRenterSerializers
        else:
            return Response(
                {
                    "message": "you can only post the feedback if you are the owner or renter of the book"
                },
                status.HTTP_401_UNAUTHORIZED,
            )
        if feed_back:
            feed = FeedBack.objects.get(borrowed=borrowed.id)
            if serializer == PostFeedBackOwnerSerializers and (
                feed.stars_owner or feed.rating_owner
            ):
                return Response(
                    {"msg": "you already replied to the feed Back"},
                    status.HTTP_400_BAD_REQUEST,
                )
            elif serializer == PostFeedBackRenterSerializers and (
                feed.stars_renter or feed.rating_renter
            ):
                return Response(
                    {"msg": "you already replied to the feed Back"},
                    status.HTTP_400_BAD_REQUEST,
                )
            Serializer = serializer(
                feed,
                data=request.data,
                partial=True,
            )
            Serializer.is_valid(raise_exception=True)
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED)
        elif not feed_back:
            Serializer = serializer(data=request.data)
            Serializer.is_valid(raise_exception=True)
            Serializer.save(borrowed=borrowed)
            return Response(Serializer.data, status=status.HTTP_201_CREATED)


class GetFeedBack(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = GetOrUpdateFeedBackSerializers
    queryset = FeedBack.objects.all()


class GetUserFeedBack(APIView):
    queryset = FeedBack
    serializer_class = GetOrUpdateFeedBackSerializers

    def get(self, request: Request, user_id) -> Response:
        user = get_object_or_404(User, id=self.kwargs["user_id"])
        borrowed = Borrowed.objects.filter(user=user.id)
        data = []
        for keys in borrowed:
            try:
                feed_back = FeedBack.objects.get(borrowed=keys.id)
                data.append(feed_back)
            except ObjectDoesNotExist:
                pass
        serializer = GetOrUpdateFeedBackSerializers(data=data, many=True)
        serializer.is_valid()
        return Response(serializer.data)


class GetBookFeedBack(APIView):
    queryset = FeedBack
    serializer_class = GetOrUpdateFeedBackSerializers

    def get(self, request: Request, book_id) -> Response:
        book = get_object_or_404(Book, id=self.kwargs["book_id"])
        borrowed = Borrowed.objects.filter(book=book.id)
        data = []
        for keys in borrowed:
            try:
                feed_back = FeedBack.objects.get(borrowed=keys.id)
                data.append(feed_back)
            except ObjectDoesNotExist:
                pass
        serializer = GetOrUpdateFeedBackSerializers(data=data, many=True)
        serializer.is_valid()
        return Response(serializer.data)


class GetFeedBackDatail(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = GetOrUpdateFeedBackSerializers
    queryset = FeedBack.objects.all()
