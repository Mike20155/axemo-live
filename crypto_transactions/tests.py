from coinbase.wallet.client import Client


key = "qllinMZsWKJxMbm1"
secret = "O8166FUvpXgZk5XowalRE8cP0tVXRWkT"


client = Client(key, secret)

rates = client.get_exchange_rates(currency='BTC')
print(rates['rates']['USD'])