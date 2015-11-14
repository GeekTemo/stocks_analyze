__author__ = 'gongxingfa'

from pyquery import PyQuery
import datetime
from lxml.etree import fromstring
from cssselect import GenericTranslator


def simple_session_parser(html):
    d = PyQuery(html)
    open_price = d('#gt1')[0].text
    if open_price == '-':
        return ''
    prev_close = d('#gt8')[0].text
    highest_price = d('#gt2')[0].text
    lowest_price = d('#gt9')[0].text
    limit_up = d('#gt3')[0].text
    limit_down = d('#gt10')[0].text
    close = d('#price9')[0].text
    change_rate = d('#km2')[0].text[0:-1]
    change_amount = d('#km1')[0].text
    import datetime
    dt = str(datetime.date.today())
    name = d('#name')[0].text
    code = d('#code')[0].text
    session = {'name': name, 'code': code, 'open': open_price, 'prev_close': prev_close,
               'highest_price': highest_price,
               'lowest_price': lowest_price, 'limit_up': limit_up, 'limit_down': limit_down, 'close': close,
               'change_rate': change_rate,
               'change_amount': change_amount, 'date_time': dt}
    return session


def stock_index_parser(html):
    start = '<div id="zyzs" class="mod-datas">'
    end = '<div class="space-10">'
    start_index = html.find(start)
    end_index = html.find(end, start_index)
    data_div = html[start_index:end_index]
    expr = GenericTranslator().css_to_xpath('tr')
    doc = fromstring(data_div)
    trs = [e for e in document.xpath(expr)][1:]
    stock_indexs = []
    for tr in trs:
        tds = tr.getchildren()
        code = tds[0].getchildren()[0].text
        name = tds[1].getchildren()[0].text
        latest_price = tds[2].getchildren()[0].text
        change_amount = tds[3].getchildren()[0].text
        change_rate = tds[4].getchildren()[0].text[0:-1]
        volume = tds[5].text
        turnover = tds[6].text
        prev_close = tds[7].text
        today_open = tds[8].getchildren()[0].text
        highest = tds[9].getchildren()[0].text
        lowest = tds[10].getchildren()[0].text
        date_time = str(datetime.date.today())
        stock_index = dict(code=code, name=name, latest_price=latest_price, change_amount=change_amount,
                           change_rate=change_rate, volume=volume, turnover=turnover, prev_close=prev_close,
                           open=today_open, highest=highest, lowest=lowest, date_time=date_time)
        stock_indexs.append(stock_index)
    return stock_indexs
