from django.test import TestCase
import re
from django.http import HttpResponse
from rest_framework import status
from django.template import loader
from rest_framework.decorators import api_view


@api_view(['GET'])
def index(request):

    search_post = request.GET.get('search')

    if search_post:
        posts = 'database objects'
    else:
        posts = "something_else"

    page = 'index.html'
    template = loader.get_template(page)
    return HttpResponse(template.render({'posts': posts}, request), status=status.HTTP_200_OK)
