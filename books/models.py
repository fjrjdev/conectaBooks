from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator


class Transaction(models.TextChoices):
    SALE = "Sale"
    LOCATION = "Location"


class Language(models.TextChoices):
    PORTUGUESE = "Portuguese"
    ENGLISH = "English"


class Book(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    title = models.TextField()
    transaction = models.CharField(
        max_length=10, choices=Transaction.choices, default=Transaction.LOCATION
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)
    author = models.CharField(max_length=100)
    year = models.CharField(max_length=4)
    language = models.CharField(
        max_length=10, choices=Language.choices, default=Language.ENGLISH
    )
    publishing = models.CharField(max_length=254)
    condition = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    isbn = models.CharField(max_length=13)
    isActive = models.BooleanField(default=True)

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="book",
    )
    genders = models.ManyToManyField(
        "genders.Gender",
        related_name="book",
    )
