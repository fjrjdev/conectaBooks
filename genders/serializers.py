from rest_framework import serializers

from genders.models import Gender ,Genders


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = [
            "id",
           "genders"
        ]

class GenderSerializerChoices(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    genders = serializers.ChoiceField(choices=Genders.choices , default = Genders.DEFAULT)
