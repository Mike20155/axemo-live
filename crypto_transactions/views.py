from django.http import HttpResponse
from rest_framework import status
from django.template import loader
from .process import coinbase, local, get_address, bal_converter, crypto_calculator
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

            message = request.session['message']
            stats = request.session['current_status']
            p = len(message)
            print(stats)
            print(p)
            print(message)

            request.session['message'] = ''
            request.session['current_status'] = ''

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
                       'currency': currency.capitalize(), 'history': history, 'trans': trans, 'symbol': symbol,
                       'message': message, 'p': p, 'status': stats}
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


@api_view(['GET'])
def send(request):

    currency = request.session['currency']

    logged_user = User.objects.get(username=request.user)

    user = UsersData.objects.get(user=logged_user)
    message = request.session['message']
    stats = request.session['current_status']
    p = len(message)

    request.session['message'] = ''
    request.session['current_status'] = ''

    btc = float(user.bitcoin_balance)
    eth = float(user.etherum_balance)
    ltc = float(user.litecoin_balance)
    bch = float(user.bitcoin_cash_balance)

    btc_ = str("{:.8f}".format(btc))
    eth_ = str("{:.8f}".format(eth))
    ltc_ = str("{:.8f}".format(ltc))
    bch_ = str("{:.8f}".format(bch))

    balance = 0
    symbol = None
    crypt = 0

    if currency == 'BITCOIN':
        balance = fiat_calculator(btc, 0, 0, 0)
        symbol = 'BTC'
        crypt = btc_

    elif currency == 'ETHERUM':
        balance = fiat_calculator(0, eth, 0, 0)
        symbol = 'ETH'
        crypt = eth_

    elif currency == 'LITECOIN':
        balance = fiat_calculator(0, 0, ltc, 0)
        symbol = 'LTC'
        crypt = ltc_

    elif currency == 'BITCOINCASH':
        balance = fiat_calculator(0, 0, 0, bch)
        symbol = 'BCH'
        crypt = bch_

    balance = str("{:.1f}".format(balance))
    balance = bal_converter(balance)
    print(message)
    print(stats)
    print(p)


    page = 'pages/send.html'
    template = loader.get_template(page)

    request.session['fiat_balance'] = balance

    context = {'crypt': crypt,  'fiat': balance,
               'currency': currency.capitalize(),  'symbol': symbol, 'p': p, 'status': stats, 'message': message}

    return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
def check(request):
    try:
        if request.method == 'POST':
            try:
                if request.session['session_timeout'] > time.time():
                    print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
                    request.session['session_timeout'] = time.time() + 1000

                    pin = '0000'

                    user = User.objects.get(username=request.user)
                    user = UsersData.objects.get(user=user)

                    if hashlib.sha256(pin.encode()).hexdigest() == str(user.pin):

                        try:
                            to = request.POST.get('address' '')
                            amount = request.POST.get('amount' '')
                            print(request.POST)

                            btc = float(user.bitcoin_balance)
                            eth = float(user.etherum_balance)
                            ltc = float(user.litecoin_balance)
                            bch = float(user.bitcoin_cash_balance)
                            print('pass')

                            balance = 0.00
                            logo = None

                            if request.session['currency'] == 'BITCOIN':
                                balance = btc
                                logo = "https://img.icons8.com/fluent/96/000000/bitcoin.png"
                            elif request.session['currency'] == 'ETHERUM':
                                balance = eth
                                logo = "https://img.icons8.com/fluent/96/000000/ethereum.png"
                            elif request.session['currency'] == 'LITECOIN':
                                balance = ltc
                                logo = "https://img.icons8.com/fluent/96/000000/litecoin.png"
                            elif request.session['currency'] == 'BITCOINCASH':
                                balance = bch

                            currency = request.session['currency']

                            bal = 0.00
                            symbol = None
                            amount = float(amount)

                            if currency == 'BITCOIN':
                                bal = crypto_calculator(amount, 0, 0, 0)
                                symbol = 'BTC'

                            elif currency == 'ETHERUM':
                                bal = crypto_calculator(0, amount, 0, 0)
                                symbol = 'ETH'

                            elif currency == 'LITECOIN':
                                bal = crypto_calculator(0, 0, amount, 0)
                                symbol = 'LTC'

                            elif currency == 'BITCOINCASH':
                                bal = crypto_calculator(0, 0, 0, amount)
                                symbol = 'BCH'

                            if len(to) > 0:
                                if amount > 0:
                                    if len(str(amount)) > 0:
                                        print(balance)
                                        print(bal)
                                        if float(balance) >= float(bal):

                                            print('FORM IS VALID')

                                            current_time = datetime.datetime.now()
                                            time_now = str(current_time)[:16]

                                            bl_fee = 0.00
                                            bc_fee = 0.00
                                            total = amount + bl_fee + bc_fee
                                            total = str("{:.1f}".format(total))
                                            total = bal_converter(total)

                                            context = {'to': to, 'amount': amount, 'bc_fee': bc_fee, 'bl_fee': bl_fee,
                                                       'total': total, 'crypto': bal, 'desc': 'desc', 'c': currency,
                                                       'symbol': symbol, 'user': str(request.user), 'time': time_now,
                                                       'logo': logo}
                                            request.session['data'] = context
                                            print(context)
                                            page = 'pages/confirmation.html'
                                            template = loader.get_template(page)

                                            return HttpResponse(template.render(context, request),
                                                                status=status.HTTP_200_OK)
                                        else:
                                            fiat = request.session['fiat_balance']
                                            request.session['message'] = {'a': f'Insufficient balance! you have only ', 'b': f'${fiat}',
                                                  'c': 'available'}
                                            return redirect(send)
                                    else:
                                        request.session['message'] = {'a': f'Invalid amount'}
                                        return redirect(send)

                                else:
                                    request.session['message'] = {'a': f'Invalid amount'}
                                    return redirect(send)

                            else:
                                request.session['message'] = {'a': f'Invalid address provided'}
                                return redirect(send)

                        except Exception as e:
                            currency = request.session['currency']
                            request.session['message'] = {'a': f'something went wrong, please try again later 1'}
                            return redirect(send, currency)

                    else:
                        currency = request.session['currency']
                        request.session['message'] = {'a': f'Invalid pin'}
                        return redirect(send, currency)
                else:
                    logout(request)
                    return redirect('login')

            except IndexError as e:
                print(e)
                logout(request)
                return redirect('login')

        if request.method == 'GET':
            params = request.session['data']

            currency = params['c']

            user = params['user']
            amount = params['crypto']


            if User.objects.get(username=user):
                user = User.objects.get(username=user)
                user = UsersData.objects.get(user=user)
                balance = 0.00
                symbol = None

                if currency == 'BITCOIN':
                    balance = float(user.bitcoin_balance)
                    params['currency'] = 'BTC'
                    symbol = 'BTC'

                elif currency == 'ETHERUM':
                    balance = float(user.etherum_balance)
                    params['currency'] = 'ETH'
                    symbol = 'ETH'

                elif currency == 'LITECOIN':
                    balance = float(user.litecoin_balance)
                    params['currency'] = 'LTC'
                    symbol = 'LTC'

                elif currency == 'BITCOINCASH':
                    balance = float(user.bitcoin_cash_balance)
                    params['currency'] = 'BCH'
                    symbol = 'BCH'

                print(params)

                if balance >= float(amount):
                    response = 'request not resolved'

                    addresses = Address.objects.filter(address=params['to'])
                    to = params['to']

                    if len(addresses) > 0:
                        user = addresses[0].user
                        user = User.objects.get(username=user)
                        params['to'] = str(user.email)
                        platform = 'axemo'
                    else:
                        platform = 'blockchain'

                    if platform == 'blockchain':
                        response = coinbase(params, to)

                    elif platform == 'axemo':
                        response = local(params, to)

                    if response == 'success':
                        amount = params['crypto']
                        amount = str("{:.8f}".format(amount))
                        message = {'a': 'You have transferred', 'b': f'{amount} {symbol}', 'c': to,
                                   'd': 'successfully'}
                        request.session['message'] = message
                        request.session['current_status'] = 'success'
                        return redirect(crypto, currency)

                    else:
                        currency = request.session['currency']
                        request.session['message'] = {'a': f'something went wrong, please try again later 2'}
                        return redirect(crypto, currency)

                else:
                    fiat = request.session['fiat_balance']
                    request.session['message'] = {'a': f'Insufficient balance! you have only ', 'b': fiat,
                                                  'c': 'available 2'}
                    return redirect(send)
            else:
                request.session['message'] = {'a': 'something went wrong. please cross-check your entries and try again 3'}
                return redirect(send)

        else:
            request.session['message'] = {'a': 'something went wrong. please cross-check your entries and try again 4'}
            return redirect(send)

    except Exception as e:
        print(e)
        currency = request.session['currency']
        request.session['message'] = {'a': f'something went wrong, please try again later 5'}
        return redirect(crypto, currency)
