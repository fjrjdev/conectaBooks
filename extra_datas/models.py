from django.db import models

import uuid


class Extra_Data(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
    )

    additional_data = models.TextField(
        null=True,
        blank=True,
        default=None,
    )
    translater = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    translated = models.BooleanField(
        default=False,
    )

    book = models.OneToOneField(
        "books.Book",
        on_delete=models.CASCADE,
        related_name="extra_data",
    )
