from django.http import HttpResponse
from rest_framework import status
from django.template import loader
from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import Notifications
from django.shortcuts import redirect
from crypto_transactions.models import History
import time
import hashlib
import datetime
import json

# Create your views here.


@api_view(['GET', 'POST'])
def CoinbaseNotification(request):
    """
    Retrieve, update or delete a code snippet.
    """

    if request.method == 'GET':
        return Response({'hey': 'get'})


    if request.method == 'POST':
        notify = request.POST
        notify = notify.dict()
        data_type = type(notify)

        notif = Notifications(data=notify, data_type=data_type)
        notif.save()

        print(notify)
        return HttpResponse(status=status.HTTP_200_OK)




'https://hidden-hollows-00126.herokuapp.com/webhooks/coinbase-webhook/'