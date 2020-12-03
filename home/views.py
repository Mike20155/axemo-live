from django.http import HttpResponse
from rest_framework import status
from django.template import loader
from .models import RegForm
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import UsersData
from crypto_transactions.models import History
from django.shortcuts import redirect
import time
from .process import bal_converter, investments, fiat_calculator


# Create your views here.


@api_view(['GET'])
def home_page(request):
    page = 'landing.html'
    template = loader.get_template(page)
    user = User.objects.all()
    logout(request)
    return HttpResponse(template.render({'header': 'TESTING ABOUT VIEW'}, request), status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def login_user(request):
    if request.method == 'GET':
        page = 'pages/login.html'
        template = loader.get_template(page)
        logout(request)
        return HttpResponse(template.render({'message': ''}, request), status=status.HTTP_200_OK)

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        try:
            user = authenticate(username=username, password=password)
            if authenticate(username=username, password=password):
                login(request, user)
                print('passsssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')

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
                return HttpResponse(template.render(context, request), status=status.HTTP_406_NOT_ACCEPTABLE)

        except Exception as e:
            page = 'pages/login.html'
            template = loader.get_template(page)
            context = {'timeout': e}
            return HttpResponse(template.render(context, request), status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET', 'POST'])
def dash(request):
    print('pass')
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

            x = ['BITCOIN', 'ETHERUM', 'LITECOIN', 'BITCOINCASH']
            btc = str("{:.8f}".format(user.bitcoin_balance))
            eth = str("{:.8f}".format(user.etherum_balance))
            ltc = str("{:.8f}".format(user.litecoin_balance))
            bch = str("{:.8f}".format(user.bitcoin_cash_balance))

            balance = str("{:.1f}".format(total_balance))
            balance = bal_converter(balance)

            if invested:
                total_payment = str("{:.1f}".format(invested['total_payment']))
                invested['total_payment'] = bal_converter(total_payment)

            page = 'pages/dashboard.html'
            template = loader.get_template(page)
            context = {'user': str(request.user), 'x': x, 'btc': btc, "eth": eth,
                       'ltc': ltc, "bch": bch,  'integer': balance, 'invested': invested}
            return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

        else:
            logout(request)
            page = 'pages/login.html'
            template = loader.get_template(page)
            context = {'timeout': 'This session has expired, please log in again to continue.'}
            return HttpResponse(template.render(context, request), status=status.HTTP_406_NOT_ACCEPTABLE)

    except Exception as e:
        page = 'pages/login.html'
        template = loader.get_template(page)
        context = {'timeout': e}
        return HttpResponse(template.render(context, request), status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET', 'POST'])
def register(request):
    reg_form = RegForm

    if request.method == 'GET':
        form = reg_form(None)
        page = 'pages/register.html'
        template = loader.get_template(page)
        logout(request)
        return HttpResponse(template.render({'form': form}, request), status=status.HTTP_200_OK)

    if request.method == 'POST':
        first_name = request.POST.get('username', '')
        last_name = request.POST.get('lastname', '')
        password_1 = request.POST.get('password', '')
        password_2 = request.POST.get('password2', '')
        email = request.POST.get('email', '')
        username = request.POST.get('email', '').rpartition('@')[0]
        ref = request.POST.get('ref', '')
        form = reg_form(request.POST)
        print(request.POST)

        if len(password_1) < 8:
            context = {'message': 'password must contain 8 or more characters', 'username': first_name, 'last_name':
                       last_name, 'email': email, 'referral': ref}
            page = 'pages/register.html'
            template = loader.get_template(page)
            return HttpResponse(template.render(context, request), status=status.HTTP_406_NOT_ACCEPTABLE)
        if password_1 != password_2:
            context = {'message': 'Passwords do not match. please enter same password twice', 'username': first_name, 'last_name':
                       last_name, 'email': email, 'referral': ref, 'password_1': password_1}
            page = 'pages/register.html'
            template = loader.get_template(page)
            return HttpResponse(template.render(context, request), status=status.HTTP_406_NOT_ACCEPTABLE)

        if form.is_valid():
            email = form.cleaned_data['email']
            print(email)

            print(User.objects.all())

            if len(User.objects.filter(email=email)) == 0:
                print('pass')

            try:
                User.objects.get(email=email)

                context = {'message': f'email {email} already exists, please try again with a  different email',
                           'username': first_name, 'last_name': last_name, 'referral':
                               ref, 'password_1': password_1, 'password_2': password_2}
                page = 'pages/register.html'
                template = loader.get_template(page)
                return HttpResponse(template.render(context, request), status=status.HTTP_406_NOT_ACCEPTABLE)

            except Exception as e:
                print(e)
                print('email available to be used')
                password = form.cleaned_data['password']

                request.session['registration_details'] = {'first_name': first_name, 'last_name': last_name,
                                                           'email': email, 'username': username, 'ref': ref,
                                                           'password': password}

                otp = '1234'
                request.session['OTP'] = otp

                """send_mail(
                    'Confirm OTP',
                    f'Your OTP is {otp}. Please do not share this code with anyone else. '
                    'If did not request for this OTP please ignore',
                    'Axemo',
                    ['olumichael2015@outlook.com'],
                    fail_silently=False,
                )"""

                print('otp sent')

                return redirect(otp_validator)

        page = 'pages/register.html'
        template = loader.get_template(page)
        context = {'message': 'Something went wrong, please try again.'}
        return HttpResponse(template.render(context, request), status=status.HTTP_406_NOT_ACCEPTABLE)

    else:
        redirect(home_page)


@api_view(['GET', 'POST'])
def otp_validator(request):
    if request.method == 'GET':
        page = 'pages/otp.html'
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

                info = User.objects.create_user(username=username, email=email, password=password)
                info.save()

                user = User.objects.get(username=username)
                user_data = UsersData(user=user, referral=ref, first_name=first_name, last_name=last_name)
                user_data.save()

                user = User.objects.get(username=username)
                history = History(user=user)
                history.save()

                context = {'message': 'Registration successful',
                           'data': data}
                print(context)
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    context['logged in'] = str(request.user)
                    return redirect(dash)
                else:
                    redirect(home_page)

            except Exception as e:
                page = 'pages/register.html'
                template = loader.get_template(page)
                context = {'error': e}
                return HttpResponse(template.render(context, request), status=status.HTTP_406_NOT_ACCEPTABLE)

        else:
            page = 'pages/otp.html'
            template = loader.get_template(page)
            email = request.session['registration_details']['email']
            context = {'email': email, 'message': 'incorrect otp, please try again.'}
            return HttpResponse(template.render(context, request), status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        redirect(home_page)






@api_view(['GET'])
def confirm(request):
    page = 'pages/confirm.html'
    template = loader.get_template(page)
    return HttpResponse(template.render({'header': ''}, request), status=status.HTTP_200_OK)


@api_view(['GET'])
def profile(request):
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


@api_view(['GET'])
def terms(request):
    page = 'pages/terms&c.html'
    template = loader.get_template(page)
    return HttpResponse(template.render({'header': 'Terms and conditions'}, request), status=status.HTTP_200_OK)


@api_view(['GET'])
def logout_view(request):
    # logout(request)
    return redirect(login_user)


@api_view(['GET'])
def test(request):
    page = 'pages/test.html'
    template = loader.get_template(page)
    return HttpResponse(template.render({'logo': ''}, request), status=status.HTTP_200_OK)