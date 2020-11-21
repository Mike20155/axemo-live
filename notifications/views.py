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

    notify = request.POST
    notif = notify.dict()
    data_type = type(notify)

    notif = Notifications(data=notif, data_type=data_type)
    notif.save()

    user_id = request.GET.get('test')
    data_type = type(user_id)

    nots = Notifications(data=user_id, data_type=data_type)
    nots.save()

    print(notify)
    return HttpResponse(status=status.HTTP_200_OK)





'https://hidden-hollows-00126.herokuapp.com/webhooks/coinbase-webhook/'