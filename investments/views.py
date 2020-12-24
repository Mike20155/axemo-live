from .process import invest_save
from django.http import HttpResponse
from rest_framework import status
from django.template import loader
from crypto_transactions.process import coinbase, local, get_address, bal_converter, crypto_calculator
from django.contrib.auth import logout
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from home.models import UsersData
import time
from home.process import fiat_calculator, bal_converter
from django.shortcuts import redirect

# Create your views here.


@api_view(['GET'])
def invest(request):
    try:
        page = 'pages/invest2.html'
        template = loader.get_template(page)
        return HttpResponse(template.render({'header': ''}, request), status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        redirect('dash')


@api_view(['GET', 'POST'])
def amount(request, currency):
    try:
        print(currency)
        page = 'pages/trade_amount.html'

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

        template = loader.get_template(page)

        request.session['fiat_balance'] = balance
        request.session['currency'] = currency

        print(currency)
        print(currency)
        print(currency)
        print(currency)
        print(currency)
        print(currency)
        print(currency)
        print(currency)

        context = {'crypt': crypt, 'fiat': balance,
                   'currency': currency.capitalize(), 'symbol': symbol, 'p': p, 'status': stats, 'message': message}

        return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        redirect('dash')


@api_view(['POST'])
def confirm_invest(request):
    print('229920')
    try:
        if request.session['session_timeout'] > time.time():
            print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
            request.session['session_timeout'] = time.time() + 1000

            pin = '0000'

            user = User.objects.get(username=request.user)
            user = UsersData.objects.get(user=user)

            if True:

                try:
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
                    print(currency)

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

                    if amount > 0:
                        if len(str(amount)) > 0:
                            print(balance)
                            print(bal)
                            if float(balance) >= float(bal):

                                print('FORM IS VALID')

                                bl_fee = 0.00
                                bc_fee = 0.00
                                total = amount + bl_fee + bc_fee
                                total = str("{:.1f}".format(total))
                                total = bal_converter(total)

                                request.session['currency'] = symbol
                                request.session['investment_amount'] = float(bal)

                                context = {'amount': amount, 'bc_fee': bc_fee, 'bl_fee': bl_fee,
                                           'total': total, 'crypto': bal, 'desc': 'desc', 'c': currency,
                                           'symbol': symbol, 'user': str(request.user),
                                           'logo': logo}
                                request.session['data'] = context
                                print(context)
                                page = 'pages/invest_confirm.html'
                                template = loader.get_template(page)

                                return HttpResponse(template.render(context, request),
                                                    status=status.HTTP_200_OK)
                            else:
                                fiat = request.session['fiat_balance']
                                request.session['message'] = {'a': f'Insufficient balance! you have only ',
                                                              'b': f'${fiat}',
                                                              'c': 'available'}
                                return redirect('invest_amount', currency)
                        else:
                            request.session['message'] = {'a': f'Invalid amount'}
                            return redirect('invest_amount', currency)

                    else:
                        request.session['message'] = {'a': f'Invalid amount'}
                        return redirect('invest_amount', currency)

                except Exception as e:
                    print(e)
                    request.session['message'] = {'a': f'something went wrong, please try again later 2'}
                    return redirect('dash')

    except Exception as e:
        print(e)
        request.session['message'] = {'a': f'something went wrong, please try again later 2'}
        return redirect('dash')


@api_view(['GET'])
def make_investment(request):
    try:
        request.session['session_timeout'] = time.time() + 60000000
        if request.session['session_timeout'] > time.time():
            print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
            request.session['session_timeout'] = time.time() + 60000000

            logged_user = User.objects.get(username=request.user)

            user = UsersData.objects.get(user=logged_user)

            currency = request.session['currency']
            amount = request.session['investment_amount']

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

                print(balance)
                print(amount)

                if balance >= float(amount):

                    param = {'user': logged_user, 'currency': currency, 'amount': amount}
                    print(param)

                    invest_save(param)

                    request.session['message'] = {'status': 'success',
                               'message': f'Congratulations! you have successfully invested {currency}{balance}'}
                    return redirect('dash')

                else:
                    page = 'pages/dashboard.html'
                    template = loader.get_template(page)

                    context = {'status': 'failed', 'message': f'insufficient funds in currency requested.'
                                                              f'you have only {currency}{balance} available in your '
                                                              f'{currency} wallet'}
                    return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

        else:
            request.session['message'] = {'message': f'something went wrong while trying to '
                                                 f'process your request, please try again later.'}
            return redirect('dash')

    except Exception as e:
        print(e)
        request.session['message'] = {'message': f'something went wrong while trying to '
                                                 f'process your request, please try again later.'}
        return redirect('dash')

