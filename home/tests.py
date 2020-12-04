from django.test import TestCase
import re
from django.core.mail import send_mail

otp = '1234'

email = 'olumichael2015@outlook.com'
title = 'Confirm OTP'
message = f'Your OTP is {otp}. Please do not share this code ' \
          f'with anyone else. If did not request for this OTP please ignore'
header = 'BitChedda'
email = [email]

print('sending email...')
send_mail(title, message, header, email, fail_silently=False)
print('email sent')
