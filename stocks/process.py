__author__ = 'gongxingfa'

from multiprocessing import Process
import logging
from splinter import Browser

logging.basicConfig(level=logging.DEBUG, datefmt='%a, %d %b %Y %H:%M:%S')


class WebPageProcess(Process):
    def __init__(self, url_queue, html_queue):
        Process.__init__(self)
        self.url_queue = url_queue
        self.html_queue = html_queue

    def run(self):
        browser = Browser('chrome')
        logging.warning('Process:%s start visit.' % self.name)
        while True:
            url = self.url_queue.get()
            browser.visit(url)
            html = browser.html
            self.html_queue.put(html)


class HtmlParseProcess(Process):
    def __init__(self, html_queue, parser, target_queue):
        Process.__init__(self)
        self.html_queue = html_queue
        self.parser = parser
        self.target_queue = target_queue

    def run(self):
        logging.warning('HtmlParseProcess:%s start Parse' % self.name)
        while True:
            html = self.html_queue.get()
            result = self.parser(html)
            self.target_queue.put(result)

