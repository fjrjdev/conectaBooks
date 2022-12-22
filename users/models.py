from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from feed_back.models import  FeedBack
from borroweds.models import Borrowed
from books.models import Book   
import uuid

from borroweds.models import Borrowed


class User(AbstractUser):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
    )

    avatar = models.TextField(
        null=True,
        blank=True,
        default=None,
    )
    email = models.EmailField()
    birth = models.DateField()
    stars = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=5,
        editable=False,
    )

    REQUIRED_FIELDS = [
        "email",
        "birth",
    ]

    def get_nota(self)-> str:
        
        valores = []
        for e in FeedBack.objects.all():
            valores.append(e)
       
        notas=[]
        
        for item in valores:
            nota = Borrowed.objects.get(feed_back = item)
            feed = FeedBack.objects.get(id = item.id)
            book = Book.objects.get(id = feed.borrowed.book_id)
            if feed.borrowed.user_id == self.id:  
                if feed.stars_renter != None:
                    notas.append(feed.stars_renter)

            
            if book.user_id == self.id:
                if feed.stars_owner != None:
                    notas.append(feed.stars_owner)
        notafinal = 5
        if  len(notas)> 0:
            notafinal =0
            for numero in notas:
                notafinal += numero
       
            notafinal = notafinal/len(notas)
        
        return notafinal