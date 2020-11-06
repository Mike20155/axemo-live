from django.urls import path
from . import views

urlpatterns = [
    path('invest', views.confirm_investment, name='invest'),
]
