from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import ContactSerializer

from .models import Contact

class ContactViewSet(ModelViewSet):
    http_method_names = ["post", "head", "options"]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
