from django.contrib.auth import logout
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from home.models import UsersData
from django.shortcuts import redirect
from .process import invest
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

                    param={'user': logged_user, 'currency': currency, 'amount': amount}

                    invest(param)

                    print('pass')
                else:
                    pass

            return redirect('dash')

        else:
            logout(request)
            return redirect('dash')

    except IndexError:
        return redirect('dash')
