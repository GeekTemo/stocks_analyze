__author__ = 'gongxingfa'

from multiprocessing import Queue
from parsers import stock_index_parser
from handlers import stock_index_handler
from spider import BrowserSpider

if __name__ == '__main__':
    url_queue = Queue(1)
    url_queue.put('http://quote.eastmoney.com/center/index.html#zyzs_0_1')
    bs = BrowserSpider(url_queue, (('.*', stock_index_parser, stock_index_handler),))
    bs.start()