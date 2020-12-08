from django.urls import path
from . import views


urlpatterns = [
    path('help_desk', views.help_desk, name='help'),
    path('tickets', views.tickets, name='tickets'),
    path('inquiries', views.inquiries, name='inquiries'),
    path('contact_us', views.contact_form, name='contact'),
    path('create_ticket', views.create_ticket, name='create_ticket'),
    path('view_ticket/<i_d>', views.open_ticket, name='open_ticket'),
]

