# -*- coding:utf-8 -*-
__author__ = 'gongxingfa'


def write_stocks(conn, stocks):
    cur = conn.cursor()
    for name, code, local, url in stocks:
        sql = "insert into stocks(name, code, local, url) VALUES('%s', '%s', '%s', '%s')"%(name, code, local, url)
        cur.execute(sql)
        conn.commit()


from gather import gather_stocks
stocks = gather_stocks()

import sqlite3
conn = sqlite3.connect('/Users/gongxingfa/stocks_analyze.db')
write_stocks(conn, stocks)

