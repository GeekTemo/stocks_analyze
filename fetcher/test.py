__author__ = 'gongxingfa'

from pyquery import PyQuery
from pony.orm import db_session, commit
from bo.bo import Stock, Simple_Sessions
from spider import BrowserSpider
from multiprocessing import Queue


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


@db_session
def simple_sessions_handler(data):
    print('.....................................')
    simple_sessions = Simple_Sessions()
    simple_sessions.set(**sessions)
    commit()

if __name__ == '__main__':
    url_queue = Queue(1024)
    bs = BrowserSpider(url_queue, (('.*', simple_session_parser, simple_sessions_handler),))
    bs.start()
    with db_session:
        stocks = Stock.select_by_sql('select * from stock')[:]
        print('......len:%d'%len(stocks))
    for s in stocks:
        url_queue.put(s.url)
    import time
    time.sleep(100)
