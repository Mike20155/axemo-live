from investments.models import Investments
from django.utils import timezone
from .models import UsersData
from django.contrib.auth.models import User


def investments(user):
    active_user = User.objects.get(username=user)

    active = Investments.objects.filter(user=active_user, status='active')

    if len(active) > 0:
        for i in active:
            start = i.date_created
            percentage = i.percentage
            crypto_capital = i.capital
            print('pass')

            now = timezone.now()

            total = str(now - start)[:2]
            tot = str(now - start)
            if len(str(now - start)) < 16:
                total = 0

            print(len(tot))

            weeks = int(total)/7
            weeks = int(weeks)
            print('pass')
            print(int(weeks))

            user = UsersData.objects.get(user=active_user)

            c = 0.00

            if i.currency == 'BTC':
                c = float(user.bitcoin_balance)
            elif i.currency == 'ETH':
                c = float(user.etherum_balance)
            elif i.currency == 'LTC':
                c = float(user.litecoin_balance)
            elif i.currency == 'BCH':
                c = float(user.bitcoin_cash_balance)
            print('pass')

            if weeks == 1:

                if percentage < 35:
                    print('due')
                    top_up = float((35/100)*float(crypto_capital))
                    c += top_up
                    i.week = 'one'
                    tp = float(i.total_paid)
                    tp += top_up
                    i.total_paid = tp
                    print('pass3')
                    i.percentage = 35
                else:
                    pass
            elif weeks == 2:
                if percentage < 70:
                    print('due')
                    p = (70 - percentage)
                    top_up = float((p / 100) * crypto_capital)
                    c += top_up
                    i.week = 'two'
                    print('pass2')
                    tp = float(i.total_paid)
                    tp += top_up
                    i.total_paid = tp
                    print('pass3')
                    i.percentage = 70
                else:
                    pass
            elif weeks == 3:

                if percentage < 105:
                    print('due')
                    p = (105 - percentage)
                    top_up = float((p / 100) * crypto_capital)
                    c += top_up
                    i.week = 'three'
                    tp = float(i.total_paid)
                    tp += top_up
                    i.total_paid = tp
                    print('pass3')
                    i.percentage = 105
                else:
                    pass
            elif weeks == 4:
                if percentage < 140:
                    print('due')
                    p = (140 - percentage)
                    top_up = float((p / 100) * crypto_capital)
                    c += top_up
                    i.week = 'four'
                    tp = float(i.total_paid)
                    tp += top_up
                    i.total_paid = tp
                    print('pass36766587')
                    i.percentage = 140
                    i.status = 'completed'
                else:
                    pass
            else:
                pass
            print('pass')

            i.save()

            start = i.date_created
            percentage = i.percentage
            fiat_capital = i.capital
            crypto_capital = i.capital
            week = i.week
            total_paid = i.total_paid
            currency = i.currency
            id = i.tx_hash

            data = {'start': start, 'percentage': percentage, 'fiat': str(fiat_capital), 'crypto': crypto_capital, 'week': week,
                    'total_paid': total_paid, 'currency': currency, 'id': id}

            return data

    else:
        return None


def bal_converter(x):
    print(len(x))
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
