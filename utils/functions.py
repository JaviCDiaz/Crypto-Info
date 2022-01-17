import os
import datetime
import json

import pandas as pd
import requests
import sqlite3
from sqlite3 import Error


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


# FUNCTION TO GET ALL COINS LISTED IN AN EXCHANGE
def get_coin_list (exchange):
    coin_list = []
    if exchange == 'Binance':
        for coin in requests.get('https://api.binance.com/api/v3/ticker/price').json():
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

    return coin_list


# FUNCTION TO GET COIN INFO
def get_coin_info (exchange, coin):
    ticker_info = {} # {price, vol, quote_vol, change_24h}
    if exchange == 'Binance':
        coin_info = requests.get('https://api.binance.com/api/v3/ticker/24hr?symbol=' + coin + 'USDT').json()
        coin_chart = requests.get('https://api.binance.com/api/v3/klines?symbol=' + coin + 'USDT&interval=1h&limit=24').json()
        ticker_info['price'] = float(coin_info['lastPrice'])
        ticker_info['volume_24h'] = float(coin_info['volume'])
        ticker_info['quote_volume_24h'] = float(coin_info['quoteVolume'])
        ticker_info['change_24h'] = float(coin_info['priceChangePercent'])
        ticker_info['chart_24h'] = []
        for kline in coin_chart:
            ticker_info['chart_24h'].append(float(kline[4]))
        ticker_info['chart_24h'] = json.dumps(ticker_info['chart_24h'])

    elif exchange == 'KuCoin':
        coin_info = requests.get('https://api.kucoin.com/api/v1/market/stats?symbol=' + coin + '-USDT').json()['data']
        time_24h_ago = int((datetime.datetime.now() - datetime.timedelta(hours = 24)).timestamp())
        coin_chart = requests.get('https://api.kucoin.com/api/v1/market/candles?type=1hour&symbol=' + coin + '-USDT&startAt=' + str(time_24h_ago)).json()['data']
        ticker_info['price'] = float(coin_info['last'])
        ticker_info['volume_24h'] = float(coin_info['vol'])
        ticker_info['quote_volume_24h'] = float(coin_info['volValue'])
        ticker_info['change_24h'] = float(coin_info['changeRate']) * 100
        ticker_info['chart_24h'] = []
        for kline in coin_chart:
            ticker_info['chart_24h'].append(float(kline[2]))
        ticker_info['chart_24h'] = json.dumps(ticker_info['chart_24h'][::-1])

    elif exchange == 'GateIO':
        coin_info = requests.get('https://api.gateio.ws/api/v4/spot/tickers?currency_pair=' + coin + '_USDT').json()[0]
        coin_chart = requests.get('https://api.gateio.ws/api/v4/spot/candlesticks?currency_pair=' + coin + '_USDT&limit=24&interval=1h').json()
        ticker_info['price'] = float(coin_info['last'])
        ticker_info['volume_24h'] = float(coin_info['base_volume'])
        ticker_info['quote_volume_24h'] = float(coin_info['quote_volume'])
        ticker_info['change_24h'] = float(coin_info['change_percentage'])
        ticker_info['chart_24h'] = []
        for kline in coin_chart:
            ticker_info['chart_24h'].append(float(kline[2]))
        ticker_info['chart_24h'] = json.dumps(ticker_info['chart_24h'])

    elif exchange == 'Kraken':
        coin_info = list(requests.get('https://api.kraken.com/0/public/Ticker?pair=' + coin + 'USD').json()['result'].values())[0]
        time_24h_ago = (datetime.datetime.now() - datetime.timedelta(hours = 24)).timestamp()
        coin_chart = list(requests.get('https://api.kraken.com/0/public/OHLC?pair=' + coin + 'USD&interval=60&since=' + str(time_24h_ago)).json()['result'].values())[0]
        ticker_info['price'] = float(coin_chart[-1][4])
        ticker_info['volume_24h'] = float(coin_info['v'][-1])
        ticker_info['quote_volume_24h'] = -1 # NO DATA
        ticker_info['change_24h'] = (float(coin_chart[-1][4]) / float(coin_chart[0][1]) - 1) * 100
        ticker_info['chart_24h'] = []
        for kline in coin_chart:
            ticker_info['chart_24h'].append(float(kline[4]))
        ticker_info['chart_24h'] = json.dumps(ticker_info['chart_24h'])

    elif exchange == 'Huobi':
        coin_info = requests.get('https://api.huobi.pro/market/detail?symbol=' + coin.lower() + 'usdt').json()['tick']
        coin_chart = requests.get('https://api.huobi.pro/market/history/kline?period=60min&size=24&symbol=' + coin.lower() + 'usdt').json()['data']
        ticker_info['price'] = coin_info['close']
        ticker_info['volume_24h'] = coin_info['amount']
        ticker_info['quote_volume_24h'] = coin_info['vol']
        ticker_info['change_24h'] = (coin_chart[0]['close'] / coin_chart[-1]['open'] - 1) * 100
        ticker_info['chart_24h'] = []
        for kline in coin_chart:
            ticker_info['chart_24h'].append(kline['close'])
        ticker_info['chart_24h'] = json.dumps(ticker_info['chart_24h'][::-1])

    elif exchange == 'Coinbase':
        coin_info = requests.get('https://api.exchange.coinbase.com/products/' + coin + '-USD/stats').json()
        coin_chart = list(requests.get('https://api.exchange.coinbase.com/products/' + coin + '-USD/candles?granularity=3600').json())
        ticker_info['price'] = float(coin_info['last'])
        ticker_info['volume_24h'] = float(coin_info['volume'])
        ticker_info['quote_volume_24h'] = -1 # NO DATA
        ticker_info['change_24h'] = (coin_chart[0][4] / coin_chart[23][3] - 1) * 100
        ticker_info['chart_24h'] = []
        for idx in range(24):
            ticker_info['chart_24h'].append(coin_chart[idx][4])
        ticker_info['chart_24h'] = json.dumps(ticker_info['chart_24h'][::-1])

    elif exchange == 'OKEx':
        coin_info = requests.get('https://www.okex.com/api/v5/market/ticker?instId=' + coin + '-USDT').json()['data'][0]
        coin_chart = requests.get('https://www.okex.com/api/v5/market/candles?instId=' + coin + '-USDT&bar=1H&limit=24').json()['data']
        ticker_info['price'] = float(coin_info['last'])
        ticker_info['volume_24h'] = float(coin_info['vol24h'])
        ticker_info['quote_volume_24h'] = float(coin_info['volCcy24h'])
        ticker_info['change_24h'] = (float(coin_info['last']) / float(coin_info['open24h']) - 1) * 100
        ticker_info['chart_24h'] = []
        for kline in coin_chart:
            ticker_info['chart_24h'].append(float(kline[4]))
        ticker_info['chart_24h'] = json.dumps(ticker_info['chart_24h'][::-1])

    return ticker_info


# FUNCTION TO ADD COIN TO DB
def add_coin_to_db (db_path, db_table_name, info):
    conn = None
    success = False
    try:
        conn = sqlite3.connect(db_path)

        conn.cursor().execute(f'''
            CREATE TABLE IF NOT EXISTS {db_table_name}(
                [coin] TEXT,
                [exchange] TEXT,
                [price] FLOAT,
                [volume_24h] FLOAT,
                [quote_volume_24h] FLOAT,
                [change_24h] FLOAT,
                [chart_24h] TEXT,
                UNIQUE (coin, exchange)
            )
        ''')

        conn.cursor().execute(f'''
            INSERT OR IGNORE INTO {db_table_name} (coin, exchange, price, volume_24h, quote_volume_24h, change_24h, chart_24h)
            VALUES ("{info['coin']}", "{info['exchange']}", {info['price']}, {info['volume_24h']}, {info['quote_volume_24h']}, {info['change_24h']}, "{info['chart_24h']}")
        ''')
                            
        conn.commit()
        success = True

    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()

    return success
