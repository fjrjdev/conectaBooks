from rest_framework import serializers
from borroweds.serializers import BorrowedsSerializers
from django.core.validators import MinValueValidator, MaxValueValidator
from feed_back.models import FeedBack


class PostFeedBackOwnerSerializers(serializers.ModelSerializer):
    borrowed = BorrowedsSerializers(read_only=True)
    stars_owner = serializers.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    rating_owner = serializers.CharField()

    class Meta:
        model = FeedBack
        fields = [
            "id",
            "borrowed",
            "stars_renter",
            "rating_renter",
            "stars_owner",
            "rating_owner",
        ]
        read_only_fields = [
            "stars_renter",
            "rating_renter",
        ]


class PostFeedBackRenterSerializers(serializers.ModelSerializer):
    borrowed = BorrowedsSerializers(read_only=True)
    stars_renter = serializers.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    rating_renter = serializers.CharField()

    class Meta:
        model = FeedBack
        fields = [
            "id",
            "borrowed",
            "stars_owner",
            "rating_owner",
            "stars_renter",
            "rating_renter",
        ]
        read_only_fields = [
            "stars_owner",
            "rating_owner",
        ]


class GetOrUpdateFeedBackSerializers(serializers.ModelSerializer):
    borrowed = BorrowedsSerializers(read_only=True)

    class Meta:
        model = FeedBack
        fields = [
            "id",
            "borrowed",
            "stars_owner",
            "stars_renter",
            "rating_owner",
            "rating_renter",
        ]
