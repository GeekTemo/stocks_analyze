# -*- coding:utf-8 -*-
__author__ = 'gongxingfa'

#from pyquery import PyQuery as pq
#import requests


def _query(html, css_path):
    d = pq(html)
    return d(css_path)


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

from splinter import Browser
browser = Browser()
def gather_stock_sessions(stock_url):
    browser.visit(stock_url)
    css_path = 'table.yfw td.txtl'
    data = browser.find_by_css(css_path)
    values = [v.text for v in data]
    return values
    #open, highest_price, limit_up, turnover_rate, volume, price_earnings, total_market_cap = values


print(gather_stock_sessions('http://quote.eastmoney.com/sz002217.html'))
