# -*- coding:utf-8 -*-
__author__ = 'gongxingfa'

from pyquery import PyQuery as pq
import requests


# [name, code]
def gather_stocks():
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
    local = 'sh'
    for s in data:
        stock = s.text
        url = s.attrib['href']
        m = re.match(pattern, stock)
        name, code = m.groups()
        if code == '000001':
            local = 'sz'
        stocks.append((name, code, local, url))
    return stocks

gather_stocks()



