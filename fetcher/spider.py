__author__ = 'gongxingfa'

from multiprocessing import Process, Queue
import logging
from splinter import Browser
import re

logging.basicConfig(level=logging.WARNING, datefmt='%a, %d %b %Y %H:%M:%S')


class BrowserProcess(Process):
    def __init__(self, url_queue, output_queue):
        Process.__init__(self)
        self.url_queue = url_queue
        self.output_queue = output_queue

    def run(self):
        browser = Browser('chrome')
        logging.warning('Process:%s start.' % self.name)
        while True:
            url = self.url_queue.get()
            browser.visit(url)
            html = browser.html
            self.output_queue.put((url, html))


class DispatcherProcess(Process):
    def __init__(self, patters, input_queue, output_queue):
        Process.__init__(self)
        self.patters = patters
        self.input_queue = input_queue
        self.output_queue = output_queue

    def run(self):
        logging.warning('Process:%s start.' % self.name)
        while True:
            url, html = self.input_queue.get()
            parser, handler = self._match(url)
            self.output_queue.put((html, parser, handler))

    def _match(self, url):
        for pattern, parser, handler in self.patters:
            if re.match(pattern, url):
                return parser, handler


class HtmlParserProcess(Process):
    def __init__(self, input_queue, output_queue):
        Process.__init__(self)
        self.input_queue = input_queue
        self.output_queue = output_queue

    def run(self):
        logging.warning('HtmlParseProcess:%s start Parse' % self.name)
        while True:
            html, parser, handler = self.input_queue.get()
            data = parser(html)
            if data:
                self.output_queue.put((data, handler))


class HandlerProcess(Process):
    def __init__(self, input_queue):
        Process.__init__(self)
        self.input_queue = input_queue

    def run(self):
        logging.warning('Process:%s start.'%self.name)
        while True:
            data, handler = self.input_queue.get()
            handler(data)

class BrowserSpider(object):
    def __init__(self, url_queue, patters, browser_nums = 1, parser_nums = 1, handler_nums = 1):
        self.url_queue = url_queue
        self.html_queue = Queue(256)
        self.parser_queue = Queue(256)
        self.handler_queue = Queue(256)
        self.patters = patters
        self.browsers = [BrowserProcess(self.url_queue, self.html_queue) for i in range(browser_nums)]
        self.dispatcher = DispatcherProcess(self.patters, self.html_queue, self.parser_queue)
        self.parsers = [HtmlParserProcess(self.parser_queue, self.handler_queue) for i in range(parser_nums)]
        self.handlers = [HandlerProcess(self.handler_queue) for i in range(handler_nums)]

    def start(self):
        for browser in self.browsers:
            browser.start()
        self.dispatcher.start()
        for parser in self.parsers:
            parser.start()
        for handler in self.handlers:
            handler.start()

    def stop(self):
        pass
