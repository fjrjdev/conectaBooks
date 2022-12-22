from rest_framework import serializers
from borroweds.models import Borrowed


class BorrowedsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Borrowed
        fields = [
            "id",
            "initial_date",
            "finish_date",
            "shipping_method",
            "user_id",
            "book_id",
            "total_price"
        ]
        read_only_fields = [
            "id",
            "total_price"
            "initial_date",
            "user_id",
            "book_id"
        ]
        
class BorrowedsSerializersDevolution(serializers.ModelSerializer):
    class Meta:
        model = Borrowed
        fields = [
            "id",
            "user_id",
            "book_id",
        ]
        read_only_fields = [
            "id",
            "initial_date",
            "finish_date",
            "initial_date",
            "shipping_method",
            "user_id",
            "book_id"
        ]
