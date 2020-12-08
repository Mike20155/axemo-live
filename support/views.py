from django.http import HttpResponse
from rest_framework import status
from django.template import loader
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import Tickets, Contacts, Inquiry

# Create your views here.


@api_view(['GET'])
def help_desk(request):
    page = 'pages/suport.html'
    template = loader.get_template(page)
    context = {'user': str(request.user)}
    return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def inquiries(request):

    if request.method == 'GET':
        page = 'pages/enquires.html'
        template = loader.get_template(page)
        return HttpResponse(template.render({'header': ''}, request), status=status.HTTP_200_OK)

    if request.method == 'POST':
        page = 'pages/sent.html'

        name = request.POST.get('fullname', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        inc = Inquiry(full_name=name, email=email, inquiry=message)
        inc.save()

        message = {'a':  'Your inquiry was submitted successflly, thank you for reaching out to us. A'
                         ' feed back will be relayed in the earliest time possible'}

        context = {'status': 'success', 'message': message}

        template = loader.get_template(page)
        return HttpResponse(template.render(context, request),
                            status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def contact_form(request):

    if request.method == 'GET':
        page = 'pages/contact.html'
        template = loader.get_template(page)
        return HttpResponse(template.render({'header': ''}, request), status=status.HTTP_200_OK)

    if request.method == 'POST':
        page = 'pages/sent.html'

        name = request.POST.get('fullname', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        con = Contacts(full_name=name, email=email, message=message)
        con.save()

        message = {'a':  'Your message was submitted successflly, thank you for reaching out to us.' 
                         'A feed back will be relayed in the earliest time possible'}

        context = {'status': 'success', 'message': message}

        template = loader.get_template(page)
        return HttpResponse(template.render(context, request),
                            status=status.HTTP_200_OK)


@api_view(['GET'])
def tickets(request):
    tics = Tickets.objects.filter(user=request.user)
    print(tics)

    all_tics = []

    for t in tics:
        tic = {'id': t.i_d, 'date': t.date_created, 'stat': t.status, 'title': t.title}
        all_tics.append(tic)

    print(all_tics)

    context = {'all_tic': all_tics, 'tick': len(all_tics)}

    page = 'pages/tickets.html'
    template = loader.get_template(page)
    return HttpResponse(template.render(context, request),
                        status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def create_ticket(request):

    if request.method == 'GET':
        page = 'pages/create_ticket.html'
        template = loader.get_template(page)
        return HttpResponse(template.render({'tickets': [1, 2, 3, 4, 5], 'resolved': 'false'}, request),
                            status=status.HTTP_200_OK)

    if request.method == 'POST':
        page = 'pages/sent.html'
        category = request.POST.get('category', '')
        title = request.POST.get('title', '')
        desc = request.POST.get('desc', '')

        active_user = User.objects.get(username=request.user)

        tic = Tickets(user=active_user, category=category, title=title, description=desc)
        tic.save()
        message = {'a': 'Your ticket has been opended successflly, '
                                                     'thank you for reaching out to us. A '
                                                     'feed back will be relayed in the earliest time possible' }
        context = {'status': 'success', 'message': message}

        template = loader.get_template(page)
        return HttpResponse(template.render(context, request),
                            status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def open_ticket(request, i_d):

    if request.method == 'GET':
        page = 'pages/tickets.html'

        t = Tickets.objects.filter(user=request.user, i_d=i_d)
        t = t[0]

        id = t.i_d
        date = t.date_created
        stat = t.status
        cat = t.category
        title = t.title
        desc = t.desc
        chat = t.chat

        context = {'id': id, 'date': date, 'status': stat, 'cat': cat, 'title': title, 'desc': desc, 'chat': chat}

        template = loader.get_template(page)
        return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

    if request.method == 'POST':
        message = request.POST.get('message', '')

        t = Tickets.objects.filter(user=request.user, i_d=i_d)
        t = t[0]

        chat_history = eval(t.chat)
        chat_history[f'reply{len(t.chat) + 1}'] = message
        t.chat = str(chat_history)

        t.save()

        redirect(open_ticket)



