import time
import requests

amount = 100
wallet = amount
symbol = ''

while True:
    time.sleep(1)
    
    volatile = sorted(requests.get('https://api.binance.com/api/v3/ticker/24hr').json(), key=lambda x: float(x['priceChangePercent']), reverse=True)[0]

    if volatile['symbol'] == symbol:
        volatile = sorted(requests.get('https://api.binance.com/api/v3/ticker/24hr').json(), key=lambda x: float(x['priceChangePercent']), reverse=True)[1]

    symbol = volatile['symbol']
    price = float(volatile['lastPrice'])
    quantity = amount / price
    wallet -= quantity * price

    while True:
        time.sleep(1)

        latest = float(requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}').json()['price'])

        if latest >= price:
            increase = wallet + quantity * latest - amount

            print(f'{symbol} has INCREASED by ${latest - price}! Price is now ${latest}, and wallet will have ${wallet + quantity * latest} when sold.')

            if increase >= amount + 1:
                print(f'Selling ${increase}')

                wallet += increase
                quantity -= increase / latest

                print(f'Sold ${increase} of {symbol}! Wallet now has ${wallet}.')

            continue

        print(f'{symbol} has DECREASED by {price - latest}! Price is now ${latest}, and wallet will have ${wallet + quantity * latest} when sold.')

        wallet += quantity * latest

        break