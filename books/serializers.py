from rest_framework import serializers

# from borroweds.serializers import BorrowedsSerializers
from extra_datas.serializers import Extra_DataSerializer
from genders.serializers import GenderSerializer,GenderSerializerChoices
from extra_datas.serializers import Extra_DataSerializer

from books.models import Book


class BookPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book

        fields = [
            "id",
            "title",
            "transaction",
            "available",
            "author",
            "year",
            "price",
            "language",
            "publishing",
            "condition",
            "isbn",
            "genders",
            "user",
            "extra_data",
        ]

        extra_kwargs = {
            "id": {"read_only": True},
            "genders": {"read_only": True},
            "user": {"read_only": True},
            "extra_data": {"read_only": True},
        }

    extra_data = Extra_DataSerializer(read_only=True)
    genders = GenderSerializer(many=True,read_only=True)


class BookGetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "transaction",
            "available",
            "author",
            "price",
            "language",
            "publishing",
            "condition",
            "isbn",
            "extra_data",
            "genders",
        ]

        extra_kwargs = {
            "id": {"read_only": True},
            "genders": {"read_only": True},
            "extra_data": {"read_only": True},
            
        }

        # borrowed = BorrowedsSerializers(many=True)
        extra_data = Extra_DataSerializer(many=True)
        genders = GenderSerializer(many=True)


class BookDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book

        fields = "__all__"

        read_only_fields = [
            "id",
            "title",
            "transaction",
            "price",
            "available",
            "author",
            "year",
            "language",
            "publishing",
            "condition",
            "isbn",
            "extra_data",
            "user",
            "genders",
            # "borrowed"
        ]
        extra_kwargs = {
            "isActive": {"required": True},
        }
