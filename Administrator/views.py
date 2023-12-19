from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from message.models import MessageToAdmin


# Create your views here.

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def show_all_message(request):
    messages = MessageToAdmin.objects.all()
    print(messages)
