from coinbase.wallet.client import Client
from crypto_transactions.models import History
from django.contrib.auth.models import User
from home.models import UsersData
import string
import random
from .models import DebitTransaction, Address


# make transaction here
key = "qllinMZsWKJxMbm1"
secret = "O8166FUvpXgZk5XowalRE8cP0tVXRWkT"

btc_id ="98d51393-b7bf-5381-b727-21200c515708"
eth_id = "181fc56c-73d6-568e-ab6d-1c0aedc9f333"
ltc_id = "7c31f848-dc67-5510-8ff4-0e5e74a700c6"
bch_id = "b38fa818-27f2-5fe2-822f-0d24ab658ee1"

client = Client(key, secret)


def get_address(user, cu):
    client = Client(key, secret)

    address = None
    if cu == 'BITCOIN':
        address = client.create_address(btc_id)
    if cu == 'ETHERUM':
        address = client.create_address(eth_id)
    if cu == 'BITCOINCASH':
        address = client.create_address(bch_id)
    if cu == 'LITECOIN':
        address = client.create_address(ltc_id)

    user = User.objects.get(username=user)
    address_saver = Address(user=user, address=address['address'], currency=cu)
    address_saver.save()
    return address['address']


def bal_converter(x):
    if len(x) == 6:
        a = x[0]
        b = x[1:]
        return f'{a},{b}'
    elif len(x) == 7:
        a = x[:2]
        b = x[2:]
        return f'{a},{b}'
    elif len(x) == 8:
        a = x[:3]
        b = x[3:]
        return f'{a},{b}'
    elif len(x) == 9:
        a = x[0]
        b = x[1:4]
        c = x[4:]
        return f'{a},{b},{c}'
    elif len(x) == 10:
        a = x[:2]
        b = x[2:5]
        c = x[5:]
        return f'{a},{b},{c}'
    elif len(x) == 11:
        a = x[:2]
        b = x[2:5]
        c = x[5:]
        return f'{a},{b},{c}'
    else:
        return x


def coinbase(param, to):
    crypt = param['bal']
    param['amount'] = crypt

    try:
        # tx = ['completed']
        print('sending to coinbase....')
        client = Client(key, secret)
        print('validating client....')
        tx = client.send_money(btc_id, to=param['to'], amount=float(param['amount']), currency=param['currency'],
                               desc=param['desc'])
        print(tx)
        if tx['status'] == 'completed':
            param['status'] = 'success'
            param['resolved'] = True
            currency = param['currency']
            user = User.objects.filter(username=param['user'])[0]
            user = UsersData.objects.filter(user=user)[0]

            if currency == 'BTC':
                balance = float(user.bitcoin_balance)
                balance -= float(param['amount'])
                user.bitcoin_balance = balance
            elif currency == 'ETH':
                balance = float(user.etherum_balance)
                balance -= float(param['amount'])
                user.etherum_balance = balance
            elif currency == 'LTC':
                balance = float(user.litecoin_balance)
                balance -= float(param['amount'])
                user.litecoin_balance = balance
            elif currency == 'BTC':
                balance = float(user.bitcoin_cash_balance)
                balance -= float(param['amount'])
                user.bitcoin_cash_balance = balance

            user.save()
            save(param, to)
            return 'success'
        else:
            return 'transaction failed'
    except IndexError as e:
        print('error'*10)
        return str(e)


def luno(param):
    try:
        user = User.objects.get(username=param['user'])
        user = UsersData.objects.get(user=user)
        balance = float(user.bitcoin_balance)
        balance -= float(param['amount'])
        user.bitcoin_balance = balance
        user.save()

        param['status'] = 'pending'
        param['resolved'] = False
        # save(param, to)
        return 'success'
    except Exception as e:
        return str(e)


def local(param, to):
    try:
        receiver = param['to']
        sender = param['user']
        currency = param['currency']
        crypt = param['crypto']
        param['amount'] = crypt
        x = User.objects.filter(email=receiver)
        if len(x) == 1:
            sender = User.objects.filter(username=sender)[0]
            user = UsersData.objects.filter(user=sender)[0]

            if currency == 'BTC':
                balance = float(user.bitcoin_balance)
                balance -= float(param['amount'])
                user.bitcoin_balance = balance
            elif currency == 'ETH':
                balance = float(user.etherum_balance)
                balance -= float(param['amount'])
                user.etherum_balance = balance
            elif currency == 'LTC':
                balance = float(user.litecoin_balance)
                balance -= float(param['amount'])
                user.litecoin_balance = balance
            elif currency == 'BCH':
                balance = float(user.bitcoin_cash_balance)
                balance -= float(param['amount'])
                user.bitcoin_cash_balance = balance

            user.save()
            param['type'] = 'Transfer'
            param['status'] = 'success'
            param['resolved'] = True
            param['type'] = 'Debit'
            print('ghcyech yce')

            identity = save(param, to)
            print(identity)

            receiver = User.objects.filter(email=receiver)[0]
            r = UsersData.objects.filter(user=receiver)[0]

            hist = History.objects.filter(user=receiver)[0]
            param['type'] = 'Credit'
            param['from'] = f'{to[:20]}......'
            param['real_address'] = to

            print('heloo')
            print(param)
            amount = float(param['amount'])

            try:
                if currency == 'BTC':
                    balance = float(r.bitcoin_balance)
                    balance += amount
                    r.bitcoin_balance = balance
                    history = eval(hist.btc_history)
                    print('XERTSUUSOOS')
                    print(param)
                    history[identity] = param
                    hist.btc_history = str(history)
                elif currency == 'ETH':
                    balance = float(r.etherum_balance)
                    balance += amount
                    r.etherum_balance = balance
                    history = eval(hist.eth_history)
                    history[identity] = param
                    hist.eth_history = str(history)
                elif currency == 'LTC':
                    balance = float(r.litecoin_balance)
                    balance += amount
                    r.litecoin_balance = balance
                    history = eval(hist.ltc_history)
                    history[identity] = param
                    hist.ltc_history = str(history)
                elif currency == 'BCH':
                    balance = float(r.bitcoin_cash_balance)
                    balance += amount
                    r.bitcoin_cash_balance = balance
                    history = eval(hist.bch_history)
                    history[identity] = param
                    hist.bch_history = str(history)
            except Exception as e:
                print(e)
                print('error herer')

            hist.save()
            r.save()
            return 'success'
        else:
            return f'User: {receiver} does not exist'
    except Exception as e:
        print(f'error is {e}')
        if str(e) == "User matching query does not exist.":
            return {'error': 'Invalid receivers address.',
                    'message': 'please cross-check address and try again'}
        else:
            return str(e)


def save(param, to):
    username = param['user']
    param['type'] = 'Debit'
    cur = param['currency']

    letters = string.ascii_lowercase
    identity = ''.join(random.choice(letters) for _ in range(30))

    user = User.objects.get(username=username)
    hist = History.objects.get(user=user)
    param['amount'] = str("{:.8f}".format(param['amount']))
    param['to'] = f'{to[:20]}......'
    param['real_address'] = to

    if cur == 'BTC':
        history = eval(hist.btc_history)
        history[identity] = param
        hist.btc_history = str(history)
    elif cur == 'ETH':
        history = eval(hist.eth_history)
        history[identity] = param
        hist.eth_history = str(history)
    elif cur == 'LTC':
        history = eval(hist.ltc_history)
        history[identity] = param
        hist.ltc_history = str(history)
    elif cur == 'BCH':
        history = eval(hist.bch_history)
        history[identity] = param
        hist.bch_history = str(history)

    hist.save()

    dec = param['desc']
    description = f'From: axemo \n sender: {user} \n description: {dec}'
    param['route'] = 'axemo'

    debit = DebitTransaction(user=user, username=username, tx_hash=identity, amount=param['amount'],
                             description=description, destination=to,
                             status=param['status'], resolve=param['resolved'], route=param['route'])

    debit.save()
    return identity


def crypto_calculator(btc, eth, ltc, bch):
    btc_rate = client.get_exchange_rates(currency='BTC')
    eth_rate = client.get_exchange_rates(currency='ETH')
    ltc_rate = client.get_exchange_rates(currency='LTC')
    bch_rate = client.get_exchange_rates(currency='BCH')

    btc_rate = float(btc_rate['rates']['USD'])
    eth_rate = float(eth_rate['rates']['USD'])
    ltc_rate = float(ltc_rate['rates']['USD'])
    bch_rate = float(bch_rate['rates']['USD'])

    btc_usd = btc/btc_rate
    eth_usd = eth/eth_rate
    ltc_usd = ltc/ltc_rate
    bch_usd = bch/bch_rate

    total_crypto = btc_usd + eth_usd + ltc_usd + bch_usd

    return total_crypto
