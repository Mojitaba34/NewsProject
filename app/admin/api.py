import requests,json

def get_BTCPrice():
    r = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT')
    data = r.text
    data = json.loads(data)
    price = round(float(data["price"]),2)
    return price