# -*- coding:utf-8 -*-
__author__ = 'gongxingfa'

from multiprocessing.dummy import Pool as ThreadPool
from splinter import Browser
from pony.orm import db_session
import pika


def gather_stocks_simple_sessions(stocks):
    browser = Browser('phantomjs')
    browser.visit(stocks.url)
    open = browser.find_by_id('gt1')[0].text
    if open == '-':
        return
    prev_close = browser.find_by_id('gt8')[0].text
    highest_price = browser.find_by_id('gt2')[0].text
    lowest_price = browser.find_by_id('gt9')[0].text
    limit_up = browser.find_by_id('gt3')[0].text
    limit_down = browser.find_by_id('gt10')[0].text
    close = browser.find_by_id('price9')[0].text
    grains = browser.find_by_id('km2')[0].text[0:-1]
    gains_drop = browser.find_by_id('km1')[0].text
    import datetime
    dt = str(datetime.date.today())
    simple_session = {'name': stocks.name, 'code': stocks.code, 'open': open, 'prev_close': prev_close,
                      'highest_price': highest_price,
                      'lowest_price': lowest_price, 'limit_up': limit_up, 'close': close, 'grains': grains,
                      'gains_drop': gains_drop, 'date_time': dt}
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='simple_sessions')
    channel.basic_publish(exchange='',
                          routing_key='simple_sessions',
                          body=str(simple_session))

from bo.sqlite_bo import Stocks
from multiprocessing import Pool
from threading import Thread

@db_session
def start_gather():
    stocks = Stocks.select_by_sql('select * from stocks')[:]
    for s in stocks:
        t = Thread(target=gather_stocks_simple_sessions, args=[s,])
        t.start()
        import time
        time.sleep(1)


start_gather()
