import time
import requests

amount = 100
wallet = amount
symbol = ''

while True:
    coins = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=cad&order=market_cap_asc&per_page=250&price_change_percentage=1h', 'x-cg-demo-api-key: CG-VsuBhYY5sKsk5bQZCcBfziaB').json()

    for coin in coins:
        if coin['price_change_percentage_24h'] and float(coin['price_change_percentage_24h']) > 0 and coin['symbol'] != symbol:
            symbol = coin['symbol']
            price = float(coin['current_price'])
            id = coin['id']

    quantity = amount / price
    wallet -= quantity * price

    while True:
        latest = float(requests.get(f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=cad&ids={id}&order=market_cap_asc&per_page=250&price_change_percentage=1h', 'x-cg-demo-api-key: CG-VsuBhYY5sKsk5bQZCcBfziaB').json()['current_price'])

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