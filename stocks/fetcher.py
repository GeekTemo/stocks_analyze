__author__ = 'gongxingfa'

from multiprocessing import Process, Queue, Lock
from splinter import Browser
from pyquery import PyQuery
from pony.orm import db_session, commit
from bo.sqlite_bo import Stocks, Simple_Sessions

url_queue = Queue()
html_queue = Queue(256)
sessions_queue = Queue(1024)
with db_session:
    stocks = Stocks.select_by_sql('select * from stocks')[:]
STOCKS_COUNT = len(stocks)

web_page_count = 0
web_page_count_lock = Lock()


def increase_page_count():
    global web_page_count
    with web_page_count_lock:
        web_page_count += 1


def get_page_count():
    count = 0
    with web_page_count_lock:
        count = web_page_count
    return count


class WebPageProcess(Process):
    def __init__(self, url_queue, html_queue):
        Process.__init__(self)
        self.url_queue = url_queue
        self.html_queue = html_queue

    def run(self):
        browser = Browser('chrome')
        while True:
            if get_page_count() >= STOCKS_COUNT:
                print('Web Page Finished......')
                return
            url = self.url_queue.get()
            browser.visit(url)
            html = browser.html
            self.html_queue.put(html)
            increase_page_count()


html_count = 0
html_count_lock = Lock()


def increase_hmtl_count():
    global html_count
    with html_count_lock:
        html_count += 1


def get_html_count():
    count = 0
    with html_count_lock:
        count = html_count
    return count


class HtmlParseProcess(Process):
    def __init__(self, html_queue, sessions_queue):
        Process.__init__(self)
        self.html_queue = html_queue
        self.sessions_queue = sessions_queue

    def run(self):
        while True:
            if get_html_count() >= STOCKS_COUNT:
                print('Finish Html Parse Finish...')
                return
            html = self.html_queue.get()
            d = PyQuery(html)
            open_price = d('#gt1')[0].text
            if open_price == '-':
                increase_hmtl_count()
                continue
            prev_close = d('#gt8')[0].text
            highest_price = d('#gt2')[0].text
            lowest_price = d('#gt9')[0].text
            limit_up = d('#gt3')[0].text
            limit_down = d('#gt10')[0].text
            close = d('#price9')[0].text
            grains = d('#km2')[0].text[0:-1]
            gains_drop = d('#km1')[0].text
            import datetime
            dt = str(datetime.date.today())
            name = d('#name')[0].text
            code = d('#code')[0].text
            session = {'name': name, 'code': code, 'open': open_price, 'prev_close': prev_close,
                       'highest_price': highest_price,
                       'lowest_price': lowest_price, 'limit_up': limit_up, 'limit_down': limit_down, 'close': close,
                       'grains': grains,
                       'gains_drop': gains_drop, 'date_time': dt}
            self.sessions_queue.put(session)
            increase_hmtl_count()


persistent_count = 0
persistent_count_lock = Lock()


def increase_persistent_count():
    global persistent_count
    with persistent_count_lock:
        persistent_count += 1


def get_persistent_count():
    count = 0
    with persistent_count_lock:
        count = persistent_count
    return count


class PersistentProcess(Process):
    def __init__(self, sessions_queue):
        Process.__init__(self)
        self.sessions_queue = sessions_queue

    @staticmethod
    def _new_sessions_from_dict(cls, d):
        sessions = cls()
        # sessions.name = d.get('name')
        # sessions.code = d.get('code')
        # sessions.open = d.get('open')
        # sessions.prev_close = d.get('prev_close')
        # sessions.highest_price = d.get('highest_price')
        # sessions.lowest_price = d.get('lowest_price')
        # sessions.limit_up = d.get('limit_up')
        # sessions.limit_down = d.get('limit_down')
        # sessions.close = d.get('close')
        # sessions.grains = d.get('grains')
        # sessions.gains_drop = d.get('gains_drop')
        # sessions.date_time = d.get('date_time')
        sessions.set(**d)
        return sessions

    @db_session
    def run(self):
        while True:
            if get_persistent_count() >= STOCKS_COUNT:
                print('Persistent Process Finished....')
            sessions = self.sessions_queue.get()
            simple_sessions = Simple_Sessions()
            simple_sessions.set(**sessions)
            # simple_sessions = Simple_Sessions(name=sessions['name'], code=sessions['code'], open=sessions['open'],
            #                                   prev_close=sessions['prev_close'],
            #                                   highest_price=sessions['highest_price'],
            #                                   lowest_price=sessions['lowest_price'],
            #                                   limit_up=sessions['limit_up'], limit_down=sessions['limit_down'],
            #                                   close=sessions['close'], grains=sessions['grains'],
            #                                   gains_drop=sessions['gains_drop'],
            #                                   date_time=sessions['date_time'])
            commit()
            increase_persistent_count()


if __name__ == '__main__':
    web_page_processes = [WebPageProcess(url_queue, html_queue) for i in range(10)]
    html_parse_process = HtmlParseProcess(html_queue, sessions_queue)
    persistent_process = PersistentProcess(sessions_queue)
    for p in web_page_processes:
        p.start()
    html_parse_process.start()
    persistent_process.start()
    for s in stocks:
        url_queue.put(s.url)
    persistent_process.join()
    print('Start Fetcher........')
