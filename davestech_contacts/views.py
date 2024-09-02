from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import ContactSerializer
from django.core.mail import send_mail
import logging

logger=logging.getLogger(__name__)


from .models import Contact

class ContactViewSet(ModelViewSet):
    http_method_names = ["post", "head", "options"]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        try:
            email_from = 'dave@davestechnicalservices.com'
            email_to = [request.data['email'], 'dave@davestechnicalservices.com']
            subject = 'Contact from davestechnicalservices.com'
            message = request.data['message']
            send_mail(subject, message, email_from, email_to, fail_silently=False)
        except Exception as e:
            logger.debug(type(e))
            logger.debug(e)            

        return super().create(request, *args, **kwargs)