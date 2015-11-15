__author__ = 'gongxingfa'

from pyquery import PyQuery
from pony.orm import db_session, commit
from bo.bo import Stock, Simple_Sessions
from spider import BrowserSpider
from multiprocessing import Queue
from parsers import simple_session_parser
from handlers import simple_sessions_handler


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
