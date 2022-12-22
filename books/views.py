from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.views import Response, status

from .models import Book
from .serializers import (
    BookPostSerializer,
    BookGetUpdateSerializer,
    BookDeleteSerializer,
)
from genders.models import Gender
from users.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from extra_datas.models import Extra_Data
from .permissions import IsAdmOrOwnerBook
from utils.validation_error import CustomForbidenError
from extra_datas.serializers import Extra_DataSerializer
from genders.serializers import GenderSerializer


# Create your views here.
class BookView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Book.objects.all()
    serializer_class = BookPostSerializer

    def perform_create(self, serializer):
        if "genders" not in self.request.data.keys():
            raise CustomForbidenError({"genders": ["This camp is required."]})

        if "extra_data" not in self.request.data.keys():
            raise CustomForbidenError({"extra_data": ["This camp is required."]})

        book = serializer.save(user=self.request.user)

        extra = self.request.data.pop("extra_data")

        extraSerializer = Extra_DataSerializer(data=extra)
        extraSerializer.is_valid(raise_exception=True)

        Extra_Data.objects.create(**extra, book=book)

        genders = self.request.data.pop("genders")

        for item in genders:
            genderSerializer = GenderSerializer(data=item)
            genderSerializer.is_valid(raise_exception=True)

            gender, _ = Gender.objects.get_or_create(**item)
            book.genders.add(gender)


class BookGetPacthDeleteIdView(RetrieveUpdateDestroyAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmOrOwnerBook]

    queryset = Book.objects.all()
    serializer_class = BookGetUpdateSerializer

    def perform_create(self, *args, **kwargs):
        book = self.get_object()

        if "extra_data" in self.request.data.keys():
            extra = self.request.data.pop("extra_data")
            extraSerializer = Extra_DataSerializer(data=extra)
            extraSerializer.is_valid(raise_exception=True)

            Extra_Data.objects.update(**extra)

        if "genders" in self.request.data.keys():
            genders = self.request.data.pop("genders")
            book.genders.clear()

            for item in genders:
                genderSerializer = GenderSerializer(data=item)
                genderSerializer.is_valid(raise_exception=True)
                gender, _ = Gender.objects.get_or_create(**item)
                book.genders.add(gender)

        return super().get_serializer(*args, **kwargs)


class BookDeleteView(UpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmOrOwnerBook]

    queryset = Book.objects.all()
    serializer_class = BookDeleteSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(status=status.HTTP_204_NO_CONTENT)
