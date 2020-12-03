from django.urls import path
from . import views

urlpatterns = [
    path('crypto/<currency>', views.crypto, name='crypto'),
    path('receive/', views.receive, name='receive'),
    path('send/', views.send, name='send'),
    path('confirm/', views.check, name='check'),

]
