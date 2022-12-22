from django.db import models
import uuid


class Picture(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    picture = models.TextField(null=True, blank=True)

    book = models.ForeignKey(
        "books.Book",
        on_delete=models.CASCADE,
        related_name="picture",
        null=True,
        blank=True,
    )
    