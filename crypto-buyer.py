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

    print(requests.get(f'https://api.binance.com/api/v3/ticker?symbol=RAREBTC').json())

    symbol = volatile['symbol']
    price = float(volatile['lastPrice'])
    quantity = amount / price
    wallet -= quantity * price

    print(symbol, price, quantity, wallet)

    while True:
        time.sleep(1)
        
        latest = float(requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}').json()['price'])

        if latest >= price:
            increase = wallet + quantity * latest - amount

            print(f'{symbol} has INCREASED by {latest - price:.8f}! Price is now ${latest:.8f}, and wallet will have ${wallet + quantity * latest:.8f} when sold.')

            price = latest

            if increase >= 1:
                print(f'Selling ${increase}')

                wallet += increase
                quantity -= increase / latest

                print(f'Sold ${increase} of {symbol}! Wallet now has ${wallet}.')

            continue

        print(f'{symbol} has DECREASED by {price - latest:.8f}! Price is now ${latest:.8f}, and wallet will have ${wallet + quantity * latest:.8f} when sold.')

        wallet += quantity * latest

        break