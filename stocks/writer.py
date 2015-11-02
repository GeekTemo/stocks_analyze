# -*- coding:utf-8 -*-
__author__ = 'gongxingfa'


def write_stocks(conn, stocks):
    cur = conn.cursor()
    for name, code, local, url in stocks:
        sql = "insert into stocks(name, code, local, url) VALUES('%s', '%s', '%s', '%s')" % (name, code, local, url)
        cur.execute(sql)
        conn.commit()


def write_sessions(conn, data):
    import string
    t = "INSERT INTO sessions(name, open, prev_close, highest_price, lowest_price, limit_up, limit_down, turnover_rate, quantity_relative, volume, turnover, price_earnings, price_book, total_market_cap, tradable_market_cap, sessions_date, close, grains, gains_drop) VALUES ('$name', '$open', '$prev_close', '$highest_price', '$lowest_price', '$limit_up', '$limit_down', '$turnover_rate', '$quantity_relative', '$volume', '$turnover', '$price_earnings', '$price_book', '$total_market_cap', '$tradable_market_cap', '$sessions_date', '$close', '$grains', '$gains_drop')"
    t = string.Template(t)
    cur = conn.cursor()
    sql = t.substitute(data)
    cur.execute(sql)
    conn.commit()

from gather import gather_stocks

stocks = gather_stocks()

import sqlite3

conn = sqlite3.connect('/Users/gongxingfa/stocks_analyze.db')
write_stocks(conn, stocks)
