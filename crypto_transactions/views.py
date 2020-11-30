from django.http import HttpResponse
from rest_framework import status
from django.template import loader
from .process import coinbase, luno, local, get_address, bal_converter
from django.contrib.auth import logout
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from home.models import UsersData
from .models import Address
from django.shortcuts import redirect
from crypto_transactions.models import History
import time
import hashlib
import datetime
from home.process import fiat_calculator, bal_converter

# Create your views here.


@api_view(['GET', 'POST'])
def crypto(request, currency):
    try:
        request.session['session_timeout'] = time.time() + 60000000
        if request.session['session_timeout'] > time.time():
            print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
            request.session['session_timeout'] = time.time() + 60000000

            page = 'pages/accounts.html'
            template = loader.get_template(page)

            logged_user = User.objects.get(username=request.user)

            user = UsersData.objects.get(user=logged_user)

            btc = float(user.bitcoin_balance)
            eth = float(user.etherum_balance)
            ltc = float(user.litecoin_balance)
            bch = float(user.bitcoin_cash_balance)
            ngn = bal_converter(str(user.local_currency_balance))

            hist = History.objects.get(user=logged_user)
            print('*'*500)
            history = []
            symbol = None
            balance = 0.00
            if currency == 'BITCOIN':
                balance = fiat_calculator(btc, 0, 0, 0)
                for h, i in eval(hist.btc_history).items():
                    history.append(i)
                    symbol = 'BTC'

            elif currency == 'ETHERUM':
                balance = fiat_calculator(0, eth, 0, 0)
                for h, i in eval(hist.eth_history).items():
                    history.append(i)
                    symbol = 'ETH'

            elif currency == 'LITECOIN':
                balance = fiat_calculator(0, 0, ltc, 0)
                for h, i in eval(hist.ltc_history).items():
                    history.append(i)
                    symbol = 'LTC'

            elif currency == 'BITCOINCASH':
                balance = fiat_calculator(0, 0, 0, bch)
                for h, i in eval(hist.bch_history).items():
                    history.append(i)
                    symbol = 'BCH'

            elif currency == 'NAIRA':
                for h, i in eval(hist.ngn_history).items():
                    history.append(i)
                    symbol = 'NGN'

            balance = str("{:.1f}".format(balance))
            btc = str("{:.8f}".format(btc))
            eth = str("{:.8f}".format(eth))
            ltc = str("{:.8f}".format(ltc))
            bch = str("{:.8f}".format(bch))

            balance = bal_converter(balance)

            request.session['currency'] = currency
            history.reverse()
            trans = True
            if len(history) == 0:
                trans = False
            print('pass')
            context = {'btc': btc, 'eth': eth, 'ltc': ltc, 'bch': bch, 'local': ngn, 'fiat': balance,
                       'currency': currency.capitalize(), 'history': history, 'trans': trans, 'symbol': symbol}
            return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

        else:
            logout(request)
            return redirect('login')

    except Exception as e:
        print(e)
        logout(request)
        return redirect('login')


@api_view(['GET'])
def receive(request):
    try:
        if request.session['session_timeout'] > time.time():
            print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
            request.session['session_timeout'] = time.time() + 600

            currency = request.session['currency']

            page = 'pages/adress.html'

            template = loader.get_template(page)

            address = get_address(request.user, currency)
            qr = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={address}"

            context = {'address': address, 'source': qr, 'currency': currency.capitalize(), 'c': currency}

            return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

        else:
            logout(request)
            return redirect('login')

    except Exception as e:
        page = 'pages/accounts.html'
        template = loader.get_template(page)

        logged_user = User.objects.get(username=request.user)

        user = UsersData.objects.get(user=logged_user)

        btc = float(user.bitcoin_balance)
        eth = float(user.etherum_balance)
        ltc = float(user.litecoin_balance)
        bch = float(user.bitcoin_cash_balance)
        ngn = bal_converter(str(user.local_currency_balance))

        hist = History.objects.get(user=logged_user)
        print('*' * 500)
        history = []
        symbol = None
        currency = request.session['currency']
        if currency == 'BITCOIN':
            for h, i in eval(hist.btc_history).items():
                history.append(i)
                symbol = 'BTC'
        elif currency == 'ETHERUM':
            for h, i in eval(hist.eth_history).items():
                history.append(i)
                symbol = 'ETH'
        elif currency == 'LITECOIN':
            for h, i in eval(hist.ltc_history).items():
                history.append(i)
                symbol = 'LTC'
        elif currency == 'BITCOINCASH':
            for h, i in eval(hist.bch_history).items():
                history.append(i)
                symbol = 'BCH'
        elif currency == 'NAIRA':
            for h, i in eval(hist.ngn_history).items():
                history.append(i)
                symbol = 'NGN'

        request.session['currency'] = currency
        history.reverse()
        context = {'btc': btc, 'eth': eth, 'ltc': ltc, 'bch': bch, 'local': ngn,
                   'currency': currency.capitalize(), 'history': history, 'symbol': symbol,
                   'status': 'failed', 'message': f'something went wrong. please try again later'}

        return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
def check(request):
    try:
        if request.method == 'POST':
            try:
                if request.session['session_timeout'] > time.time():
                    print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
                    request.session['session_timeout'] = time.time() + 1000

                    pin = str(request.POST.get('pin' ''))

                    user = User.objects.get(username=request.user)
                    user = UsersData.objects.get(user=user)

                    if hashlib.sha256(pin.encode()).hexdigest() == str(user.pin):

                        try:
                            platform = request.POST.get('platform' '')
                            to = request.POST.get('destination' '')
                            amount = request.POST.get('amount' '')
                            # desc = request.POST.get('desc' '')
                            print(request.POST)

                            btc = float(user.bitcoin_balance)
                            eth = float(user.etherum_balance)
                            ltc = float(user.litecoin_balance)
                            bch = float(user.bitcoin_cash_balance)

                            balance = 0.00

                            if request.session['currency'] == 'BITCOIN':
                                balance = btc
                            elif request.session['currency'] == 'ETHERUM':
                                balance = eth
                            elif request.session['currency'] == 'LITECOIN':
                                balance = ltc
                            elif request.session['currency'] == 'BITCOINCASH':
                                balance = bch

                            print(float(balance))
                            print(float(amount))

                            if len(to) > 0:
                                if len(amount) > 0:
                                    if float(balance) >= float(amount):

                                        print('FORM IS VALID')

                                        currency = request.session['currency']

                                        current_time = datetime.datetime.now()
                                        time_now = str(current_time)[:16]

                                        context = {'to': to, 'amount': amount, 'desc': 'desc', 'currency': currency,
                                                   'platform': platform, 'user': str(request.user), 'time': time_now}
                                        request.session['data'] = context
                                        print(context)
                                        page = 'pages/confirm.html'
                                        template = loader.get_template(page)

                                        return HttpResponse(template.render(context, request),
                                                            status=status.HTTP_200_OK)
                                    else:
                                        page = 'pages/accounts.html'
                                        template = loader.get_template(page)

                                        logged_user = User.objects.get(username=request.user)

                                        user = UsersData.objects.get(user=logged_user)

                                        btc = float(user.bitcoin_balance)
                                        eth = float(user.etherum_balance)
                                        ltc = float(user.litecoin_balance)
                                        bch = float(user.bitcoin_cash_balance)
                                        ngn = bal_converter(str(user.local_currency_balance))

                                        hist = History.objects.get(user=logged_user)
                                        print('*' * 500)
                                        history = []
                                        symbol = None
                                        currency = request.session['currency']
                                        if currency == 'BITCOIN':
                                            for h, i in eval(hist.btc_history).items():
                                                history.append(i)
                                                symbol = 'BTC'
                                        elif currency == 'ETHERUM':
                                            for h, i in eval(hist.eth_history).items():
                                                history.append(i)
                                                symbol = 'ETH'
                                        elif currency == 'LITECOIN':
                                            for h, i in eval(hist.ltc_history).items():
                                                history.append(i)
                                                symbol = 'LTC'
                                        elif currency == 'BITCOINCASH':
                                            for h, i in eval(hist.bch_history).items():
                                                history.append(i)
                                                symbol = 'BCH'
                                        elif currency == 'NAIRA':
                                            for h, i in eval(hist.ngn_history).items():
                                                history.append(i)
                                                symbol = 'NGN'

                                        request.session['currency'] = currency
                                        history.reverse()
                                        context = {'btc': btc, 'eth': eth, 'ltc': ltc, 'bch': bch, 'local': ngn,
                                                   'currency': currency.capitalize(), 'history': history,
                                                   'symbol': symbol,
                                                   'status': 'failed',
                                                   'message': f'Transaction failed. insufficient balance'}

                                        return HttpResponse(template.render(context, request),
                                                            status=status.HTTP_200_OK)

                                else:
                                    page = 'pages/accounts.html'
                                    template = loader.get_template(page)

                                    logged_user = User.objects.get(username=request.user)

                                    user = UsersData.objects.get(user=logged_user)

                                    btc = float(user.bitcoin_balance)
                                    eth = float(user.etherum_balance)
                                    ltc = float(user.litecoin_balance)
                                    bch = float(user.bitcoin_cash_balance)
                                    ngn = bal_converter(str(user.local_currency_balance))

                                    hist = History.objects.get(user=logged_user)
                                    print('*' * 500)
                                    history = []
                                    symbol = None
                                    currency = request.session['currency']
                                    if currency == 'BITCOIN':
                                        for h, i in eval(hist.btc_history).items():
                                            history.append(i)
                                            symbol = 'BTC'
                                    elif currency == 'ETHERUM':
                                        for h, i in eval(hist.eth_history).items():
                                            history.append(i)
                                            symbol = 'ETH'
                                    elif currency == 'LITECOIN':
                                        for h, i in eval(hist.ltc_history).items():
                                            history.append(i)
                                            symbol = 'LTC'
                                    elif currency == 'BITCOINCASH':
                                        for h, i in eval(hist.bch_history).items():
                                            history.append(i)
                                            symbol = 'BCH'
                                    elif currency == 'NAIRA':
                                        for h, i in eval(hist.ngn_history).items():
                                            history.append(i)
                                            symbol = 'NGN'

                                    request.session['currency'] = currency
                                    history.reverse()
                                    context = {'btc': btc, 'eth': eth, 'ltc': ltc, 'bch': bch, 'local': ngn,
                                               'currency': currency.capitalize(), 'history': history,
                                               'symbol': symbol,
                                               'status': 'failed',
                                               'message': f'Transaction failed. Invalid amount requested'}

                                    return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

                            else:

                                page = 'pages/accounts.html'
                                template = loader.get_template(page)

                                logged_user = User.objects.get(username=request.user)

                                user = UsersData.objects.get(user=logged_user)

                                btc = float(user.bitcoin_balance)
                                eth = float(user.etherum_balance)
                                ltc = float(user.litecoin_balance)
                                bch = float(user.bitcoin_cash_balance)
                                ngn = bal_converter(str(user.local_currency_balance))

                                hist = History.objects.get(user=logged_user)
                                print('*' * 500)
                                history = []
                                symbol = None
                                currency = request.session['currency']
                                if currency == 'BITCOIN':
                                    for h, i in eval(hist.btc_history).items():
                                        history.append(i)
                                        symbol = 'BTC'
                                elif currency == 'ETHERUM':
                                    for h, i in eval(hist.eth_history).items():
                                        history.append(i)
                                        symbol = 'ETH'
                                elif currency == 'LITECOIN':
                                    for h, i in eval(hist.ltc_history).items():
                                        history.append(i)
                                        symbol = 'LTC'
                                elif currency == 'BITCOINCASH':
                                    for h, i in eval(hist.bch_history).items():
                                        history.append(i)
                                        symbol = 'BCH'
                                elif currency == 'NAIRA':
                                    for h, i in eval(hist.ngn_history).items():
                                        history.append(i)
                                        symbol = 'NGN'

                                request.session['currency'] = currency
                                history.reverse()
                                context = {'btc': btc, 'eth': eth, 'ltc': ltc, 'bch': bch, 'local': ngn,
                                           'currency': currency.capitalize(), 'history': history,
                                           'symbol': symbol,
                                           'status': 'failed',
                                           'message': f'invalid address provided'}

                                return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

                        except Exception as e:

                            page = 'pages/accounts.html'
                            template = loader.get_template(page)

                            logged_user = User.objects.get(username=request.user)

                            user = UsersData.objects.get(user=logged_user)

                            btc = float(user.bitcoin_balance)
                            eth = float(user.etherum_balance)
                            ltc = float(user.litecoin_balance)
                            bch = float(user.bitcoin_cash_balance)
                            ngn = bal_converter(str(user.local_currency_balance))

                            hist = History.objects.get(user=logged_user)
                            print('*' * 500)
                            history = []
                            symbol = None
                            currency = request.session['currency']
                            if currency == 'BITCOIN':
                                for h, i in eval(hist.btc_history).items():
                                    history.append(i)
                                    symbol = 'BTC'
                            elif currency == 'ETHERUM':
                                for h, i in eval(hist.eth_history).items():
                                    history.append(i)
                                    symbol = 'ETH'
                            elif currency == 'LITECOIN':
                                for h, i in eval(hist.ltc_history).items():
                                    history.append(i)
                                    symbol = 'LTC'
                            elif currency == 'BITCOINCASH':
                                for h, i in eval(hist.bch_history).items():
                                    history.append(i)
                                    symbol = 'BCH'
                            elif currency == 'NAIRA':
                                for h, i in eval(hist.ngn_history).items():
                                    history.append(i)
                                    symbol = 'NGN'

                            request.session['currency'] = currency
                            history.reverse()
                            context = {'btc': btc, 'eth': eth, 'ltc': ltc, 'bch': bch, 'local': ngn,
                                       'currency': currency.capitalize(), 'history': history,
                                       'symbol': symbol,
                                       'status': 'failed',
                                       'message': f'something went wrong, please try again later'}

                            return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)


                    else:
                        page = 'pages/accounts.html'
                        template = loader.get_template(page)

                        logged_user = User.objects.get(username=request.user)

                        user = UsersData.objects.get(user=logged_user)

                        btc = float(user.bitcoin_balance)
                        eth = float(user.etherum_balance)
                        ltc = float(user.litecoin_balance)
                        bch = float(user.bitcoin_cash_balance)
                        ngn = bal_converter(str(user.local_currency_balance))

                        hist = History.objects.get(user=logged_user)
                        print('*' * 500)
                        history = []
                        symbol = None
                        currency = request.session['currency']
                        if currency == 'BITCOIN':
                            for h, i in eval(hist.btc_history).items():
                                history.append(i)
                                symbol = 'BTC'
                        elif currency == 'ETHERUM':
                            for h, i in eval(hist.eth_history).items():
                                history.append(i)
                                symbol = 'ETH'
                        elif currency == 'LITECOIN':
                            for h, i in eval(hist.ltc_history).items():
                                history.append(i)
                                symbol = 'LTC'
                        elif currency == 'BITCOINCASH':
                            for h, i in eval(hist.bch_history).items():
                                history.append(i)
                                symbol = 'BCH'
                        elif currency == 'NAIRA':
                            for h, i in eval(hist.ngn_history).items():
                                history.append(i)
                                symbol = 'NGN'

                        request.session['currency'] = currency
                        history.reverse()
                        context = {'btc': btc, 'eth': eth, 'ltc': ltc, 'bch': bch, 'local': ngn,
                                   'currency': currency.capitalize(), 'history': history,
                                   'symbol': symbol,
                                   'status': 'failed',
                                   'message': f'invalid pin provided'}

                        return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

                else:
                    logout(request)
                    return redirect('login')

            except IndexError as e:
                print(e)
                logout(request)
                return redirect('login')

        if request.method == 'GET':

            params = request.session['data']
            currency = params['currency']

            user = params['user']
            amount = params['amount']
            platform = 'blockchain'

            if User.objects.get(username=user):
                user = User.objects.get(username=user)
                user = UsersData.objects.get(user=user)
                balance = 0.00

                if currency == 'BITCOIN':
                    balance = float(user.bitcoin_balance)
                    params['currency'] = 'BTC'

                elif currency == 'ETHERUM':
                    balance = float(user.etherum_balance)
                    params['currency'] = 'ETH'

                elif currency == 'LITECOIN':
                    balance = float(user.litecoin_balance)
                    params['currency'] = 'LTC'

                elif currency == 'BITCOINCASH':
                    balance = float(user.bitcoin_cash_balance)
                    params['currency'] = 'BCH'

                elif currency == 'NAIRA':
                    balance = float(user.local_currency_balance)
                    params['currency'] = 'NGN'

                if balance >= float(amount):
                    response = 'request not resolved'

                    addresses = Address.objects.filter(address=params['to'])
                    print(addresses)

                    if len(addresses) > 0:
                        user = addresses[0].user
                        user = User.objects.get(username=user)
                        user = UsersData.objects.get(user=user)
                        params['to'] = str(user.email)
                        platform = 'axemo'



                    print(currency * 10)
                    if currency == 'BITCOIN':
                        params['route'] = platform

                        if platform == 'blockchain':
                            response = coinbase(params)

                        elif platform == 'coinbase':
                            response = coinbase(params)

                        elif platform == 'luno':
                            response = luno(params)

                        elif platform == 'axemo':
                            response = local(params)

                    else:
                        params['route'] = platform

                        if platform == 'blockchain':
                            response = coinbase(params)

                        elif platform == 'axemo':
                            response = local(params)

                    if response == 'success':
                        receiver = params['to']
                        currency = params['currency']

                        page = 'pages/accounts.html'
                        template = loader.get_template(page)

                        logged_user = User.objects.get(username=request.user)

                        user = UsersData.objects.get(user=logged_user)

                        btc = float(user.bitcoin_balance)
                        eth = float(user.etherum_balance)
                        ltc = float(user.litecoin_balance)
                        bch = float(user.bitcoin_cash_balance)
                        ngn = bal_converter(str(user.local_currency_balance))

                        hist = History.objects.get(user=logged_user)
                        print('*' * 500)
                        history = []
                        symbol = None
                        currency = request.session['currency']
                        if currency == 'BITCOIN':
                            for h, i in eval(hist.btc_history).items():
                                history.append(i)
                                symbol = 'BTC'
                        elif currency == 'ETHERUM':
                            for h, i in eval(hist.eth_history).items():
                                history.append(i)
                                symbol = 'ETH'
                        elif currency == 'LITECOIN':
                            for h, i in eval(hist.ltc_history).items():
                                history.append(i)
                                symbol = 'LTC'
                        elif currency == 'BITCOINCASH':
                            for h, i in eval(hist.bch_history).items():
                                history.append(i)
                                symbol = 'BCH'
                        elif currency == 'NAIRA':
                            for h, i in eval(hist.ngn_history).items():
                                history.append(i)
                                symbol = 'NGN'

                        request.session['currency'] = currency
                        history.reverse()
                        context = {'btc': btc, 'eth': eth, 'ltc': ltc, 'bch': bch, 'local': ngn,
                                   'currency': currency.capitalize(), 'history': history,
                                   'symbol': symbol,
                                   'status': 'success',
                                   'message': f'sent {currency}{amount} to  {receiver} successfully'}

                        return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

                    else:
                        page = 'pages/accounts.html'
                        template = loader.get_template(page)

                        logged_user = User.objects.get(username=request.user)

                        user = UsersData.objects.get(user=logged_user)

                        btc = float(user.bitcoin_balance)
                        eth = float(user.etherum_balance)
                        ltc = float(user.litecoin_balance)
                        bch = float(user.bitcoin_cash_balance)
                        ngn = bal_converter(str(user.local_currency_balance))

                        hist = History.objects.get(user=logged_user)
                        print('*' * 500)
                        history = []
                        symbol = None
                        currency = request.session['currency']
                        if currency == 'BITCOIN':
                            for h, i in eval(hist.btc_history).items():
                                history.append(i)
                                symbol = 'BTC'
                        elif currency == 'ETHERUM':
                            for h, i in eval(hist.eth_history).items():
                                history.append(i)
                                symbol = 'ETH'
                        elif currency == 'LITECOIN':
                            for h, i in eval(hist.ltc_history).items():
                                history.append(i)
                                symbol = 'LTC'
                        elif currency == 'BITCOINCASH':
                            for h, i in eval(hist.bch_history).items():
                                history.append(i)
                                symbol = 'BCH'
                        elif currency == 'NAIRA':
                            for h, i in eval(hist.ngn_history).items():
                                history.append(i)
                                symbol = 'NGN'

                        request.session['currency'] = currency
                        history.reverse()
                        context = {'btc': btc, 'eth': eth, 'ltc': ltc, 'bch': bch, 'local': ngn,
                                   'currency': currency.capitalize(), 'history': history,
                                   'symbol': symbol,
                                   'status': 'failed', 'message': f'something went wrong. please try again later'}

                        return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

                else:

                    page = 'pages/accounts.html'
                    template = loader.get_template(page)

                    logged_user = User.objects.get(username=request.user)

                    user = UsersData.objects.get(user=logged_user)

                    btc = float(user.bitcoin_balance)
                    eth = float(user.etherum_balance)
                    ltc = float(user.litecoin_balance)
                    bch = float(user.bitcoin_cash_balance)
                    ngn = bal_converter(str(user.local_currency_balance))

                    hist = History.objects.get(user=logged_user)
                    print('*' * 500)
                    history = []
                    symbol = None
                    currency = request.session['currency']
                    if currency == 'BITCOIN':
                        for h, i in eval(hist.btc_history).items():
                            history.append(i)
                            symbol = 'BTC'
                    elif currency == 'ETHERUM':
                        for h, i in eval(hist.eth_history).items():
                            history.append(i)
                            symbol = 'ETH'
                    elif currency == 'LITECOIN':
                        for h, i in eval(hist.ltc_history).items():
                            history.append(i)
                            symbol = 'LTC'
                    elif currency == 'BITCOINCASH':
                        for h, i in eval(hist.bch_history).items():
                            history.append(i)
                            symbol = 'BCH'
                    elif currency == 'NAIRA':
                        for h, i in eval(hist.ngn_history).items():
                            history.append(i)
                            symbol = 'NGN'

                    request.session['currency'] = currency
                    history.reverse()
                    context = {'btc': btc, 'eth': eth, 'ltc': ltc, 'bch': bch, 'local': ngn,
                               'currency': currency.capitalize(), 'history': history, 'symbol': symbol,
                               'status': 'failed', 'message': f'insufficient balance'}

                    return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

            else:

                page = 'pages/accounts.html'
                template = loader.get_template(page)

                logged_user = User.objects.get(username=request.user)

                user = UsersData.objects.get(user=logged_user)

                btc = float(user.bitcoin_balance)
                eth = float(user.etherum_balance)
                ltc = float(user.litecoin_balance)
                bch = float(user.bitcoin_cash_balance)
                ngn = bal_converter(str(user.local_currency_balance))

                hist = History.objects.get(user=logged_user)
                print('*' * 500)
                history = []
                symbol = None
                currency = request.session['currency']
                if currency == 'BITCOIN':
                    for h, i in eval(hist.btc_history).items():
                        history.append(i)
                        symbol = 'BTC'
                elif currency == 'ETHERUM':
                    for h, i in eval(hist.eth_history).items():
                        history.append(i)
                        symbol = 'ETH'
                elif currency == 'LITECOIN':
                    for h, i in eval(hist.ltc_history).items():
                        history.append(i)
                        symbol = 'LTC'
                elif currency == 'BITCOINCASH':
                    for h, i in eval(hist.bch_history).items():
                        history.append(i)
                        symbol = 'BCH'
                elif currency == 'NAIRA':
                    for h, i in eval(hist.ngn_history).items():
                        history.append(i)
                        symbol = 'NGN'

                request.session['currency'] = currency
                history.reverse()
                context = {'btc': btc, 'eth': eth, 'ltc': ltc, 'bch': bch, 'local': ngn,
                           'currency': currency.capitalize(), 'history': history, 'symbol': symbol,
                           'status': 'failed',
                           'message': 'something went wrong. please cross-check your entries and try again'}

                return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

        else:
            page = 'pages/accounts.html'
            template = loader.get_template(page)

            logged_user = User.objects.get(username=request.user)

            user = UsersData.objects.get(user=logged_user)

            btc = float(user.bitcoin_balance)
            eth = float(user.etherum_balance)
            ltc = float(user.litecoin_balance)
            bch = float(user.bitcoin_cash_balance)
            ngn = bal_converter(str(user.local_currency_balance))

            hist = History.objects.get(user=logged_user)
            print('*' * 500)
            history = []
            symbol = None
            currency = request.session['currency']
            if currency == 'BITCOIN':
                for h, i in eval(hist.btc_history).items():
                    history.append(i)
                    symbol = 'BTC'
            elif currency == 'ETHERUM':
                for h, i in eval(hist.eth_history).items():
                    history.append(i)
                    symbol = 'ETH'
            elif currency == 'LITECOIN':
                for h, i in eval(hist.ltc_history).items():
                    history.append(i)
                    symbol = 'LTC'
            elif currency == 'BITCOINCASH':
                for h, i in eval(hist.bch_history).items():
                    history.append(i)
                    symbol = 'BCH'
            elif currency == 'NAIRA':
                for h, i in eval(hist.ngn_history).items():
                    history.append(i)
                    symbol = 'NGN'

            request.session['currency'] = currency
            history.reverse()
            context = {'btc': btc, 'eth': eth, 'ltc': ltc, 'bch': bch, 'local': ngn,
                       'currency': currency.capitalize(), 'history': history, 'symbol': symbol,
                       'status': 'failed',
                       'message': 'something went wrong. please cross-check your entries and try again'}

            return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

    except Exception as e:
        page = 'pages/accounts.html'
        template = loader.get_template(page)

        logged_user = User.objects.get(username=request.user)

        user = UsersData.objects.get(user=logged_user)

        btc = float(user.bitcoin_balance)
        eth = float(user.etherum_balance)
        ltc = float(user.litecoin_balance)
        bch = float(user.bitcoin_cash_balance)
        ngn = bal_converter(str(user.local_currency_balance))

        hist = History.objects.get(user=logged_user)
        print('*' * 500)
        history = []
        symbol = None
        currency = request.session['currency']
        if currency == 'BITCOIN':
            for h, i in eval(hist.btc_history).items():
                history.append(i)
                symbol = 'BTC'
        elif currency == 'ETHERUM':
            for h, i in eval(hist.eth_history).items():
                history.append(i)
                symbol = 'ETH'
        elif currency == 'LITECOIN':
            for h, i in eval(hist.ltc_history).items():
                history.append(i)
                symbol = 'LTC'
        elif currency == 'BITCOINCASH':
            for h, i in eval(hist.bch_history).items():
                history.append(i)
                symbol = 'BCH'
        elif currency == 'NAIRA':
            for h, i in eval(hist.ngn_history).items():
                history.append(i)
                symbol = 'NGN'

        request.session['currency'] = currency
        history.reverse()
        context = {'btc': btc, 'eth': eth, 'ltc': ltc, 'bch': bch, 'local': ngn,
                   'currency': currency.capitalize(), 'history': history, 'symbol': symbol,
                   'status': 'failed',
                   'message': 'something went wrong. please try again later'}

        return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)
