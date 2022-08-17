#!/usr/bin/env python3

import requests
import json
import time

from prometheus_client import start_http_server, Gauge

BINANCE_API = 'https://api.binance.com'

def get_data(path):
    url = BINANCE_API + path

    try:
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
        else:
            print("I got wront response code or format: %s : %s" % (r.status_code, r.text))
            return {}
    except Exception as e:
        print("Can't open API: %s" % (e))
        return {}

    return data


def get_24hr_data():
    """
    https://api.binance.com/api/v3/ticker/24hr returns info about 24 hours trades
    """
    # for test with cached result in file 24hr uncomment lines
    # with open('24hr') as f:
    #     return json.loads(f.read())

    s24hr =  get_data('/api/v3/ticker/24hr')

    return s24hr


def top_5_by_volume(s24hr):
    """
    1. Print the top 5 symbols with quote asset BTC and the highest volume over the last 24 hours in descending order.
    GET https://api.binance.com/api/v3/exchangeInfo
    """

    limit = 5
    assetBTC = {}
    for sym in s24hr:
        if sym["symbol"].endswith('BTC'):
            assetBTC.update({sym["symbol"]:float(sym["quoteVolume"])})

    top_5_vol = {}
    for sym in sorted(assetBTC, key=assetBTC.get, reverse=True)[:limit]:
        print(sym, assetBTC[sym])
        top_5_vol.update({sym: assetBTC[sym]})

    return top_5_vol


def top_5_by_count(s24hr):
    """
    2. Print the top 5 symbols with quote asset USDT and the highest number of trades over the last 24 hours in descending order.
    """
    limit = 5
    assetBTC = {}
    for sym in s24hr:
        if sym["symbol"].endswith('USDT'):
            assetBTC.update({sym["symbol"]:float(sym["count"])})

    top_5_count = {}
    for sym in sorted(assetBTC, key=assetBTC.get, reverse=True)[:limit]:
        print(sym, assetBTC[sym])
        top_5_count.update({sym:assetBTC[sym]})

    return top_5_count


def bids_asks(symbols):
    """
    3. Using the symbols from Q1, what is the total notional value of the top 200 bids and asks currently on each order book?
    'https://api.binance.com/api/v3/depth?symbol=ETHBTC&limit=200'
    """
    print("Sym\tbids\tasks")
    for s in symbols:
        path = '/api/v3/depth?symbol=%s&limit=200' % (s)
        depth = get_data(path)
        bids = asks = 0
        for b in depth['bids']:
            bids += float(b[0]) * float(b[1])

        for a in depth['asks']:
            asks += float(a[0]) * float(a[1])
        print("%s\t%s\t%s" % (s, bids, asks))


def price_spread(symbols, price=False):
    """
    4. What is the price spread for each of the symbols from Q2?
    """
    res = {}
    for s in symbols:
        path = '/api/v3/depth?symbol=%s' % (s)
        depth = get_data(path)
        max_bid = float(depth['bids'][0][0])
        for b in depth['bids']:
            max_bid = max(max_bid, float(b[0]))

        min_ack = float(depth['asks'][0][0])
        for a in depth['asks']:
            min_ack = min(float(a[0]), min_ack)
        res.update({s: {"spread": min_ack - max_bid}})
        # print("%s\t%s" % (s, min_ack - max_bid))
        if price:
            path = '/api/v3/trades?symbol=%s' % (s)
            trades = get_data(path)
            sym_price = float(trades[0]["price"])
            res[s]["price"] = sym_price

    return res

def price_difference(symbols):
    """
    5. Every 10 seconds print the result of Q4 and the absolute delta from the previous value for each symbol.
    """
    print("price difference")
    price_spread_res, price_spread_res_prev = {}, {}
    price_spread_res = price_spread(symbols, price = True)
    print("Sym\tspread\tprice")

    # Add prometheus metrics
    g_spread = Gauge('symblol_spread', 'Change in symbols, spread', ['symbol'])
    g_price = Gauge('symblol_price_change', 'Change in symbols, price', ['symbol'])

    for i in range(10):
        time.sleep(10)
        price_spread_res_prev = price_spread_res
        price_spread_res = price_spread(symbols, price = True)
        for (k,v) in price_spread_res.items():
            print("%s\t%s\t%s" % (k, v["spread"], price_spread_res_prev[k]["price"] - v["price"]))
            # Add prometheus metrics
            g_spread.labels(k).set(v["spread"])
            g_price.labels(k).set(price_spread_res_prev[k]["price"] - v["price"])

def main():
    print("Hello Binance")
    print("=" * 100)
    print("Get 24hr data from API")
    data = get_24hr_data()
    print("top 5 quote asset BTC symbols by volume")
    top_5_vol = top_5_by_volume(data)

    print("=" * 100)
    print("top 5 quote asset USDT symbols by count")
    top_5_count = top_5_by_count(data)

    print("=" * 100)
    print("total notional value of the top 200 bids and asks")
    print("=" * 100)
    print("price spread")

    price_spread_res = price_spread(top_5_count.keys())
    print("Sym\tspread")
    for (k,v) in price_spread_res.items():
        print("%s\t%s" % (k, v["spread"]))

    print("=" * 100)
    start_http_server(8000)
    price_difference(top_5_count.keys())


if __name__ == '__main__':
    main()
