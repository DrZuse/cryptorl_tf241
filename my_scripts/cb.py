import cbpro



key = '9cdf8adb50ebc17b8c7467347f85d786'
b64secret = 'NgMe+hZTwrPKANiIOJHwk0vrbRlpannuozXsQx4/x+ZnyiHc3vDt5mGlaandsXsK7WygSFl8nO3YH5cDog6I9A=='
passphrase = 'ndx1r15u0o'
api_url = 'https://api-public.sandbox.pro.coinbase.com'


auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase, api_url)


fills_gen = auth_client.get_fills('BTC-USD')
all_fills = list(fills_gen)
print(all_fills)


auth_client.place_market_order(product_id='BTC-USD', 
                               side='buy', 
                               funds='100.00')

get1acc = auth_client.get_account("06c63d37-1442-43ea-a04f-1ad5d5c0447a")
print(get1acc)

orders = auth_client.get_orders(product_id='BTC-USD')
print(orders)