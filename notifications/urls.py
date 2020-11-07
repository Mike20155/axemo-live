from django.urls import path
from . import views

urlpatterns = [
    path('coinbase-webhook/', views.CoinbaseNotification, name='notify'),
]
