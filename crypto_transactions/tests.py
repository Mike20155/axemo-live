from coinbase.wallet.client import Client


key = "qllinMZsWKJxMbm1"
secret = "O8166FUvpXgZk5XowalRE8cP0tVXRWkT"
btc_id ="98d51393-b7bf-5381-b727-21200c515708"

to = "98d51393-b7bf-5381-b727-21200c5157"

param = f'{to[:7]}...{to[27:]}'
print(param)
print(len(to))
