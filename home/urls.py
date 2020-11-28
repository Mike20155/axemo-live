from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('terms&conditions', views.terms, name='terms'),
    path('register', views.register, name='register'),
    path('otp', views.otp_validator, name='otp'),
    path('login', views.login_user, name='login'),
    path('dash', views.dash, name='dash'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logout_view, name='logout')
]
