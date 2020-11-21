import requests

payload = {'test': 'this is a webhook test'}
r = requests.post('https://hidden-hollows-00126.herokuapp.com/webhooks/coinbase-webhook/', params=payload)
print(r)
