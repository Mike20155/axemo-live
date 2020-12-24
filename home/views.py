from django.http import HttpResponse
from rest_framework import status
from django.template import loader
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import UsersData
from crypto_transactions.models import History
from django.shortcuts import redirect
import time
from .process import bal_converter, investments, fiat_calculator, send_email
from django.core.mail import send_mail
from dotenv import load_dotenv
load_dotenv()


# Create your views here.


@api_view(['GET'])
def home_page(request):
    page = 'landing.html'
    template = loader.get_template(page)
    logout(request)
    return HttpResponse(template.render({'header': 'TESTING ABOUT VIEW'}, request), status=status.HTTP_200_OK)


@api_view(['GET'])
def sitemap(request):
    page = 'sitemap.xml'
    template = loader.get_template(page)
    logout(request)
    return HttpResponse(template.render({'header': 'TESTING ABOUT VIEW'}, request), status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def login_user(request):
    try:
        if request.method == 'GET':
            page = 'pages/login.html'
            template = loader.get_template(page)
            logout(request)
            return HttpResponse(template.render({'message': ''}, request), status=status.HTTP_200_OK)

        if request.method == 'POST':
            username = request.POST.get('email', '').rpartition('@')[0]
            password = request.POST.get('password', '')
            print(request.POST)

            try:
                user = authenticate(username=username, password=password)
                if authenticate(username=username, password=password):
                    login(request, user)

                    request.session['current_user'] = username
                    request.session['user_password'] = password

                    request.session['session_timeout'] = time.time() + 100000
                    request.session['message'] = ''
                    request.session['current_status'] = ''

                    return redirect(dash)

                else:
                    page = 'pages/login.html'
                    template = loader.get_template(page)
                    context = {'message': 'Invalid e-mail or password! '}
                    return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

            except Exception as e:
                page = 'pages/login.html'
                template = loader.get_template(page)
                context = {'timeout': e}
                return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        redirect(home_page)


@api_view(['GET', 'POST'])
def dash(request):
    try:
        request.session['session_timeout'] = time.time() + 100000
        if request.session['session_timeout'] > time.time():
            request.session['session_timeout'] = time.time() + 100000

            request.session['message'] = ''
            request.session['current_status'] = ''

            active_user = User.objects.get(username=request.user)

            user = UsersData.objects.get(user=active_user)

            invested = investments(active_user)

            btc = float(user.bitcoin_balance)
            eth = float(user.etherum_balance)
            ltc = float(user.litecoin_balance)
            bch = float(user.bitcoin_cash_balance)

            # handle total balance

            total_balance = fiat_calculator(btc, eth, ltc, bch)

            btc_fiat = fiat_calculator(btc, 0, 0, 0)
            eth_fiat = fiat_calculator(0, eth, 0, 0)
            ltc_fiat = fiat_calculator(0, 0, ltc, 0)
            bch_fiat = fiat_calculator(0, 0, 0, bch)

            x = ['BITCOIN', 'ETHERUM', 'LITECOIN', 'BITCOINCASH']
            btc = str("{:.8f}".format(user.bitcoin_balance))
            eth = str("{:.8f}".format(user.etherum_balance))
            ltc = str("{:.8f}".format(user.litecoin_balance))
            bch = str("{:.8f}".format(user.bitcoin_cash_balance))

            btc_fiat = str("{:.1f}".format(btc_fiat))
            eth_fiat = str("{:.1f}".format(eth_fiat))
            ltc_fiat = str("{:.1f}".format(ltc_fiat))
            bch_fiat = str("{:.1f}".format(bch_fiat))

            btc_fiat = bal_converter(btc_fiat)
            eth_fiat = bal_converter(eth_fiat)
            ltc_fiat = bal_converter(ltc_fiat)
            bch_fiat = bal_converter(bch_fiat)

            balance = str("{:.1f}".format(total_balance))
            balance = bal_converter(balance)

            if invested:
                total_payment = str("{:.1f}".format(invested['total_payment']))
                invested['total_payment'] = bal_converter(total_payment)

            page = 'pages/dashboard.html'
            template = loader.get_template(page)
            context = {'user': str(request.user), 'x': x, 'btc': btc, "eth": eth,
                       'ltc': ltc, "bch": bch,  'integer': balance, 'invested': invested,
                       'b_fiat': btc_fiat, 'e_fiat': eth_fiat, 'l_fiat': ltc_fiat, 'bc_fiat': bch_fiat}
            return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

        else:
            logout(request)
            page = 'pages/login.html'
            template = loader.get_template(page)
            context = {'timeout': 'This session has expired, please log in again to continue.'}
            return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

    except Exception as e:
        page = 'pages/login.html'
        template = loader.get_template(page)
        context = {'timeout': e}
        return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        page = 'pages/sign_up.html'
        template = loader.get_template(page)
        logout(request)
        return HttpResponse(template.render({'none': 'none'}, request), status=status.HTTP_200_OK)

    if request.method == 'POST':
        try:
            first_name = request.POST.get('firstname', '')
            last_name = request.POST.get('lastname', '')
            password_1 = request.POST.get('password', '')
            password_2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            username = request.POST.get('email', '').rpartition('@')[0]
            ref = request.POST.get('ref', '')

            print(request.POST)

            if len(password_1) < 8:
                context = {'message': 'password must contain 8 or more characters', 'first_name': first_name,
                           'last_name': last_name, 'email': email, 'ref': ref}
                page = 'pages/sign_up.html'
                template = loader.get_template(page)
                return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

            if password_1 != password_2:
                context = {'message': 'Passwords do not match. please enter same password twice',
                           'username': first_name, 'last_name':
                               last_name, 'email': email, 'referral': ref, 'password_1': password_1}
                page = 'pages/sign_up.html'
                template = loader.get_template(page)
                return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

            if username and password_1:
                try:
                    User.objects.get(email=email)

                    context = {'message': f'email {email} already exists, please try again with a  different email',
                               'username': first_name, 'last_name': last_name, 'referral':
                                   ref, 'password_1': password_1, 'password_2': password_2}
                    page = 'pages/register.html'
                    template = loader.get_template(page)
                    return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

                except Exception as e:
                    print(e)
                    print('email available to be used')
                    request.session['registration_details'] = {'first_name': first_name, 'last_name': last_name,
                                                               'email': email, 'username': username, 'ref': ref,
                                                               'password': password_1}
                    request.session['email'] = 'olumichael2015@outlook.com'

                    return redirect(otp_validator)
            else:
                page = 'pages/sign_up.html'
                template = loader.get_template(page)
                context = {'message': 'Something went wrong, please try again.'}
                return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            page = 'pages/sign_up.html'
            template = loader.get_template(page)
            context = {'message': 'Something went wrong, please try again.'}
            return HttpResponse(template.render(context, request),status=status.HTTP_200_OK)

    else:
        redirect(home_page)


@api_view(['GET', 'POST'])
def otp_validator(request):
    if request.method == 'GET':
        request.session['email'] = 'olumichael2015@outlook.com'

        otp = '1234'
        request.session['OTP'] = otp

        email = request.session['email']

        title = 'Confirm OTP'
        message = f'Your OTP is {otp}. Please do not share this code ' \
                  f'with anyone else. If did not request for this OTP please ignore'
        header = 'OTP@BitChedda.com'
        email = [email]

        print('sending email...')
        # send_mail(title, message, header, email, fail_silently=False)
        # send_email()
        print('email sent')

        page = 'pages/otp_.html'
        template = loader.get_template(page)
        email = request.session['registration_details']['email']
        context = {'info': 'OTP', 'email': email}
        return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.POST
        otp = request.POST.get('otp', '')

        if otp == request.session['OTP']:
            try:
                password = request.session['registration_details']['password']
                username = request.session['registration_details']['username']
                ref = request.session['registration_details']['ref']
                first_name = request.session['registration_details']['first_name']
                last_name = request.session['registration_details']['last_name']
                email = request.session['registration_details']['email']

                print('verified')

                info = User.objects.create_user(username=username, email=email, password=password)
                info.save()

                print('CREATED USER')

                user = User.objects.get(username=username)
                user_data = UsersData(user=user, referral=ref, first_name=first_name, last_name=last_name)
                user_data.save()

                print('created users data')

                user = User.objects.get(username=username)
                history = History(user=user)
                history.save()

                print('created history record')

                context = {'message': 'Registration successful',
                           'data': data}

                print('success')

                print(context)

                user = authenticate(username=username, password=password)

                print('authenticated')

                if user is not None:
                    login(request, user)
                    context['logged in'] = str(request.user)
                    return redirect(dash)

                else:
                    redirect(home_page)

            except Exception as e:
                page = 'pages/otp_.html'
                template = loader.get_template(page)
                print('error')
                context = {'message': e}
                return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

        else:
            page = 'pages/otp_.html'
            template = loader.get_template(page)
            email = request.session['registration_details']['email']
            print('wrong')
            context = {'email': email, 'message': 'incorrect otp, please try again.'}
            return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)
    else:
        redirect(home_page)


@api_view(['GET'])
def confirm(request):
    try:
        page = 'pages/confirm.html'
        template = loader.get_template(page)
        return HttpResponse(template.render({'header': ''}, request), status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        redirect(dash)


@api_view(['GET'])
def profile(request):
    try:
        page = 'pages/profile.html'
        template = loader.get_template(page)
        user = request.user
        email = user.email
        user = UsersData.objects.get(username=user)
        first_name = user.first_name
        last_name = user.last_name
        date_created = user.date_created
        context = {'email': email, 'first_name': first_name, 'last_name': last_name, 'date_created': date_created}
        return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        redirect(dash)


@api_view(['GET'])
def terms(request):
    try:
        page = 'pages/terms&c.html'
        template = loader.get_template(page)
        return HttpResponse(template.render({'header': 'Terms and conditions'}, request), status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        redirect(home_page)


@api_view(['GET'])
def logout_view(request):
    try:
        logout(request)
        return redirect(login_user)
    except Exception as e:
        print(e)
        redirect(home_page)


@api_view(['GET'])
def test(request):
    page = 'pages/invest2.html'
    template = loader.get_template(page)
    return HttpResponse(template.render({'tickets': [1, 2, 3, 4, 5], 'resolved': 'false'}, request),
                        status=status.HTTP_200_OK)


