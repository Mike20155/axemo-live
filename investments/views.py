from django.http import HttpResponse
from rest_framework import status
from django.contrib.auth import logout
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from home.models import UsersData
from django.shortcuts import redirect
from .process import invest
import time
from django.template import loader
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from crypto_transactions.models import History
from django.shortcuts import redirect
import time


# Create your views here.


@api_view(['POST'])
def confirm_investment(request):
    try:
        request.session['session_timeout'] = time.time() + 60000000
        if request.session['session_timeout'] > time.time():
            print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
            request.session['session_timeout'] = time.time() + 60000000

            logged_user = User.objects.get(username=request.user)

            user = UsersData.objects.get(user=logged_user)

            data = request.POST

            currency = data['currency']
            amount = float(data['amount'])

            if User.objects.get(username=user):
                user = User.objects.get(username=user)
                user = UsersData.objects.get(user=user)
                balance = 0.00

                if currency == 'BTC':
                    balance = float(user.bitcoin_balance)

                elif currency == 'ETH':
                    balance = float(user.etherum_balance)

                elif currency == 'LTC':
                    balance = float(user.litecoin_balance)

                elif currency == 'BCH':
                    balance = float(user.bitcoin_cash_balance)

                if balance >= float(amount):

                    param = {'user': logged_user, 'currency': currency, 'amount': amount}

                    invest(param)

                    page = 'pages/dashboard.html'
                    template = loader.get_template(page)

                    context = {'status': 'success',
                               'message': f'Congratulations! you have successfully invested {currency}{balance}'}
                    return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

                else:
                    page = 'pages/dashboard.html'
                    template = loader.get_template(page)

                    context = {'status': 'failed', 'message': f'insufficient funds in currency requested.'
                                                              f'you have only {currency}{balance} available in your '
                                                              f'{currency} wallet'}
                    return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

        else:
            logout(request)
            page = 'pages/login.html'
            template = loader.get_template(page)
            context = {'timeout': f'session timeout! please log in again to continue'}
            return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

    except Exception as e:
        logout(request)
        page = 'pages/login.html'
        template = loader.get_template(page)
        context = {'message': f'something went wrong while trying to process your request, please try again later.'}
        return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)
