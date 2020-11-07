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

# Create your views here.


@api_view(['GET', 'POST'])
def CoinbaseNotification(request):
    """
    Retrieve, update or delete a code snippet.
    """

    if request.method == 'GET':
        page = 'notify.html'
        template = loader.get_template(page)
        context = {'user': request.user}
        return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

    if request.method == 'POST':
        notify = request.POST
        data_type = type(notify)

        notif = Notifications(data=notify, data_type=data_type)
        notif.save()

        print(notify)
        return Response(status=status.HTTP_200_OK)


