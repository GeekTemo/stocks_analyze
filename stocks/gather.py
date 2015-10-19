# -*- coding:utf-8 -*-
__author__ = 'gongxingfa'

from pyquery import PyQuery as pq
import requests


# [name, code]
def get_stocks():
    url = 'http://quote.eastmoney.com/stocklist.html'
    r = requests.get(url)
    r.encoding = 'gbk'
    html = r.text
    d = pq(html)
    css_path = 'div.quotebody ul li a'
    data = d(css_path)
    import re
    pattern = '(.*)\((.*)\)'
    stocks = []
    for s in data:
        stock = s.text
        m = re.match(pattern, stock)
        stocks.append((m.groups()[0], m.groups()[1]))
    return stocks

