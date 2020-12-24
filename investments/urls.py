from django.urls import path
from . import views

urlpatterns = [
    path('invest', views.invest, name='invest'),
    path('invest/amount/<currency>', views.amount, name='invest_amount'),
    path('invest/confirm', views.confirm_invest, name='confirm_invest'),
    path('invest/opening_trade', views.make_investment, name='save_invest'),
]
