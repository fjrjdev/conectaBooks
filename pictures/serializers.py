from rest_framework import serializers

from .models import Picture


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = [
            "id",
            "picture",
            "book"
        ]
        read_only_fields = [
            "id",
        ]
        depth = 1
