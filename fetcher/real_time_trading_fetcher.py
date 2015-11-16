__author__ = 'gongxingfa'

from splinter import Browser
from multiprocessing import Process
import datetime
import time
from pony.orm import db_session, commit
from bo.bo import Real_Time_Trading


class RealTimeBrowserProcess(Process):
    def __init__(self, urls):
        Process.__init__(self)
        self.urls = urls
        self.browsers = [Browser('chrome') for i in range(len(self.urls))]

    def run(self):
        for i in range(len(self.urls)):
            self.browsers[i].visit(self.urls[i])
        while True:
            for browser in self.browsers:
                name = browser.find_by_id('name')[0].text
                code = browser.find_by_id('code')[0].text
                price = browser.find_by_id('price9')[0].text
                change_rate = browser.find_by_id('km2')[0].text[0:-1]
                change_amount = browser.find_by_id('km1')[0].text
                turnover_rate = browser.find_by_id('gt4')[0].text[0:-1]
                quantity_relative = browser.find_by_id('gt11')[0].text
                volume = browser.find_by_id('gt5')[0].text
                turnover = browser.find_by_id('gt12')[0].text
                real_time = datetime.datetime.now()
                date_time = str(datetime.date.today())
                real_time_trading = dict(name=name, code=code, price=price,change_rate=change_rate, change_amount=change_amount,
                                         turnover_rate=turnover_rate, quantity_relative=quantity_relative,
                                         volume=volume, turnover=turnover, real_time=real_time, date_time=date_time)
                with db_session:
                    rtl = Real_Time_Trading()
                    rtl.set(**real_time_trading)
                    commit()





if __name__ == '__main__':
    urls = ['http://quote.eastmoney.com/sz002217.html', 'http://quote.eastmoney.com/sz000707.html',
            'http://quote.eastmoney.com/sz000593.html', 'http://quote.eastmoney.com/sz000567.html',
            'http://quote.eastmoney.com/sh600744.html']
    real_process = RealTimeBrowserProcess(urls)
    real_process.start()









