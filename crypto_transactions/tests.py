import requests

payload = {'test': {'id': 'heheihridicinh', 'amount': '0.0037'}}
r = requests.post('https://hidden-hollows-00126.herokuapp.com/webhooks/coinbase-webhook/', params=payload)
print(r)
