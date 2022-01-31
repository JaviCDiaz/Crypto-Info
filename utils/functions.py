import os
import datetime
import json

import requests
import asyncio
from aiohttp import ClientSession


# FUNCTION TO GET ICONS
def get_icon_path (icon_name, folder_name='icons'):
    app_path = os.path.abspath(os.getcwd())
    folder_path = os.path.join(app_path, folder_name)
    icon_path = os.path.normpath(os.path.join(folder_path, icon_name))
    icon_path = icon_path.replace('\\', '/')
    return icon_path


# FUNCTION TO GET COIN ICONS
def get_coin_icon (coin_name, size=16):
    if coin_name[-2:] == 'UP':
        icon_name = coin_name[:-2]
    elif coin_name[-4:] == 'DOWN':
        icon_name = coin_name[:-4]
    else:
        icon_name = coin_name

    icon_coin_name = icon_name + '_' + str(size) + '.png'
    icon_coin_path = get_icon_path(icon_coin_name, 'icons/coins_png')
    if os.path.isfile(icon_coin_path):
        return icon_coin_path
    else:
        return get_icon_path('BTC_' + str(size) + '.png', 'icons/coins_png')


# FUNCTION TO GET EXCHANGE ICONS
def get_exchange_icon (exchange_name, size=16):
    icon_coin_name = exchange_name + '_' + str(size) + '.png'
    icon_coin_path = get_icon_path(icon_coin_name, 'icons/exchanges_png')
    if os.path.isfile(icon_coin_path):
        return icon_coin_path
    else:
        return get_icon_path('binance_' + str(size) + '.png', 'icons/exchanges_png')


# FUNCTION TO LOAD COIN LISTS FROM ALL EXCHANGES
def get_all_coin_lists ():
    urls = [
        {'exchange': 'Binance', 'url': 'https://api.binance.com/api/v3/ticker/price'},
        {'exchange': 'KuCoin', 'url': 'https://api.kucoin.com/api/v1/market/allTickers'},
        {'exchange': 'GateIO', 'url': 'https://api.gateio.ws/api/v4/spot/currency_pairs'},
        {'exchange': 'Kraken', 'url': 'https://api.kraken.com/0/public/Assets'},
        {'exchange': 'Huobi', 'url': 'https://api.huobi.pro/v1/common/symbols'},
        {'exchange': 'Coinbase', 'url': 'https://api.exchange.coinbase.com/products'},
        {'exchange': 'OKEx', 'url': 'https://www.okex.com/api/v5/market/tickers?instType=SPOT'}
    ]

    async def fetch (url, session):
        async with session.get(url) as response:
            return await response.json()

    async def run (urls):
        tasks = []

        async with ClientSession() as session:
            for url in urls:
                task_coin_list = asyncio.ensure_future(fetch(url['url'], session))
                tasks.append(task_coin_list)

            responses = [[url['exchange'] for url in urls], await asyncio.gather(*tasks)]
            return responses

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(urls))
    loop.run_until_complete(future)

    return format_coin_lists(future.result())

def format_coin_lists (coin_lists_request_results):
    all_coin_lists = []

    for idx in range(len(coin_lists_request_results[0])):
        coin_list = []
        exchange = coin_lists_request_results[0][idx]

        if exchange == 'Binance':
            for coin in coin_lists_request_results[1][idx]:
                if coin['symbol'][-4:] == 'USDT':
                    coin_list.append(coin['symbol'][:-4])

        elif exchange == 'KuCoin':
            for coin in requests.get('https://api.kucoin.com/api/v1/market/allTickers').json()['data']['ticker']:
                coin_ticker = coin['symbol'].split('-')[0]
                if coin_ticker not in coin_list:
                    coin_list.append(coin['symbol'].split('-')[0])

        elif exchange == 'GateIO':
            for coin in requests.get('https://api.gateio.ws/api/v4/spot/currency_pairs').json():
                coin_ticker = coin['base']
                if coin['base'] not in coin_list:
                    coin_list.append(coin_ticker)

        elif exchange == 'Kraken':
            for coin in requests.get('https://api.kraken.com/0/public/Assets').json()['result']:
                if coin not in coin_list:
                    coin_list.append(coin)

        elif exchange == 'Huobi':
            for coin in requests.get('https://api.huobi.pro/v1/common/symbols').json()['data']:
                coin_ticker = coin['base-currency'].upper()
                if coin_ticker not in coin_list:
                    coin_list.append(coin_ticker)

        elif exchange == 'Coinbase':
            for coin in requests.get('https://api.exchange.coinbase.com/products').json():
                coin_ticker = coin['base_currency']
                if coin_ticker not in coin_list:
                    coin_list.append(coin_ticker)

        elif exchange == 'OKEx':
            for coin in requests.get('https://www.okex.com/api/v5/market/tickers?instType=SPOT').json()['data']:
                coin_ticker = coin['instId'].split('-')[0]
                if coin_ticker not in coin_list:
                    coin_list.append(coin_ticker)

        all_coin_lists.append({'exchange': exchange, 'coin_list': coin_list})

    return all_coin_lists


# FUNCTION TO GET COINS INFO
def get_coins_info_urls (db_coins_info):
    urls = []

    for coin_info in db_coins_info:
        current_url_data = {}

        coin_name = coin_info['coin']
        exchange = coin_info['exchange']
        
        current_url_data['coin'] = coin_name
        current_url_data['exchange'] = exchange

        if exchange == 'Binance':
            current_url_data['coin_info_url'] = 'https://api.binance.com/api/v3/ticker/24hr?symbol=' + coin_name + 'USDT'
            current_url_data['coin_chart_url'] = 'https://api.binance.com/api/v3/klines?symbol=' + coin_name + 'USDT&interval=1h&limit=168'

        elif exchange == 'KuCoin':
            current_url_data['coin_info_url'] = 'https://api.kucoin.com/api/v1/market/stats?symbol=' + coin_name + '-USDT'
            time_24h_ago = int((datetime.datetime.now() - datetime.timedelta(hours = 168)).timestamp())
            current_url_data['coin_chart_url'] = 'https://api.kucoin.com/api/v1/market/candles?type=1hour&symbol=' + coin_name + '-USDT&startAt=' + str(time_24h_ago)

        elif exchange == 'GateIO':
            current_url_data['coin_info_url'] = 'https://api.gateio.ws/api/v4/spot/tickers?currency_pair=' + coin_name + '_USDT'
            current_url_data['coin_chart_url'] = 'https://api.gateio.ws/api/v4/spot/candlesticks?currency_pair=' + coin_name + '_USDT&limit=168&interval=1h'

        elif exchange == 'Kraken':
            current_url_data['coin_info_url'] = 'https://api.kraken.com/0/public/Ticker?pair=' + coin_name + 'USD'
            time_24h_ago = (datetime.datetime.now() - datetime.timedelta(hours = 168)).timestamp()
            current_url_data['coin_chart_url'] = 'https://api.kraken.com/0/public/OHLC?pair=' + coin_name + 'USD&interval=60&since=' + str(time_24h_ago)

        elif exchange == 'Huobi':
            current_url_data['coin_info_url'] = 'https://api.huobi.pro/market/detail?symbol=' + coin_name.lower() + 'usdt'
            current_url_data['coin_chart_url'] = 'https://api.huobi.pro/market/history/kline?period=60min&size=168&symbol=' + coin_name.lower() + 'usdt'

        elif exchange == 'Coinbase':
            current_url_data['coin_info_url'] = 'https://api.exchange.coinbase.com/products/' + coin_name + '-USD/stats'
            current_url_data['coin_chart_url'] = 'https://api.exchange.coinbase.com/products/' + coin_name + '-USD/candles?granularity=3600'

        elif exchange == 'OKEx':
            current_url_data['coin_info_url'] = 'https://www.okex.com/api/v5/market/ticker?instId=' + coin_name + '-USDT'
            current_url_data['coin_chart_url'] = 'https://www.okex.com/api/v5/market/candles?instId=' + coin_name + '-USDT&bar=1H&limit=168'

        urls.append(current_url_data)

    return urls

def get_coins_info (urls):
    async def fetch (url, session):
        async with session.get(url) as response:
            return await response.json()

    async def run (urls):
        tasks = []

        async with ClientSession() as session:
            for url in urls:
                task_coin_info = asyncio.ensure_future(fetch(url['coin_info_url'], session))
                task_coin_chart = asyncio.ensure_future(fetch(url['coin_chart_url'], session))
                tasks.append(task_coin_info)
                tasks.append(task_coin_chart)

            responses = [[info['coin'] for info in urls], [info['exchange'] for info in urls], await asyncio.gather(*tasks)]
            return responses

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(urls))
    loop.run_until_complete(future)

    return future.result()

def format_coin_info (coin, exchange, coin_info, coin_chart):
    ticker_info = {}
    ticker_info['coin'] = coin
    ticker_info['exchange'] = exchange
    if exchange == 'Binance':
        coin_info = coin_info
        coin_chart = coin_chart
        ticker_info['price'] = float(coin_info['lastPrice'])
        ticker_info['volume_24h'] = float(coin_info['volume'])
        ticker_info['quote_volume_24h'] = float(coin_info['quoteVolume'])
        ticker_info['change_24h'] = float(coin_info['priceChangePercent'])
        ticker_info['chart_7d'] = []
        for kline in coin_chart:
            ticker_info['chart_7d'].append(float(kline[4]))
        ticker_info['chart_7d'] = json.dumps(ticker_info['chart_7d'])

    elif exchange == 'KuCoin':
        coin_info = coin_info['data']
        coin_chart = coin_chart['data']
        ticker_info['price'] = float(coin_info['last'])
        ticker_info['volume_24h'] = float(coin_info['vol'])
        ticker_info['quote_volume_24h'] = float(coin_info['volValue'])
        ticker_info['change_24h'] = float(coin_info['changeRate']) * 100
        ticker_info['chart_7d'] = []
        for kline in coin_chart:
            ticker_info['chart_7d'].append(float(kline[2]))
        ticker_info['chart_7d'] = json.dumps(ticker_info['chart_7d'][::-1])

    elif exchange == 'GateIO':
        coin_info = coin_info[0]
        coin_chart = coin_chart
        ticker_info['price'] = float(coin_info['last'])
        ticker_info['volume_24h'] = float(coin_info['base_volume'])
        ticker_info['quote_volume_24h'] = float(coin_info['quote_volume'])
        ticker_info['change_24h'] = float(coin_info['change_percentage'])
        ticker_info['chart_7d'] = []
        for kline in coin_chart:
            ticker_info['chart_7d'].append(float(kline[2]))
        ticker_info['chart_7d'] = json.dumps(ticker_info['chart_7d'])

    elif exchange == 'Kraken':
        coin_info = list(coin_info['result'].values())[0]
        coin_chart = list(coin_chart['result'].values())[0]
        ticker_info['price'] = float(coin_chart[-1][4])
        ticker_info['volume_24h'] = float(coin_info['v'][-1])
        ticker_info['quote_volume_24h'] = -1 # NO DATA
        ticker_info['change_24h'] = (float(coin_chart[-1][4]) / float(coin_chart[0][1]) - 1) * 100
        ticker_info['chart_7d'] = []
        for kline in coin_chart:
            ticker_info['chart_7d'].append(float(kline[4]))
        ticker_info['chart_7d'] = json.dumps(ticker_info['chart_7d'])

    elif exchange == 'Huobi':
        coin_info = coin_info['tick']
        coin_chart = coin_chart['data']
        ticker_info['price'] = coin_info['close']
        ticker_info['volume_24h'] = coin_info['amount']
        ticker_info['quote_volume_24h'] = coin_info['vol']
        ticker_info['change_24h'] = (coin_chart[0]['close'] / coin_chart[-1]['open'] - 1) * 100
        ticker_info['chart_7d'] = []
        for kline in coin_chart:
            ticker_info['chart_7d'].append(kline['close'])
        ticker_info['chart_7d'] = json.dumps(ticker_info['chart_7d'][::-1])

    elif exchange == 'Coinbase':
        coin_info = coin_info
        coin_chart = list(coin_chart)
        ticker_info['price'] = float(coin_info['last'])
        ticker_info['volume_24h'] = float(coin_info['volume'])
        ticker_info['quote_volume_24h'] = -1 # NO DATA
        ticker_info['change_24h'] = (coin_chart[0][4] / coin_chart[23][3] - 1) * 100
        ticker_info['chart_7d'] = []
        for idx in range(168):
            ticker_info['chart_7d'].append(coin_chart[idx][4])
        ticker_info['chart_7d'] = json.dumps(ticker_info['chart_7d'][::-1])

    elif exchange == 'OKEx':
        coin_info = coin_info['data'][0]
        coin_chart = coin_chart['data']
        ticker_info['price'] = float(coin_info['last'])
        ticker_info['volume_24h'] = float(coin_info['vol24h'])
        ticker_info['quote_volume_24h'] = float(coin_info['volCcy24h'])
        ticker_info['change_24h'] = (float(coin_info['last']) / float(coin_info['open24h']) - 1) * 100
        ticker_info['chart_7d'] = []
        for kline in coin_chart:
            ticker_info['chart_7d'].append(float(kline[4]))
        ticker_info['chart_7d'] = json.dumps(ticker_info['chart_7d'][::-1])

    return ticker_info
