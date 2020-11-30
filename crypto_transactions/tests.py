from coinbase.wallet.client import Client


key = "qllinMZsWKJxMbm1"
secret = "O8166FUvpXgZk5XowalRE8cP0tVXRWkT"
btc_id ="98d51393-b7bf-5381-b727-21200c515708"

print('sending to coinbase....')
client = Client(key, secret)
print('validating client....')
tx = client.send_money(btc_id, to='3HeRwDwBR7yAPr4Xu7E12brFUjoCUB48Eo', amount=float(0.000028), currency='BTC',
                       desc='DESC')
print(tx)