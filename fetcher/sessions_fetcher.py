__author__ = 'gongxingfa'

from pony.orm import db_session
from bo.bo import Stock
from spider import BrowserSpider
from multiprocessing import Queue
from parsers import sessions_parser
from handlers import sessions_handler


if __name__ == '__main__':
    url_queue = Queue(1024)
    bs = BrowserSpider(url_queue, (('.*', sessions_parser, sessions_handler),), browser_nums=5)
    bs.start()
    with db_session:
        stocks = Stock.select_by_sql('select * from stock')[:]
    for s in stocks:
        url_queue.put(s.url)
    bs.wait_finish()

