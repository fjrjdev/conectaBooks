from django.shortcuts import render

from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import RetrieveUpdateAPIView

from .models import Address
from addresses.serializers import AddressDetailSerializer
from .permissions import isOwner


class AddressDetailView(RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [isOwner]

    queryset = Address.objects.all()

    serializer_class = AddressDetailSerializer

    lookup_field = 'user'
    lookup_url_kwarg = 'pk'