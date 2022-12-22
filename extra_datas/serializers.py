from rest_framework import serializers

from .models import Extra_Data


class Extra_DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extra_Data

        fields = "__all__"

        extra_kwargs = {
            "id": {
                "read_only": True,
            },
            "book": {
                "read_only": True,
            },
        }
