from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator


class FeedBack(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    stars_owner = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        null=True,
    )
    stars_renter = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        null=True,
    )
    rating_owner = models.TextField(null=True, blank=True)
    rating_renter = models.TextField(null=True, blank=True)
    borrowed = models.OneToOneField(
        "borroweds.Borrowed",
        on_delete=models.CASCADE,
        related_name="feed_back",
    )
