from django.test import TestCase
import re
import time
import datetime
import json
import requests


password = input("Enter string to test: ")

def test():
    if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
        print('true')
    else:
        print('false')


test()