from crypto_transactions.models import History
from django.contrib.auth.models import User
from home.models import UsersData
from .models import Investments
import string
import random
import datetime


def invest_save(param):
    try:
        user = param['user']
        currency = param['currency']
        sender = User.objects.get(username=user)

        user = User.objects.get(username=sender)
        user = UsersData.objects.get(user=user)
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

        param['type'] = 'invest'
        param['status'] = 'active'
        save(param)
        return 'success'

    except Exception as e:
        if str(e) == "User matching query does not exist.":
            return {'error': 'Invalid receivers address.',
                    'message': 'please cross-check address and try again'}
        else:
            return str(e)


def save(param):
    username = param['user']
    param['type'] = 'Debit'
    cur = param['currency']
    current_time = datetime.datetime.now()
    time_now = str(current_time)[:16]
    notify = {'to': 'Forex', 'amount': str(param['amount']), 'desc': 'desc', 'time': time_now, 'currency': cur, 'platform': 'axemo', 'user': str(username), 'route': 'local', 'type': 'Debit', 'status': 'success', 'resolved': True}

    lower_upper_alphabet = string.ascii_letters

    b = random.choice(lower_upper_alphabet).lower()
    e = random.choice(lower_upper_alphabet).lower()
    g = random.choice(lower_upper_alphabet).lower()
    i = random.choice(lower_upper_alphabet).lower()
    a = random.randint(10, 99)
    c = random.randint(10, 99)
    d = random.randint(10, 99)
    f = random.randint(10, 99)
    h = random.randint(10, 99)
    identity = f'{a}{b}{c}{d}{e}{f}{g}{h}{i}'

    user = User.objects.get(username=username)
    hist = History.objects.get(user=user)

    if cur == 'BTC':
        history = eval(hist.btc_history)
        history[identity] = notify
        hist.btc_history = str(history)
    elif cur == 'ETH':
        history = eval(hist.eth_history)
        history[identity] = notify
        hist.eth_history = str(history)
    elif cur == 'LTC':
        history = eval(hist.ltc_history)
        history[identity] = notify
        hist.ltc_history = str(history)
    elif cur == 'BCH':
        history = eval(hist.bch_history)
        history[identity] = notify
        hist.bch_history = str(history)

    hist.save()

    investment = Investments(user=user, tx_hash=identity, capital=param['amount'], status='active',
                             week='one', currency=param['currency'],
                             total_paid=0.00, percentage=0.00)
    investment.save()

    print('transaction saved')
