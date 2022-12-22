from django.db import models

import uuid

from users.models import User


class AddressState(models.TextChoices):
    AC = "Acre"
    AL = "Alagoas"
    AM = "Amazonas"
    AP = "Amapá"
    BA = "Bahia"
    CE = "Ceará"
    DF = "Distrito Federal"
    ES = "Espírito Santo"
    GO = "Goiás"
    MA = "Maranhão"
    MG = "Minas Gerais"
    MS = "Mato Grosso do Sul"
    MT = "Mato Grosso"
    PA = "Pará"
    PB = "Paraíba"
    PE = "Pernambuco"
    PI = "Piauí"
    PR = "Paraná"
    RJ = "Rio de Janeiro"
    RN = "Rio Grande do Norte"
    RO = "Rondônia"
    RR = "Roraima"
    RS = "Rio Grande do Sul"
    SC = "Santa Catarina"
    SE = "Sergipe"
    SP = "São Paulo"
    TO = "Tocantins"
    DEFAULT = "Not Defined"


class Address(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
    )

    state = models.CharField(
        max_length=100,
        choices=AddressState.choices,
        default=AddressState.DEFAULT,
    )
    city = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )
    district = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )
    place = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )
    number = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )
    zip_code = models.CharField(
        max_length=8,
        null=False,
        blank=False,
    )
    additional_data = models.TextField(
        null=True,
        blank=True,
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="address")
